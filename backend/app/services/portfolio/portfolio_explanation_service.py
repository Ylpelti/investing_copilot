from app.analytics.engine.portfolio_engine import BaseAnalyticsEngine
from app.ai.services.ai_explainer import AiExplainerService
from sqlalchemy.orm import Session
from app.services.transaction.transaction_service import TransactionService

class PortfolioExplanationService:
    def __init__(
            self,
            analytics_engine: BaseAnalyticsEngine,
            ai_explainer: AiExplainerService,
            db: Session,
            tx_service: TransactionService
            ):
        self.analytics_engine = analytics_engine
        self.ai_explainer = ai_explainer
        self.db = db
        self.tx_service = tx_service

    def explain_portfolio(self, portfolio_id: int):
        txs = self.tx_service.get_portfolio_transactions(portfolio_id) 
        result = self.analytics_engine.compute(txs, self.db)
        payload = {
            "nav": result.nav,
            "simple return": result.simple_ret,
            "cumumulative returns": result.cum_ret,
            "logarithmic returns": result.log_ret,
            "risk": result.risk
        }
        return self.ai_explainer.explain(payload, kind="portfolio_summary")