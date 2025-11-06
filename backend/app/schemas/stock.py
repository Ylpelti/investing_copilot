from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class StockBase(BaseModel):
    ticker: str
    isin: Optional[str] = None
    name: Optional[str] = None
    close_price: float
    sector: Optional[str] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class StockCreate(StockBase):
    pass
    

class StockRead(StockBase):
    id: int
    
    



