"""Portfolio import service scaffold for CSV uploads.

This module provides the core plumbing for accepting a user supplied CSV file,
parsing it into raw records, and preparing the data for transformation into the
application's `Position` model.  The actual column matching / transformation
logic is intentionally left open so it can be tailored to each broker specific
schema.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from typing import IO, Any, Dict, Iterable, List, Optional, Protocol, Sequence


@dataclass
class RawCSVRow:
    """Unstructured row as read from the incoming CSV file."""

    original_index: int
    data: Dict[str, str]


@dataclass
class NormalizedPosition:
    """Canonical representation ready to be converted into a `Position`."""

    ticker: str
    quantity: float
    price: Optional[float] = None
    currency: Optional[str] = None
    trade_date: Optional[str] = None  # ISO formatted string to keep parsing flexible
    metadata: Dict[str, Any] = field(default_factory=dict)


class ColumnMatcher(Protocol):
    """Strategy hook for turning raw CSV rows into normalized positions."""

    def __call__(self, headers: Sequence[str]) -> Dict[str, str]:
        """
        Inspect CSV headers and return a mapping to canonical field names.

        Example return value:
            {
                "ticker": "Symbol",
                "quantity": "Shares",
                "price": "Purchase Price",
                "trade_date": "Trade Date",
            }
        """


class PortfolioImportError(Exception):
    """Raised when the CSV file cannot be processed."""


class PortfolioImportService:
    """
    Service object responsible for reading CSV files and normalizing them.

    The default implementation performs three steps:
      1. Read the CSV into `RawCSVRow` objects.
      2. Ask a `ColumnMatcher` (or supplied mapping) how to map broker columns
         into canonical fields.
      3. Produce `NormalizedPosition` objects for downstream persistence.
    """

    def __init__(self, column_matcher: Optional[ColumnMatcher] = None) -> None:
        self._column_matcher = column_matcher

    def read_csv(self, file_obj: IO[str]) -> List[RawCSVRow]:
        """
        Read the uploaded CSV file and return raw rows.

        Raises:
            PortfolioImportError: When the file is empty or malformed.
        """
        reader = csv.DictReader(file_obj)
        if reader.fieldnames is None:
            raise PortfolioImportError("CSV file is missing a header row.")

        rows: List[RawCSVRow] = []
        for idx, row in enumerate(reader, start=1):
            # Skip completely empty lines while preserving line numbers for debugging.
            if not any(row.values()):
                continue
            rows.append(RawCSVRow(original_index=idx, data=row))

        if not rows:
            raise PortfolioImportError("CSV file does not contain any data rows.")
        return rows

    def build_column_mapping(
        self,
        headers: Sequence[str],
        explicit_mapping: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        """
        Determine how broker specific columns map into canonical fields.

        The caller may provide an explicit mapping.  Otherwise a ColumnMatcher
        strategy is invoked, which is where broker specific heuristics should
        live.  The method returns a dictionary such as:

            {
                "ticker": "Symbol",
                "quantity": "Qty",
                "price": "AverageCost",
            }
        """
        if explicit_mapping:
            return explicit_mapping
        if self._column_matcher:
            mapping = self._column_matcher(headers)
            if mapping:
                return mapping
        # Placeholder for future auto-detection enhancements.
        raise PortfolioImportError(
            "Column mapping was not provided and no matcher is configured."
        )

    def normalize_positions(
        self,
        rows: Iterable[RawCSVRow],
        column_mapping: Dict[str, str],
    ) -> List[NormalizedPosition]:
        """
        Convert raw CSV rows into normalized positions using the mapping.

        Missing or unparsable data is stored under `metadata['errors']` so that
        the caller can provide meaningful feedback to the user.
        """
        normalized: List[NormalizedPosition] = []
        for raw in rows:
            data = raw.data
            errors: List[str] = []

            ticker_col = column_mapping.get("ticker")
            quantity_col = column_mapping.get("quantity")

            ticker = data.get(ticker_col, "").strip() if ticker_col else ""
            quantity_raw = data.get(quantity_col, "") if quantity_col else ""

            if not ticker:
                errors.append("Missing ticker")

            try:
                quantity = float(quantity_raw)
            except (TypeError, ValueError):
                quantity = 0.0
                errors.append("Invalid quantity")

            position = NormalizedPosition(
                ticker=ticker,
                quantity=quantity,
                price=self._parse_optional_float(data, column_mapping.get("price")),
                currency=data.get(column_mapping.get("currency", ""), None)
                if column_mapping.get("currency")
                else None,
                trade_date=data.get(column_mapping.get("trade_date", ""), None)
                if column_mapping.get("trade_date")
                else None,
            )

            if errors:
                position.metadata["errors"] = errors
                position.metadata["source_row"] = raw.original_index

            # Attach original raw data for custom matching downstream.
            position.metadata["raw"] = data
            normalized.append(position)
        return normalized

    def import_from_csv(
        self,
        file_obj: IO[str],
        explicit_mapping: Optional[Dict[str, str]] = None,
    ) -> List[NormalizedPosition]:
        """
        High-level helper used by request handlers.

        Returns:
            A list of normalized position objects ready for persistence or
            further matching.
        """
        raw_rows = self.read_csv(file_obj)
        mapping = self.build_column_mapping(
            headers=list(raw_rows[0].data.keys()),
            explicit_mapping=explicit_mapping,
        )
        return self.normalize_positions(raw_rows, mapping)

    @staticmethod
    def _parse_optional_float(data: Dict[str, str], column: Optional[str]) -> Optional[float]:
        if not column:
            return None
        raw = data.get(column)
        if raw is None or raw == "":
            return None
        try:
            return float(raw.replace(",", ""))  # accept "1,234.56" formats
        except ValueError:
            return None

