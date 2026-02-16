from app.crud.portfolio_crud import PortfolioCrud
from app.core.errors.exceptions import NotFound
class PortfolioService:
    def __init__(
            self,
            
            current_user_id: int,
            portfolio_repo: PortfolioCrud):
        
        self.current_user_id = current_user_id
        self.portfolio_repo = portfolio_repo
    
    def get_owned_portfolio_or_404(self, portfolio_id):
        portfolio = self.portfolio_repo.get_owned_portfolio(portfolio_id, self.current_user_id)
        if not portfolio:
            raise NotFound(message="Portfolio not found")
        return portfolio