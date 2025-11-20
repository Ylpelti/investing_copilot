from app.models.transaction import PortfolioTransaction
from app.analytics.data.transaction_data import transaction_to_df
from app.analytics.data.prices import prices_to_df
from app.analytics.data.holdings import build_holdings_df
from app.analytics.portfolio.portfolio_value_series import build_portfolio_value_series
from app.analytics.models.returns import simple_returns, log_returns
from app.analytics.models.risks import drawdown_curve, max_drawdown, volatility, var_cvar
from app.analytics.utils.series_to_records import series_to_records
import matplotlib.pyplot as plt
from app.analytics.engine.config import EngineConfig
from app.analytics.models.performance import sharpe_ratio


def build_dashboard(tx, db, config: EngineConfig): 
    transaction_df = transaction_to_df(tx)
    prices_df = prices_to_df(db, tx)
    holdings_df = build_holdings_df(transaction_df, prices_df)
    portfolio_value_series = build_portfolio_value_series(holdings_df, prices_df)
    returns = simple_returns(portfolio_value_series)
    dd = drawdown_curve(portfolio_value_series)
    rf_daily = config.rf_annual / config.periods_per_year

    # Save raw data for visualization & metrics
    return {
        "raw": {
            "portfolio_value": portfolio_value_series,
            "returns": returns,
            "drawdown": dd,
        },
        "returns": {
            "simple returns": series_to_records(returns),
            "log returns": series_to_records(log_returns(portfolio_value_series)),
        },
        "risk metrics": {
            "drawdown_curve": series_to_records(dd),
            "max drawdown": max_drawdown(portfolio_value_series),
            "volatility": volatility(returns),
            "var cvar": var_cvar(returns),
            "std": float(returns.std())
        },
        
        
    }


def plot_portfolio_dashboard(value_series, returns, drawdown):
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    
    axs[0].plot(value_series.index, value_series, label="Portfolio Value", color="blue")
    axs[0].set_title("Portfolio Value Over Time")
    axs[0].legend()
    
    axs[1].plot(returns.index, returns, color="green", label="Daily Returns")
    axs[1].axhline(0, color="black", linewidth=0.8)
    axs[1].legend()
    
    axs[2].fill_between(drawdown.index, drawdown, 0, color="red", alpha=0.4)
    axs[2].set_title("Drawdown Curve")
    axs[2].legend()
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    from app.db.session import SessionLocal
    from datetime import datetime
    from types import SimpleNamespace

    db = SessionLocal()

    # Example transactions
    txs = [
        SimpleNamespace(stock_id=1, timestamp=datetime(2025, 1, 2), quantity=10, price=190.0, type="BUY"),
        SimpleNamespace(stock_id=1, timestamp=datetime(2025, 1, 8), quantity=5,  price=195.0, type="BUY"),
        SimpleNamespace(stock_id=1, timestamp=datetime(2025, 1, 15), quantity=8, price=200.0, type="SELL"),
        SimpleNamespace(stock_id=2, timestamp=datetime(2025, 1, 3), quantity=4,  price=370.0, type="BUY"),
        SimpleNamespace(stock_id=2, timestamp=datetime(2025, 1, 10), quantity=3, price=380.0, type="BUY"),
        SimpleNamespace(stock_id=2, timestamp=datetime(2025, 1, 22), quantity=2, price=390.0, type="SELL"),
        SimpleNamespace(stock_id=3, timestamp=datetime(2025, 1, 7), quantity=6,  price=250.0, type="BUY"),
        SimpleNamespace(stock_id=3, timestamp=datetime(2025, 1, 9), quantity=4,  price=255.0, type="BUY"),
        SimpleNamespace(stock_id=3, timestamp=datetime(2025, 1, 17), quantity=5, price=260.0, type="SELL"),
        SimpleNamespace(stock_id=3, timestamp=datetime(2025, 1, 24), quantity=3, price=265.0, type="SELL"),
    ]

    

    
