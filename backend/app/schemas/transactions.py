from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    portfolio_id: int
    stock_id: int | None = None
    symbol: str
    type: TransactionType
    quantity: float
    price: float 
    
    timestamp: datetime = Field(..., description="Date when the trade occured")
    

    model_config = ConfigDict(from_attributes=True)

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id:int
    total_value: float
    

