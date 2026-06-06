from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db
from app.crud.user_crud import UserCrud
from app.security.hashing import verify_password
from app.security.auth import create_access_token
from app.core.config import settings
from app.schemas.token import TokenResponse

router = APIRouter(prefix="/token", tags=["token"])

@router.post("/", response_model=TokenResponse)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    crud = UserCrud(db)
    user = crud.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.pw_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    expires_in = settings.access_token_expire_minutes * 60
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer", "expires_in": expires_in}

