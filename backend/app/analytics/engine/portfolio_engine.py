from app.analytics.engine.base_engine import BaseAnalyticsEngine
from app.analytics.data.transaction_data import transaction_to_df
from app.analytics.data.prices import prices_to_df
from app.analytics.data.holdings import build_holdings_df
from app.analytics.portfolio.portfolio_value_series import build_portfolio_value_series
from app.analytics.models.returns import simple_returns, log_returns
from app.analytics.models.risks import drawdown_curve, max_drawdown, volatility, var_cvar
from app.analytics.utils.series_to_records import series_to_records
import matplotlib.pyplot as plt
from app.analytics.models.performance import sharpe_ratio

class PortfolioAnalyticsEngine(BaseAnalyticsEngine):

    def __init__(self, config):
        super().__init__(config)

    def compute(self, tx, db):
        tx_df, prices_df, holdings_df, portfolio_value_series, portfolio_returns = self.build_core_series(tx, db)
        
        risk = self.compute_risk_metrics(portfolio_value_series, portfolio_returns)

        
    def build_core_series(self, tx, db):
        tx_df = self.load_tx_df(tx)
        prices_df = self.load_prices_df(db, tx)
        holdings_df = self.compute_holdings_df(tx_df, prices_df)
        portfolio_value_series = self.compute_portfolio_value_series(holdings_df, prices_df)
        portfolio_returns = self.compute_portfolio_returns(portfolio_value_series)
        return tx_df, prices_df, holdings_df, portfolio_value_series, portfolio_returns


    def load_tx_df(self, txs):
        return transaction_to_df(txs)
    
    def load_prices_df(self, db, tx):
        return prices_to_df(db, tx)
    
    def compute_holdings_df(self, tx_df, prices_df):
        return build_holdings_df(tx_df, prices_df)
    
    def compute_portfolio_value_series(self, holdings_df, prices_df):
        return build_portfolio_value_series(holdings_df, prices_df)
    
    def compute_portfolio_returns(self, portfolio_value_series):
        return simple_returns(portfolio_value_series)
    
    def compute_risk_metrics(self, value_series, returns):
        periods = self.config.periods_per_year
        rf_daily = (1-self.config.rf_annual)**(1/periods)-1
       
        return {
            "drawdown curve": drawdown_curve(value_series),
            "max drawdown": max_drawdown(value_series),
            "volatility": volatility(returns, periods_per_year=periods),
            "var cvar" : var_cvar(returns),
            "sharpe ratio" : sharpe_ratio(returns, rf_daily, periods)
        }
    
