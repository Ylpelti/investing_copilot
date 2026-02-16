from typing import IO
from app.dto.transaction_dto import NormalizedTransactionDTO
import pandas as pd
from decimal import Decimal
from app.infrastructure.parsers.base_parser import BaseParser

class NordnerCsvParser(BaseParser):

    def parse(self, file: IO[str]) -> list[NormalizedTransactionDTO]:
        result = []
        df = pd.read_csv(file, encoding="utf-16", sep="\t", decimal=',')
        df["Hankintapäivä"] = pd.to_datetime(
            df["Hankintapäivä"],
            format="%d.%m.%Y",
            errors="raise")
        
        for _,row in df.iterrows():
            dto = NormalizedTransactionDTO(
                isin = row["ISIN"],
                quantity = Decimal(row["Määrä"]),
                buy_price = Decimal(row["Hankinta-arvo (Noteerausvaluutta)"]),
                date = row["Hankintapäivä"].date()
            )
            result.append(dto)
        return result
            
