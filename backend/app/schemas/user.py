from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional, Annotated

class UserBase(BaseModel):
    username: Annotated[str, Field(min_length=5, max_length=20)]
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):

    password: Annotated[str, Field(min_length=8, max_length=20)]

class UserRead(UserBase):
    id: int
    


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

