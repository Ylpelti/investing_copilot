from datetime import date, datetime, timedelta, UTC
import jwt
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = 'supersecretkey'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def now_utc() -> datetime:
    return datetime.now(UTC)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = now_utc() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = now_utc() + (expires_delta if expires_delta else timedelta(days=7))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)