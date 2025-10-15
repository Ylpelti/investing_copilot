from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    pw_hash: Optional[str] = None

