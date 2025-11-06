from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Annotated
from datetime import datetime

class PortfolioBase(BaseModel):
    name: Optional[Annotated[str, Field(min_length=2, max_length=20)]] = "Untitled Portfolio"
    description: Optional[Annotated[str, Field(max_length=100)]] = None

    model_config = ConfigDict(from_attributes=True)

class PortfolioCreate(PortfolioBase):
    user_id: int

class PortfolioRead(PortfolioBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    

class PortfolioUpdate(PortfolioBase):
    name: Optional[str] = None
    description: Optional[str] = None