from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from requests import session
from app.models.user import User
from typing import Annotated
from app.security.auth import oauth_scheme
from app.core.config import settings
from app.crud.user_crud import UserCrud
import jwt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.session import  get_db

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth_scheme)) -> User:
    crud = UserCrud(db)
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = crud.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user
