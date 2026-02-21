from app.crud.base_crud import BaseCrud
import logging
from app.schemas.transactions import TransactionCreate, TransactionRead
from app.models.transaction import PortfolioTransaction, TransactionType
from app.models.positio import Position
from app.core.errors.exceptions import NotFound, BadRequest, Forbidden
from datetime import datetime
from app.crud.portfolio_crud import PortfolioCrud
from app.crud.position_crud import PositionCrud
from app.models.transaction import PortfolioTransaction
from sqlalchemy.exc import IntegrityError
from app.crud.stock_crud import StockCrud


class TransactionCrud(BaseCrud):
    model = PortfolioTransaction

    def add(self, tx: PortfolioTransaction):
        return self.db.add(tx)

    def get_by_portfolio(self, portfolio_id: int) -> list[PortfolioTransaction]:
        return (
            self.db.query(PortfolioTransaction)
            .filter(
                PortfolioTransaction.portfolio_id == portfolio_id)
                .order_by(PortfolioTransaction.timestamp.descU())
                .all()
        )

    def get_portfolio_transactions(self, portfolio_id:int, current_user_id:int) -> list[PortfolioTransaction]:
        portfolio_crud = PortfolioCrud(self.db)
        portfolio = portfolio_crud.get_owned_portfolio(portfolio_id, current_user_id)

        return(
            self.db.query(PortfolioTransaction)
            .filter(PortfolioTransaction.portfolio_id == portfolio.id)
            .order_by(PortfolioTransaction.timestamp.desc())
            .all()
        )


        
        
       

  
