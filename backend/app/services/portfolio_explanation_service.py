from app.analytics.engine.portfolio_engine import BaseAnalyticsEngine
from app.ai.services.ai_explainer import AiExplainerService

class PortfolioExplanationService:
    def __init__(self, analytics_engine: BaseAnalyticsEngine, ai_explainer: AiExplainerService):
        self.analytics_engine = analytics_engine
        self.ai_explainer = ai_explainer

    def explain_portfolio(self, txs, db):
        result = self.analytics_engine.compute(txs, db)
        payload = {
            "nav": result.nav,
            "simple return": result.simple_ret,
            "cumumulative returns": result.cum_ret,
            "logarithmic returns": result.log_ret,
            "risks": result.risk
        }
        return self.ai_explainer.explain(payload, kind="portfolio_summary")