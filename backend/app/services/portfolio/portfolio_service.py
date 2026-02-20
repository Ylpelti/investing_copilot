from app.crud.portfolio_crud import PortfolioCrud
from app.core.errors.exceptions import NotFound
from app.schemas.portfolio import PortfolioCreate
from app.dto.portfolio_dto import PortfolioInternal
from app.crud.position_crud import PositionCrud

class PortfolioService:
    def __init__(
            self,
            current_user_id: int,
            portfolio_repo: PortfolioCrud,
            position_repo: PositionCrud):
        
        self.current_user_id = current_user_id
        self.portfolio_repo = portfolio_repo
        self.position_repo = position_repo
    
    def get_owned_portfolio_or_404(self, portfolio_id):
        portfolio = self.portfolio_repo.get_owned_portfolio(portfolio_id, self.current_user_id)
        if not portfolio:
            raise NotFound(message="Portfolio not found")
        return portfolio
    
    def create_portfolio(self, data: PortfolioCreate):
        portfolio = PortfolioInternal(
            name = data.name,
            description= data.description,
            user_id=self.current_user_id
        )
        return self.portfolio_repo.create_portfolio(portfolio)
    
    def get_user_owned_portfolios(self):
        return self.portfolio_repo.get_user_owned_portfolios(self.current_user_id)
        
    def get_portfolio_positions(self, portfolio_id: int):
        return self.position_repo.get_portfolio_positions(portfolio_id, self.current_user_id)
    
    