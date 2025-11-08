from app.models.positio import Position
from app.schemas.positio import PositionCreate, PositionRead
from sqlalchemy.orm import Session
from app.crud.base_crud import BaseCrud
from app.crud.portfolio_crud import PortfolioCrud
from app.core.errors.exceptions import BadRequest, Forbidden
from sqlalchemy.exc import IntegrityError
import logging
from app.models.portfolio import Portfolio

logger = logging.getLogger(__name__)



class PositionCrud(BaseCrud):
    model = Position

    def create_position(self, position: PositionCreate, current_user_id: int) -> Position:
        portfolio_crud = PortfolioCrud(self.db)
        portfolio = portfolio_crud.get_owned_portfolio(position.portfolio_id, current_user_id)

        db_position = Position(
        portfolio_id=portfolio.id,
        stock_id=position.stock_id,
        quantity=position.quantity,
        buy_price=position.buy_price,
        symbol=position.symbol
        )
        try:
            self.db.add(db_position)
            self.db.commit()
            self.db.refresh(db_position)
        except IntegrityError:
            self.db.rollback()
            raise BadRequest(message="Duplicate stock in this portfolio.")
        except Exception as e:
            self.db.rollback()
            logger.exception("Unexpected error while creating position")
            raise

        return db_position
    
    def get_user_owned_position(self, position_id: int, current_user_id: int) -> Position:
        position = (
            self.db.query(Position)
            .join(Portfolio)
            .filter(Position.id == position_id, Portfolio.user_id == current_user_id)
            .first()
        )
        if not position:
            raise Forbidden(message="You do not have permission to access this position.")
        return position

    def get_portfolio_positions(self, portfolio_id:int, current_user_id: int) -> list[Position]:
        portfolio_crud = PortfolioCrud(self.db)
        portfolio = portfolio_crud.get_owned_portfolio(portfolio_id, current_user_id)
        return portfolio.positions
    
    def delete_position(self, position_id: int, current_user_id: int):
        position = self.get_user_owned_position(position_id, current_user_id)
        self.db.delete(position)
        self.db.commit()
        return True
        
         




