from app.analytics.engine.portfolio_engine import BaseAnalyticsEngine
from app.ai.services.ai_explainer import AiExplainerService

class PortfolioExplanationService:
    def __init__(self, analytics_engine: BaseAnalyticsEngine, ai_explainer: AiExplainerService):
        self.analytics_engine = analytics_engine
        self.ai_explainer = ai_explainer

    def explain_portfolio(self, txs, db):
        analytics_results = self.analytics_engine.compute(txs, db)
        return self.ai_explainer.explain(analytics_results, kind="portfolio_summary")