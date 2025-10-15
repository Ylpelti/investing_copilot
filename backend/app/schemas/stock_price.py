from pydantic import BaseModel
from typing import Optional
from datetime import date

class StockPriceCreate(BaseModel):
    stock_id: int
    date: date
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int

class StockPriceRead(BaseModel):
    id: int
    stock_id: int
    date: date
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int

    class Config:
        orm_mode = True