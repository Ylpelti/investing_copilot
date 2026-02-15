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





