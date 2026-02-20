from fastapi import Depends
from app.security.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from sqlalchemy.orm import Session
from app.crud.transaction_crud import TransactionCrud
from app.services.transaction.transaction_service import TransactionService
from app.services.position.dependency import get_position_service
from app.services.position.position_service import PositionService
from app.services.portfolio.dependencies import get_portfolio_services
from app.services.portfolio.portfolio_service import PortfolioService
from app.services.stocks.dependencies import get_stock_service
from app.services.stocks.stock_service import StockService

def get_transaction_service(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        position_service: PositionService = Depends(get_position_service),
        portfolio_service: PortfolioService = Depends(get_portfolio_services),
        stock_service: StockService = Depends(get_stock_service),
):
    tx_repo = TransactionCrud(db)
    return TransactionService(
        tx_repo,
        position_service,
        portfolio_service,
        stock_service,
        current_user.id)