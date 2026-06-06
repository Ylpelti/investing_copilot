from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ExternalStockDTO:
    ticker: str
    isin: str
    name: str
    close_price: Decimal
    sector: str | None