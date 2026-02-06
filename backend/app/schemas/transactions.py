from pydantic import BaseModel, ConfigDict
from app.models.transaction import TransactionType
from datetime import datetime
from decimal import Decimal

class TransactionBase(BaseModel):
    portfolio_id: int
    stock_id: int
    type: TransactionType
    quantity: Decimal
    price: Decimal 
    timestamp: datetime
    
    

    model_config = ConfigDict(from_attributes=True)

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id:int
    total_value: Decimal
    
    
    

