from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class ExternalStockPriceDTO:
    date: date
    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    volume: int