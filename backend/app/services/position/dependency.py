from fastapi import Depends
from app.security.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from sqlalchemy.orm import Session
from app.services.position.position_service import PositionService
from app.crud.position_crud import PositionCrud

def get_position_service(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> PositionService:
    position_repo = PositionCrud(db)
    return PositionService(position_repo, current_user.id)