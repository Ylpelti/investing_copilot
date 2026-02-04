from pydantic import BaseModel, ConfigDict
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    portfolio_id: int
    stock_id: int
    type: TransactionType
    quantity: float
    price: float 
    
    

    model_config = ConfigDict(from_attributes=True)

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id:int
    total_value: float
    symbol: str
    
    

