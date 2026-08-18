from datetime import datetime, timedelta, UTC
import jwt
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token/")

def now_utc() -> datetime:
    return datetime.now(UTC)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    expire = now_utc() + (expires_delta if expires_delta else timedelta(minutes=settings.access_token_expire_minutes))
    payload = {
        **data,
        "exp": expire,
        "type":"access"
               }
    return jwt.encode(payload, settings.secret_key, settings.algorithm)

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    expire = now_utc() + (expires_delta if expires_delta else timedelta(days=settings.refresh_token_expire_days))
    payload = {
        **data,
        "exp": expire,
        "type": "refresh"}
    return jwt.encode(payload, settings.secret_key, settings.algorithm)
