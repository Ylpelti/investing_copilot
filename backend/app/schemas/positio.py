from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal

class PositionBase(BaseModel):
    symbol: str
    quantity: Decimal
    portfolio_id: int
    stock_id: int
    buy_price: Optional[Decimal] = None


class PositionCreate(PositionBase):
    pass

class PositionRead(PositionBase):
    id: int
    


class PositionUpdate(PositionBase):
    quantity: Optional[Decimal] = None
    buy_price: Optional[Decimal] = None