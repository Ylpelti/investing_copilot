from app.models.positio import Position
from app.schemas.positio import PositionCreate, PositionRead
from sqlalchemy.orm import Session

def read_positions(db: Session) -> list[Position]:
    return db.query(Position).all()

def create_position(db: Session, position: PositionCreate) -> Position:
    db_position = Position(
        portfolio_id=position.portfolio_id,
        stock_id=position.stock_id,
        quantity=position.quantity,
        buy_price=position.buy_price,
        symbol=position.symbol
        
    )
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

def get_position(db: Session, position_id: int) -> Position | None:
    return db.query(Position).filter(Position.id == position_id).first()


