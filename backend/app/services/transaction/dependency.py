from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.portfolio_crud import PortfolioCrud
from app.crud.position_crud import PositionCrud
from app.crud.transaction_crud import TransactionCrud
from app.db.session import get_db
from app.models.user import User
from app.security.dependencies import get_current_user
from app.services.portfolio.portfolio_service import PortfolioService
from app.services.position.dependency import get_position_service
from app.services.position.position_service import PositionService
from app.services.stocks.dependencies import get_stock_service
from app.services.stocks.stock_service import StockService
from app.services.transaction.transaction_service import TransactionService


def get_transaction_service(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    position_service: PositionService = Depends(get_position_service),
    stock_service: StockService = Depends(get_stock_service),
) -> TransactionService:
    tx_repo = TransactionCrud(db)
    portfolio_repo = PortfolioCrud(db)
    position_repo = PositionCrud(db)
    portfolio_service = PortfolioService(db, current_user.id, portfolio_repo, position_repo)
    return TransactionService(
        db,
        tx_repo,
        position_service,
        portfolio_service,
        stock_service,
    )
