from app.crud.position_crud import PositionCrud
from app.models.transaction import PortfolioTransaction, TransactionType
from app.models.positio import Position
from app.core.errors.exceptions import BadRequest

class PositionService:
    def __init__(self, position_repo: PositionCrud, current_user_id: int):
        self.position_repo = position_repo
        self.current_user_id = current_user_id
    

    def apply_transaction(self, tx:PortfolioTransaction):
        position = self.position_repo.get_by_portfolio_and_stock(tx.portfolio_id, tx.stock_id)
        handlers = {

        }

        if tx.type == TransactionType.BUY:
            self._apply_buy(position, tx)
        elif tx.type == TransactionType.SELL and position:
            self._apply_sell(position, tx)
        else:
            raise BadRequest(message="invalid transaction type")


        
        
    def _apply_buy(self, position: Position | None, tx:PortfolioTransaction):
        if position:
            new_total_quantity = position.quantity + tx.quantity
            new_avg_price = (
                (position.quantity * position.buy_price) + (tx.quantity * tx.price) #type: ignore
            ) / new_total_quantity

            position.quantity, position.buy_price = new_total_quantity, new_avg_price

    def _apply_sell(self, position: Position, tx:PortfolioTransaction):
        
        if tx.quantity > position.quantity:
            raise BadRequest(message="Cannot sell more than you own")
        

        
