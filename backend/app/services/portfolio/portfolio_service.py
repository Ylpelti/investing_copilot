from app.crud.portfolio_crud import PortfolioCrud
from app.core.errors.exceptions import NotFound, Forbidden, BadRequest
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate
from app.dto.portfolio_dto import PortfolioInternal
from app.crud.position_crud import PositionCrud
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.schemas.positio import PositionRead
from app.models.positio import Position

class PortfolioService:
    def __init__(
            self,
            db: Session,
            current_user_id: int,
            portfolio_repo: PortfolioCrud,
            position_repo: PositionCrud):
        
        self.db = db
        self.current_user_id = current_user_id
        self.portfolio_repo = portfolio_repo
        self.position_repo = position_repo
    
    def get_owned_portfolio_or_404(self, portfolio_id: int):
        portfolio = self.portfolio_repo.get_by_id(portfolio_id)
        if not portfolio:
            raise NotFound(message="Portfolio not found")
        if portfolio.user_id != self.current_user_id:
            raise Forbidden(message="No access to portfolio")
        return portfolio
    
    def create_portfolio(self, data: PortfolioCreate):
        internal = PortfolioInternal(
            name = data.name,
            description= data.description,
            user_id=self.current_user_id
        )
        portfolio = self.portfolio_repo.create(internal)
        self.db.commit()
        self.db.refresh(portfolio)
        return portfolio
    
    def update_portfolio(self, portfolio_data: PortfolioUpdate, portfolio_id: int):
        portfolio = self.get_owned_portfolio_or_404(portfolio_id)
        data = portfolio_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(portfolio, key, value)
        try:
            self.db.commit()
            self.db.refresh(portfolio)
        except IntegrityError:
            self.db.rollback()
            raise BadRequest(message="Invalid input data")
        except Exception:
            self.db.rollback()
            raise
        return portfolio
        

    def get_user_owned_portfolios(self):
       return self.portfolio_repo.list_by_user_id(self.current_user_id)
        
    def delete_portfolio(self, portfolio_id: int):
        portfolio = self.get_owned_portfolio_or_404(portfolio_id)
        self.portfolio_repo.delete(portfolio)
        try:
            self.db.commit()
        except:
            self.db.rollback()
            raise

    def get_portfolio_positions(self, portfolio_id: int):
        portfolio = self.get_owned_portfolio_or_404(portfolio_id)
        return self.position_repo.list_by_portfolio_id(portfolio.id)
    
    def get_portfolio_positions_read(self, portfolio_id: int) -> list[PositionRead]:
        portfolio = self.get_owned_portfolio_or_404(portfolio_id)
        positions = self.position_repo.list_by_portfolio_id(portfolio.id)
        return [self._position_to_read(p) for p in positions]


    def _position_to_read(self, position: Position) -> PositionRead:
        if position.stock is None:
            raise BadRequest(message="Position has not loaded stock relationship")
        return PositionRead(
            symbol=position.stock.ticker,
            quantity=position.quantity,
            portfolio_id=position.portfolio_id,
            stock_id=position.stock_id,
            buy_price=position.buy_price,
            id=position.id
        )