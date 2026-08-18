from app.analytics.engine.base_engine import BaseAnalyticsEngine
from app.analytics.data.transaction_data import transaction_to_df
from app.analytics.data.prices import prices_to_df
from app.analytics.data.holdings import build_holdings_df
from app.analytics.portfolio.NAV_r import build_NAV_r
from app.analytics.models.returns import simple_returns, cumulative_returns, log_returns
from app.analytics.models.risks import drawdown_curve, max_drawdown, volatility, var_cvar
from app.analytics.engine.result import PortfolioAnalyticsResult
from app.analytics.models.performance import sharpe_ratio

from app.analytics.data.market_value import market_value

from app.analytics.data.cash_flow_internal import build_cf_series

class PortfolioAnalyticsEngine(BaseAnalyticsEngine):

    def __init__(self, config):
        super().__init__(config)

    def compute(self, tx, db) -> PortfolioAnalyticsResult:
        tx_df, prices_df, holdings_df, NAV_r, simple_returns, cum_returns, log_returns, internal_cash, external_cash = self.build_core_series(tx, db)
        risk = self.compute_risk_metrics(NAV_r, simple_returns)

        return PortfolioAnalyticsResult(
            nav=NAV_r,
            simple_ret=simple_returns,
            cum_ret=cum_returns,
            log_ret=log_returns,
            risk=risk
        )

    def build_core_series(self, tx, db):
        tx_df = self.load_tx_df(tx)
        prices_df = self.load_prices_df(db, tx)
        holdings_df = self.compute_holdings_df(tx_df, prices_df)
        internal_cash, external_cf = self.compute_Cashflows(tx_df, prices_df)
        MV = self.compute_market_value(holdings_df, prices_df)
        NAV_r= self.compute_NAV_r(MV, internal_cash)
        simple_returns = self.compute_portfolio_returns(NAV_r, external_cf)
        cum_returns = self.compute_cumulative_returns(simple_returns)
        log_returns = self.compute_log_returns(simple_returns)
        
        
        
        return tx_df, prices_df, holdings_df, NAV_r, simple_returns, cum_returns, log_returns, internal_cash, external_cf
    
    def compute_risk_metrics(self, NAV_r, returns):
        periods = self.config.periods_per_year
        rf_daily = (1-self.config.rf_annual)**(1/periods)-1
       
        return {
            "drawdown curve": drawdown_curve(NAV_r),
            "max drawdown": max_drawdown(NAV_r),
            "volatility": volatility(returns, periods_per_year=periods),
            "var cvar" : var_cvar(returns),
            "sharpe ratio" : sharpe_ratio(returns, rf_daily, periods)
        }



    def load_tx_df(self, txs):
        return transaction_to_df(txs)
    
    def load_prices_df(self, db, tx):
        return prices_to_df(db, tx)
    
    def compute_holdings_df(self, tx_df, prices_df):
        return build_holdings_df(tx_df, prices_df)
    
    def compute_NAV_r(self, MV, internal_cash):
        return build_NAV_r(MV, internal_cash)
    
    def compute_portfolio_returns(self, Nav_r, external_cash):
        return simple_returns(Nav_r, external_cash)
    
    def compute_cumulative_returns(self, simple_returns):
        return cumulative_returns(simple_returns)
    
    def compute_log_returns(self, simple_returns):
        return log_returns(simple_returns)
    
    def compute_market_value(self, holdings_df, prices_df):
        return market_value(holdings_df, prices_df)
    
    def compute_Cashflows(self, tx_df, prices_df):
        return build_cf_series(tx_df, prices_df)
