import logging
from sqlalchemy.exc import IntegrityError
from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate
from app.crud.base_crud import BaseCrud
from typing import List
from app.core.errors.exceptions import NotFound, Forbidden, BadRequest

logger = logging.getLogger(__name__)

class PortfolioCrud(BaseCrud[Portfolio]):
    model = Portfolio

    def create_portfolio(self, portfolio:PortfolioCreate) -> Portfolio:
        db_portfolio = Portfolio(
           name = portfolio.name,
           description=portfolio.description,
           user_id=portfolio.user_id 
        )
        self.db.add(db_portfolio)
        self.db.commit()
        self.db.refresh(db_portfolio)
        return db_portfolio
    
    def get_owned_portfolio(self, portfolio_id: int, user_id: int) -> Portfolio:
        portfolio = (
            self.db.query(Portfolio)
            .filter(
                Portfolio.id == portfolio_id,
                Portfolio.user_id == user_id
            ).first()
            )
        if not portfolio:
            raise Forbidden(message="No portfolio found")
        
        return portfolio
    
    def get_user_owned_portfolios(self, user_id):
        portfolios = (
            self.db.query(Portfolio)
            .filter(Portfolio.user_id == user_id)
            .all()
        )
        return portfolios
    
    def update_portfolio(self, portfolio_id: int, portfolio_in: PortfolioUpdate, current_user_id: int) -> Portfolio:
        portfolio = self.get_owned_portfolio(portfolio_id=portfolio_id, user_id=current_user_id)
        data = portfolio_in.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(portfolio, key, value)
        try:
            self.db.commit()
            self.db.refresh(portfolio)
        except IntegrityError as e:
            self.db.rollback()
            raise BadRequest(message="Invalid input data") 
        except Exception as e:
            self.db.rollback()
            logger.exception(f"unexpected error updating portfolio {portfolio_id}")
            raise
        return portfolio
            
    def delete_portfolio(self, portfolio_id: int, current_user_id: int):
        portfolio = self.get_owned_portfolio(portfolio_id=portfolio_id, user_id=current_user_id)
        self.delete_by_id(portfolio.id)
        logger.info(f"portofolio with id {portfolio.id} deleted")
        return True


            
        


