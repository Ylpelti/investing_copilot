from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.crud import user_crud


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_db)):
    db_user = user_crud.create_user(session, user)
    return db_user

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_db)):
    user = user_crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 

@router.get("/", response_model=list[UserRead])
def read_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_db)):
    users = session.query(User).offset(skip).limit(limit).all()
    return users


