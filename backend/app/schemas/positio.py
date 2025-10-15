from pydantic import BaseModel
from typing import Optional

class PositionCreate(BaseModel):
    symbol: str
    quantity: float
    portfolio_id: int
    stock_id: int
    buy_price: Optional[float] = None

class PositionRead(BaseModel):
    id: int
    symbol: str
    quantity: float
    portfolio_id: int
    stock_id: Optional[int] = None
    buy_price: Optional[float] = None

    class Config:
        orm_mode = True

class PositionUpdate(BaseModel):
    quantity: Optional[float] = None
    buy_price: Optional[float] = None