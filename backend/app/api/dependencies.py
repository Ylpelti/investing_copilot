from fastapi import Depends
from app.analytics.engine.portfolio_engine import PortfolioAnalyticsEngine
from app.analytics.engine.config import EngineConfig
from app.ai.services.ai_explainer import AiExplainerService
from app.services.portfolio_explanation_service import PortfolioExplanationService
from app.ai.dependencies.dependencies import get_ai_service
from app.services.portfolio_analytics_service import PortfolioAnalyticsService

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
