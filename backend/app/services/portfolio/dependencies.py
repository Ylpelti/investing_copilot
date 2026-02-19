from fastapi import Depends
from app.security.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from sqlalchemy.orm import Session
from app.analytics.engine.portfolio_engine import PortfolioAnalyticsEngine
from app.analytics.engine.config import EngineConfig
from app.ai.services.ai_explainer import AiExplainerService
from app.services.portfolio.portfolio_explanation_service import PortfolioExplanationService
from app.ai.dependencies.dependencies import get_ai_service
from app.services.portfolio.portfolio_import_service import PortfolioImportService
from app.crud.transaction_crud import TransactionCrud
from app.crud.portfolio_crud import PortfolioCrud
from app.crud.stock_crud import StockCrud
from app.services.portfolio.portfolio_analytics_service import PortfolioAnalyticsService
from app.infrastructure.parsers.factory import get_provider_parser
from app.services.portfolio.portfolio_service import PortfolioService
from app.services.stocks.dependencies import get_stock_service

def get_portfolio_explanation_service(
    ai_explainer: AiExplainerService = Depends(get_ai_service),
) -> PortfolioExplanationService:
    analytics_engine = PortfolioAnalyticsEngine(EngineConfig())

    return PortfolioExplanationService(
        analytics_engine=analytics_engine,
        ai_explainer=ai_explainer,
    )

def get_portfolio_analytics_service() -> PortfolioAnalyticsService:
    engine = PortfolioAnalyticsEngine(EngineConfig())
    return PortfolioAnalyticsService(engine) 


def get_portfolio_services(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> PortfolioService:
    portfolio_repo = PortfolioCrud(db)
    return PortfolioService(current_user.id, portfolio_repo)

def get_portfolio_import_service(
        provider: str, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(get_current_user),
        portfolio_service: PortfolioService = Depends(get_portfolio_services), 
        stock_service = Depends(get_stock_service)
        
) -> PortfolioImportService: 
    tx_repo = TransactionCrud(db)
    parser = get_provider_parser(provider)
    return PortfolioImportService(tx_repo, portfolio_service, stock_service, current_user.id, parser)

