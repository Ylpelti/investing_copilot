from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class StockPriceBase(BaseModel):
    stock_id: int
    date: date
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int

    model_config = ConfigDict(from_attributes=True)


class StockPriceCreate(StockPriceBase):
    pass

class StockPriceRead(StockPriceBase):
    id: int
    