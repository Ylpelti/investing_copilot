from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StockCreate(BaseModel):
    ticker: str
    isin: Optional[str] = None
    name: Optional[str] = None
    close_price: float
    sector: Optional[str] = None
    updated_at: Optional[datetime] = None

class StockRead(BaseModel):
    id: int
    ticker: str
    name: Optional[str] = None
    isin: Optional[str] = None
    close_price: float
    sector: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True




