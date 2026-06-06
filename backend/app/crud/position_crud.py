from app.models.positio import Position
from app.crud.base_crud import BaseCrud

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
    
    def list_by_portfolio_id(self, portfolio_id: int) -> list[Position]:
        return (
            self.db.query(Position)
            .filter(Position.portfolio_id == portfolio_id)
            .order_by(Position.created_at.desc())
            .all()
        )

    def add(self, position: Position) -> None:
        self.db.add(position)
    
    def delete(self, position:Position) -> None:
        self.db.delete(position) 

    
    
        
         




