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


class TransactionCrud(BaseCrud):
    model = PortfolioTransaction

    def ceate_transaction(self, tx: TransactionCreate, current_user_id: int) -> PortfolioTransaction:
        portfolio_crud = PortfolioCrud(self.db)
        position_crud = PositionCrud(self.db)

        portfolio = portfolio_crud.get_owned_portfolio(tx.portfolio_id, current_user_id)

        if tx.quantity <= 0 or tx.price <= 0:
            raise BadRequest(message="Quantity and price must be positive")
        
        total_value = tx.quantity * tx.price

        db_tx = PortfolioTransaction(
            portfolio_id = portfolio.id,
            stock_id = tx.stock_id,
            symbol = tx.symbol,
            type = tx.type,
            quantity = tx.quantity,
            price = tx.price,
            total_value = total_value,
            
        )

        try:
            self.db.add(db_tx)

            if tx.type == TransactionType.BUY:
                position_crud.create_or_update_on_buy(portfolio.id, tx)
            elif tx.type == TransactionType.SELL:
                position_crud.update_position_on_sell(portfolio.id, tx)

            
            self.db.commit()
            self.db.refresh(db_tx)
        except (NotFound, Forbidden, BadRequest):
    # These are domain/business exceptions — re-raise them unchanged
            self.db.rollback()
            raise

        except IntegrityError:
            self.db.rollback()
            raise BadRequest(message="Transaction Integrity error")
        except Exception as e:
            self.db.rollback()
            raise BadRequest(message=f"Unexpected database error: {str(e)}")
        
        return db_tx
    
    def get_portfolio_transactions(self, portfolio_id:int, current_user_id:int) -> list[PortfolioTransaction]:
        portfolio_crud = PortfolioCrud(self.db)
        portfolio = portfolio_crud.get_owned_portfolio(portfolio_id, current_user_id)

        return(
            self.db.query(PortfolioTransaction)
            .filter(PortfolioTransaction.portfolio_id == portfolio.id)
            .order_by(PortfolioTransaction.timestamp.desc())
            .all()
        )


        
        
       

  
