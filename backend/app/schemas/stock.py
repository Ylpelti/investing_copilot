from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

class StockBase(BaseModel):
    ticker: str
    isin: str
    name: str
    close_price: Decimal
    sector: Optional[str] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class StockCreate(StockBase):
    pass
    

class StockRead(StockBase):
    id: int
    
    



