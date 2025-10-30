from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.crud.user_crud import UserCrud
from app.core.errors.exceptions import AppError


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_db)):
    crud = UserCrud(session)
    try:
        db_user = crud.create_user(user)
    except AppError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    return db_user

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_db)):
    crud = UserCrud(session)
    user = crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 

#@router.get("/", response_model=list[UserRead])
#def read_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_db)):
#    users = session.query(User).offset(skip).limit(limit).all()
#    return users


