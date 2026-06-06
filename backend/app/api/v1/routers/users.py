from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.crud.user_crud import UserCrud
from app.core.errors.exceptions import AppError
from app.security.dependencies import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_db)):
    crud = UserCrud(session)
    return crud.create_user(user)

@router.get("/{user_id}", response_model=UserRead)
def read_user(current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    crud = UserCrud(session)
    return crud.get_by_id(current_user.id)

@router.get('/me', response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
    
    

#@router.get("/", response_model=list[UserRead])
#def read_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_db)):
#    users = session.query(User).offset(skip).limit(limit).all()
#    return users


