from app.models.positio import Position
from app.schemas.positio import PositionCreate, PositionRead
from sqlalchemy.orm import Session
from app.crud.base_crud import BaseCrud
from app.crud.portfolio_crud import PortfolioCrud
from app.core.errors.exceptions import BadRequest, Forbidden, NotFound
from sqlalchemy.exc import IntegrityError
import logging
from app.models.portfolio import Portfolio
from app.schemas.transactions import TransactionCreate
from app.models.stock import Stock

logger = logging.getLogger(__name__)



class PositionCrud(BaseCrud):
    model = Position



    def get_by_portfolio_and_stock(self, portfolio_id: int, stock_id: int) -> Position | None:
        return (
              self.db.query(Position)
              .filter(
                  Position.portfolio_id == portfolio_id,
                  Position.stock_id == stock_id
              )
              .first()
        )

    def create_position(self, position: Position) -> Position:
        return self.db.add(position)

    def create_or_update_on_buy(self, portfolio_id: int, tx: TransactionCreate, stock: Stock) -> Position:
        position = (
            self.db.query(Position)
            .filter_by(portfolio_id=portfolio_id, stock_id = stock.id)
            .first()
        )

        if position:
            new_total_quantity = position.quantity + tx.quantity
            new_avg_price = (
                (position.quantity * position.buy_price) + (tx.quantity * tx.price)
            ) / new_total_quantity

            logger.debug(
                f"Updating existing position {stock.ticker}: "
                f"old_qty={position.quantity}, new_qty={new_total_quantity}, "
                f"new_avg_price={new_avg_price}"
            )

            position.quantity, position.buy_price = new_total_quantity, new_avg_price

        else:
            position = Position(
                portfolio_id=tx.portfolio_id,
                stock_id=stock.id,
                quantity=tx.quantity,
                buy_price=tx.price,
                symbol=stock.ticker
            )
            self.db.add(position)
            
            logger.debug(f"Created new position for {stock.ticker} in portfolio {tx.portfolio_id}")
        try:
            self.db.flush()
        except IntegrityError:
            self.db.rollback()
            raise BadRequest(message="Integrity error while updating/creating position.")

        return position


    def update_position_on_sell(self, portfolio_id: int, tx: TransactionCreate, stock: Stock) -> Position:
        position = (
            self.db.query(Position)
            .filter_by(portfolio_id=portfolio_id, stock_id = stock.id)
            .first()
        )

        if not position:
            raise NotFound(message="Position not found")
        
        if tx.quantity > position.quantity:
            raise BadRequest(message=f"Cannot sell more shares ({tx.quantity}) than owned ({position.quantity})")
        
        position.quantity -= tx.quantity
        logger.debug(
            f"Selling {tx.quantity} {stock.ticker}, remaining quantity={position.quantity}"
        )

        if position.quantity == 0:
            self.db.delete(position)
            logger.debug(f"Position {stock.ticker} removed (quantity 0)")

        self.db.flush()
        return position
    
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
    
    
        
         




