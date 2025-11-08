from pydantic import BaseModel, ConfigDict
from typing import Optional

class PositionBase(BaseModel):
    symbol: str
    quantity: float
    portfolio_id: int
    stock_id: int
    buy_price: Optional[float] = None


class PositionCreate(PositionBase):
    pass

class PositionRead(PositionBase):
    id: int
    


class PositionUpdate(PositionBase):
    quantity: Optional[float] = None
    buy_price: Optional[float] = None