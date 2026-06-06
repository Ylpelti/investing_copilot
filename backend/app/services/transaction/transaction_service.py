from app.schemas.transactions import TransactionCreate
from app.crud.transaction_crud import TransactionCrud
from app.services.position.position_service import PositionService
from app.services.portfolio.portfolio_service import PortfolioService
from app.services.stocks.stock_service import StockService
from app.core.errors.exceptions import NotFound, BadRequest, Forbidden
from app.models.transaction import PortfolioTransaction
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

class TransactionService:
    def __init__(
            self,
            db: Session, 
            tx_repo: TransactionCrud,
            position_service: PositionService,
            portfolio_service: PortfolioService, 
            stock_service: StockService
            ):
        self.db = db
        self.tx_repo = tx_repo
        self.position_service = position_service
        self.portfolio_service = portfolio_service
        self.stock_service = stock_service

    def create_transaction(self, tx: TransactionCreate):
        portfolio = self.portfolio_service.get_owned_portfolio_or_404(tx.portfolio_id)
        stock = self.stock_service.get_stock_by_id_or_404(tx.stock_id)
        if tx.quantity <= 0 or tx.price <= 0:
            raise BadRequest(message="Quantity and price must be positive")
        
        total_value = tx.quantity * tx.price

        db_tx = PortfolioTransaction(
            portfolio_id = portfolio.id,
            type = tx.type,
            stock_id = stock.id, 
            quantity = tx.quantity,
            price = tx.price,
            total_value = total_value,
            timestamp = tx.timestamp
        )
        try:
            self.tx_repo.add(db_tx)

            self.position_service.apply_transaction(db_tx)

            self.db.commit()

            self.db.refresh(db_tx)
        except (NotFound, Forbidden, BadRequest):
            self.db.rollback()
            raise 

        except IntegrityError:
            self.db.rollback()
            raise BadRequest(message="Transaction integrity error")
        
        except Exception:
            self.db.rollback()
            raise 
        
        return db_tx
    
    def get_portfolio_transactions(self, portfolio_id: int):
        portfolio = self.portfolio_service.get_owned_portfolio_or_404(portfolio_id)
        return self.tx_repo.get_by_portfolio(portfolio.id)