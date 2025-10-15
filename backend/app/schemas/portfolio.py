from pydantic import BaseModel
from typing import Optional

class PortfolioCreate(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: int

class PortfolioRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    user_id: int

    class Config:
        orm_mode = True

class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None