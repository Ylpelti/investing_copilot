from app.analytics.engine.portfolio_engine import PortfolioAnalyticsEngine
from app.services.transaction.transaction_service import TransactionService
from sqlalchemy.orm import Session

class PortfolioAnalyticsService:
    def __init__(
            self,
            analytics_engine: PortfolioAnalyticsEngine,
            tx_service: TransactionService,
            db: Session
            ):
        self.analytics_engine = analytics_engine
        self.tx_service = tx_service
        self.db = db
        

    def calculate_nav(self, portfolio_id):
        txs = self.tx_service.get_portfolio_transactions(portfolio_id)
        result = self.analytics_engine.compute(txs, self.db)
        return result.nav
    
    def calculate_simple_ret(self, portfolio_id):
        txs = self.tx_service.get_portfolio_transactions(portfolio_id)
        result = self.analytics_engine.compute(txs, self.db)
        return result.simple_ret
