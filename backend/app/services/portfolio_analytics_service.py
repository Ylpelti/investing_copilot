from app.analytics.engine.portfolio_engine import PortfolioAnalyticsEngine

class PortfolioAnalyticsService:
    def __init__(self, analytics_engine: PortfolioAnalyticsEngine):
        self.analytics_engine = analytics_engine
        

    def calculate_nav(self, txs, db):
        result = self.analytics_engine.compute(txs, db)
        return result.nav
    
    def calculate_simple_ret(self, txs, db):
        result = self.analytics_engine.compute(txs, db)
        return result.simple_ret
