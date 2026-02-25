import logging
from sqlalchemy.exc import IntegrityError
from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate
from app.crud.base_crud import BaseCrud
from typing import List
from app.core.errors.exceptions import NotFound, Forbidden, BadRequest
from app.dto.portfolio_dto import PortfolioInternal

logger = logging.getLogger(__name__)

class PortfolioCrud(BaseCrud):
    model = Portfolio


    def create(self, portfolio:PortfolioInternal) -> Portfolio:
        db_portfolio = Portfolio(
           name = portfolio.name,
           description=portfolio.description,
           user_id=portfolio.user_id 
        )

        self.db.add(db_portfolio)
        return db_portfolio

    
    
    def get_by_id(self, portfolio_id:int) -> Portfolio | None:
        return (
            self.db.query(Portfolio)
            .filter(Portfolio.id == portfolio_id)
            .first()
        )
    
    def list_by_user_id(self, user_id) -> list[Portfolio]:
        portfolios = (
            self.db.query(Portfolio)
            .filter(Portfolio.user_id == user_id)
            .all()
        )
        return portfolios
    
            
    def delete(self, portfolio: Portfolio) -> None:
        self.db.delete(portfolio)
    
    
        
        


            
        


