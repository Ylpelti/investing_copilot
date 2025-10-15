from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.positio import Position
from app.db.session import get_db
from app.schemas.positio import PositionCreate, PositionRead, PositionUpdate
from app.crud import position_crud


router = APIRouter(
    prefix="/positions",
    tags=["positions"],
)


@router.post("/", response_model=PositionRead)
def create_position(position: PositionCreate, session: Session = Depends(get_db)):  
    position_crud.create_position(session, position)
    return position

@router.get("/{position_id}", response_model=PositionRead)
def read_position(position_id: int, session: Session = Depends(get_db)):
    position = position_crud.get_position(session, position_id)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position


@router.put("/{position_id}", response_model=PositionRead)
def update_position(position: PositionUpdate, position_id: int, session: Session = Depends(get_db)):
    db_position = position_crud.get_position(session, position_id)
    if not db_position:
        raise HTTPException(status_code=404, detail="Position not found")
    if position.quantity is not None:
        db_position.quantity = position.quantity
    if position.buy_price is not None:
        db_position.buy_price = position.buy_price
    session.commit()
    session.refresh(db_position)
    return db_position

@router.delete("/{position_id}")
def delete_position(position_id: int, session: Session = Depends(get_db)):
    db_position = session.get(Position, position_id)
    if not db_position:
        raise HTTPException(status_code=404, detail="Position not found")
    session.delete(db_position)
    session.commit()
    return {"detail": "Position deleted"}
