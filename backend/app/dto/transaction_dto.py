from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

@dataclass
class NormalizedTransactionDTO:
    isin: str
    quantity: Decimal
    buy_price: Decimal
    date: datetime
