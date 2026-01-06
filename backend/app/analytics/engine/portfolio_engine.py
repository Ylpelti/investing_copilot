from app.analytics.engine.base_engine import BaseAnalyticsEngine
from app.analytics.data.transaction_data import transaction_to_df
from app.analytics.data.prices import prices_to_df
from app.analytics.data.holdings import build_holdings_df
from app.analytics.portfolio.NAV_r import build_NAV_r
from app.analytics.models.returns import simple_returns, cumulative_returns
from app.analytics.models.risks import drawdown_curve, max_drawdown, volatility, var_cvar
from app.analytics.utils.series_to_records import series_to_records
import matplotlib.pyplot as plt
from app.analytics.models.performance import sharpe_ratio

from app.analytics.data.market_value import market_value

from app.analytics.data.cash_flow_internal import build_C_t

class PortfolioAnalyticsEngine(BaseAnalyticsEngine):

    def __init__(self, config):
        super().__init__(config)

    def compute(self, tx, db):
        tx_df, prices_df, holdings_df, NAV_r, portfolio_returns, R_c, internal_cash, external_cash = self.build_core_series(tx, db)
        
        #risk = self.compute_risk_metrics(portfolio_value_series, portfolio_returns)

        return tx_df, prices_df, holdings_df, NAV_r, portfolio_returns, 

        
    def build_core_series(self, tx, db):
        tx_df = self.load_tx_df(tx)
        prices_df = self.load_prices_df(db, tx)
        holdings_df = self.compute_holdings_df(tx_df, prices_df)
        internal_cash, external_cf = self.compute_C_internal(tx_df, prices_df)
        MV = self.compute_market_value(holdings_df, prices_df)
        NAV_r= self.compute_NAV_r(MV, internal_cash)
        portfolio_returns = self.compute_portfolio_returns(NAV_r, external_cf)
        
        R_c = self.compute_cumulative_returns(portfolio_returns)
        
        
        return tx_df, prices_df, holdings_df, NAV_r, portfolio_returns, R_c, internal_cash, external_cf
    
    def build_return_series(self, tx_db, txs):
        pass


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
    
    def compute_cumulative_returns(self, returns):
        return cumulative_returns(returns)
    
    def compute_market_value(self, holdings_df, prices_df):
        return market_value(holdings_df, prices_df)
    
    def compute_C_internal(self, tx_df, prices_df):
        return build_C_t(tx_df, prices_df)
    
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
    
if __name__ == "__main__":
    from app.db.session import SessionLocal
    from datetime import datetime
    from types import SimpleNamespace
    import matplotlib.pyplot as plt
    from app.analytics.engine.config import EngineConfig

    db = SessionLocal()
    config = EngineConfig()

    txs = [

    # ---- INITIAL INVESTMENT (~ €9,000) ----
    SimpleNamespace(stock_id=1, timestamp=datetime(2024, 8, 1), quantity=500, price=3.50, type="BUY"),      # €1750
    SimpleNamespace(stock_id=2, timestamp=datetime(2024, 8, 1), quantity=150, price=19.00, type="BUY"),     # €2850
    SimpleNamespace(stock_id=3, timestamp=datetime(2024, 8, 1), quantity=80,  price=17.00, type="BUY"),     # €1360
    # Total initial exposure: ~ €5960

    # ---- FOLLOW-UP BUYS (~ €3,000) ----
    SimpleNamespace(stock_id=1, timestamp=datetime(2024, 9, 5), quantity=200, price=3.60, type="BUY"),      # €720
    SimpleNamespace(stock_id=3, timestamp=datetime(2024, 9, 20), quantity=60,  price=17.20, type="BUY"),    # €1032
    SimpleNamespace(stock_id=2, timestamp=datetime(2024, 10, 10), quantity=70, price=19.30, type="BUY"),    # €1351
    # Running total exposure: ~ €9,000

    # ---- MID-YEAR REBALANCING / PROFIT TAKING ----
    SimpleNamespace(stock_id=3, timestamp=datetime(2024, 12, 15), quantity=40, price=18.00, type="SELL"),   # €720
    SimpleNamespace(stock_id=1, timestamp=datetime(2025, 1, 20), quantity=150, price=4.10, type="SELL"),    # €615
    # Portfolio stays healthy; cash gets reduced negativity

    # ---- NEW CONTRIBUTION (~ €2k invested gradually) ----
    SimpleNamespace(stock_id=2, timestamp=datetime(2025, 2, 10), quantity=50, price=19.20, type="BUY"),     # €960
    SimpleNamespace(stock_id=1, timestamp=datetime(2025, 2, 25), quantity=120, price=4.30, type="BUY"),     # €516
    SimpleNamespace(stock_id=3, timestamp=datetime(2025, 3, 5),  quantity=30, price=17.50, type="BUY"),     # €525

    # ---- LIGHT TRIMMING (taking profits or reducing exposure) ----
    SimpleNamespace(stock_id=3, timestamp=datetime(2025, 4, 12), quantity=30, price=18.20, type="SELL"),     # €546
    SimpleNamespace(stock_id=2, timestamp=datetime(2025, 4, 25), quantity=40, price=19.95, type="SELL"),     # €798

    # ---- FINAL SMALL ADJUSTMENT ----
    SimpleNamespace(stock_id=1, timestamp=datetime(2025, 5, 10), quantity=80, price=4.40, type="BUY"),       # €352
]



    engine = PortfolioAnalyticsEngine(config)

    # --- RUN ANALYTICS ---
    tx_df, prices_df, holdings_df, NAV_r,  port_returns = engine.compute(txs, db)

    print("\n=== Transactions df ===")
    print(tx_df)

    print("POrtfolio series \n")
    print(NAV_r.to_string())

    print("\n=== prices df ===")
    print(prices_df)

    print("\n=== Holdings df ===")
    print(holdings_df)


    print("\n=== SIMPLE RETURNS ===")
    print(port_returns)

    #print("\n=== PERFORMANCE RETURNS (CF-adjusted) ===")
    #print(perf_returns)


    tx_df2, prices_df2, holdings_df2, pv_series, simple_ret, R_c, internal_cash, external_cash = engine.build_core_series(txs, db)

    

    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # 1. Portfolio Value Over Time
    axs[0].plot(NAV_r.index, NAV_r, label="NAV", color="blue")
    axs[0].set_title("NAV")
    axs[0].set_ylabel("Value")
    axs[0].grid(True, alpha=0.3)
    axs[0].legend()

    # 2. Simple Daily Returns
    axs[1].plot(simple_ret.index, simple_ret, label="Simple Daily Returns", color="green")
    axs[1].axhline(0, color="black", linewidth=0.8)
    axs[1].set_title("Daily Returns")
    axs[1].set_ylabel("Return (%)")
    axs[1].grid(True, alpha=0.3)
    axs[1].legend()

    # 3. Cash-Flow Adjusted Performance Returns
    axs[2].plot(external_cash.index, external_cash, label="NAV shifted", color="purple")
    axs[2].axhline(0, color="black", linewidth=0.8)
    axs[2].set_title("Portvolio value")
    axs[2].set_ylabel("Value (€)")
    axs[2].grid(True, alpha=0.3)
    axs[2].legend()

    plt.tight_layout()
    plt.show()