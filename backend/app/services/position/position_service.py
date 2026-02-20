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
            TransactionType.BUY: self._apply_buy,
            TransactionType.SELL: self._apply_sell
        }

        handler = handlers.get(tx.type)
        if not handler:
            raise BadRequest(message="invalid transaction type")
        handler(position, tx)



        
        
    def _apply_buy(self, position: Position | None, tx:PortfolioTransaction):
        if position:
            new_total_quantity = position.quantity + tx.quantity
            new_avg_price = (
                (position.quantity * position.buy_price) + (tx.quantity * tx.price) #type: ignore
            ) / new_total_quantity

            position.quantity, position.buy_price = new_total_quantity, new_avg_price
        else:
            new_position = Position(
                portfolio_id=tx.portfolio_id,
                stock_id=tx.stock_id,
                quantity=tx.quantity,
                buy_price=tx.price,
            )
            self.position_repo.create_position(new_position)

    def _apply_sell(self, position: Position | None, tx:PortfolioTransaction):
        if not position:
            raise BadRequest(message="Can't sell unexisting position")
        
        if tx.quantity > position.quantity:
            raise BadRequest(message="Cannot sell more than you own")
        
        position.quantity -= tx.quantity

        if position.quantity == 0:
            self.position_repo.delete_by_id(position.id)
        
        

        
