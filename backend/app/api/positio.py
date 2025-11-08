from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.positio import Position
from app.db.session import get_db
from app.schemas.positio import PositionCreate, PositionRead, PositionUpdate
from app.crud.position_crud import PositionCrud
from app.models.user import User
from app.security.dependencies import get_current_user

router = APIRouter(
    prefix="/positions",
    tags=["positions"],
)

@router.post("/", response_model=PositionRead)
def create_position(position: PositionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    crud = PositionCrud(db)
    return crud.create_position(position, current_user.id)

@router.get("/{position_id}", response_model=PositionRead)
def read_position(position_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    crud = PositionCrud(db)
    return crud.get_user_owned_position(position_id, current_user.id)

@router.delete("/{position_id}", status_code=204)
def delete_position(position_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    crud = PositionCrud(db)
    return crud.delete_position(position_id, current_user.id)




