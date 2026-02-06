from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import date

class StockPriceBase(BaseModel):
    stock_id: int
    date: date
    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    volume: int

    model_config = ConfigDict(from_attributes=True)


class StockPriceCreate(StockPriceBase):
    pass

class StockPriceRead(StockPriceBase):
    id: int
    