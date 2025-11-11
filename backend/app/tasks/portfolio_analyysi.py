from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio
from app.models.stock_price import StockPrice

TRADING_DAYS_PER_YEAR = 252

@dataclass
class PositionSnapshot:
    stock_id: int
    ticker: Optional[str]
    quantity: float


def _index_to_label(idx: Any) -> str:
    """Convert different index types to an ISO formatted string for JSON output."""
    if isinstance(idx, pd.Timestamp):
        idx = idx.to_pydatetime()
    if isinstance(idx, datetime):
        return idx.date().isoformat()
    if isinstance(idx, date):
        return idx.isoformat()
    return str(idx)


def _safe_float(value: Any) -> Optional[float]:
    """Return a JSON-friendly float, or None for NaN/inf/non-castable values."""
    if value is None:
        return None
    try:
        float_value = float(value)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(float_value):
        return None
    return float_value


def _series_to_records(series: pd.Series, value_key: str) -> List[Dict[str, Any]]:
    """Convert a pandas Series into a list of {date, value} records for the frontend."""
    if series.empty:
        return []
    records: List[Dict[str, Any]] = []
    for idx, value in series.dropna().items():
        value_float = _safe_float(value)
        if value_float is None:
            continue
        records.append(
            {
                "date": _index_to_label(idx),
                value_key: value_float,
            }
        )
    return records

# Loading data

def get_portfolio(db: Session, portfolio_id: int) -> Optional[Portfolio]:
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    return portfolio

def get_positions_map(db: Session, portfolio_id: int) -> Dict[int, PositionSnapshot]:

    pf = get_portfolio(db, portfolio_id)
    if not pf:
        return {}
    mapping: Dict[int, PositionSnapshot] = {}
    for pos in pf.positions:
        ticker = getattr(getattr(pos, "stock", None), "ticker", None)
        mapping[pos.stock_id] = PositionSnapshot(
            stock_id=pos.stock_id,
            ticker=ticker,
            quantity=float(pos.quantity),
        )
    return mapping



def load_prices_df(
    session: Session,
    stock_ids: Iterable[int],
    start: Optional[date] = None,
    end: Optional[date] = None,
    reindex_business_days: bool = True,
    forward_fill: bool = True,
    ) -> pd.DataFrame:
    
    stock_ids = list(stock_ids)
    if not stock_ids:
        return pd.DataFrame()


    q = (
    session.query(StockPrice.stock_id, StockPrice.date, StockPrice.close_price)
    .filter(StockPrice.stock_id.in_(stock_ids))
    )
    if start is not None:
        q = q.filter(StockPrice.date >= start)
    if end is not None:
        q = q.filter(StockPrice.date <= end)


    q = q.order_by(StockPrice.date.asc())
    rows = q.all()


    if not rows:
        return pd.DataFrame()


    df = pd.DataFrame(rows, columns=["stock_id", "date", "close"])
    df = df.pivot(index="date", columns="stock_id", values="close").sort_index()


    if reindex_business_days:
        all_days = pd.date_range(start=df.index.min(), end=df.index.max(), freq="B")
        df = df.reindex(all_days)
        df.index = df.index.date #type: ignore

    if forward_fill:
        df = df.ffill()
    return df



# portfolio hinnan muodostus

def portfolio_value_series_from_quanties(prices: pd.DataFrame, quantities: Dict[int, float]) -> pd.Series:
    if prices.empty:
        return pd.Series(dtype=float)
    
    cols = [sid for sid in prices.columns if sid in quantities]
    if not cols:
        return pd.Series(dtype=float)

    sub = prices[cols].copy()
    qty_vec = pd.Series({sid: float(quantities[sid]) for sid in cols})

    values = sub.mul(qty_vec, axis=1).sum(axis=1)
    return values

def portfolio_value_series(
        session: Session,
        portfolio_id: int,
        start: Optional[date] = None,
        end: Optional[date] = None,
) -> pd.Series:
    pos_map = get_positions_map(session, portfolio_id)
    if not pos_map:
        return pd.Series(dtype=float)
    
    stock_ids = list(pos_map.keys())
    prices = load_prices_df(session, stock_ids, start=start, end=end)
    quantities = {sid: snap.quantity for sid, snap in pos_map.items()}
    return portfolio_value_series_from_quanties(prices, quantities)


# tuottojen laskenta

def series_simple_return(s: pd.Series) -> pd.Series:
    return s.pct_change().dropna()

def series_log_return(s: pd.Series) -> pd.Series:
    return np.log(s / s.shift(1)).dropna()

def cumulative_returns(returns: pd.Series) -> pd.Series:
    return (1.0 + returns).cumprod()-1.0

def rolling_volatility(returns: pd.Series, window: int = 21, annualize: bool = True, perioids_per_year: int = TRADING_DAYS_PER_YEAR ) -> pd.Series:
    vol = returns.rolling(window).std()
    if annualize:
        vol = vol * np.sqrt(perioids_per_year)
    return vol

def rolling_sharpe(returns: pd.Series, window: int = 61, rf: float = 0.0, annualize: bool = True, perioids_per_year: int = TRADING_DAYS_PER_YEAR) -> pd.Series:
    excess_ret = returns - rf / perioids_per_year
    sharpe = excess_ret.rolling(window).mean() / excess_ret.rolling(window).std()
    if annualize:
        sharpe = sharpe * np.sqrt(perioids_per_year)
    return sharpe

# Riskimittarit

def volatility(returns: pd.Series, annualize: bool = True, perioids_per_year: int = TRADING_DAYS_PER_YEAR) -> float:
    vol = returns.std()
    if annualize:
        vol = vol * np.sqrt(perioids_per_year)
    return vol

def sharpe_ratio(returns: pd.Series, rf: float = 0.0, annualize: bool = True, perioids_per_year: int = TRADING_DAYS_PER_YEAR) -> float:
    if returns.empty:
        return float('nan')
    excess_ret = returns - rf / perioids_per_year
    mean_excess = excess_ret.mean()
    std_excess = excess_ret.std()

    if std_excess == 0:
        return float('nan')
    sharpe = mean_excess / std_excess

    if annualize:
        sharpe = sharpe * np.sqrt(perioids_per_year)
    return sharpe

def sortino_ratio(returns: pd.Series, rf: float = 0.0, annualize: bool = True, perioids_per_year: int = TRADING_DAYS_PER_YEAR) -> float:
    if returns.empty:
        return float('nan')
    daily_rf = (1+rf)**(1/perioids_per_year)-1
    excess_ret = returns - daily_rf
    mean_excess = excess_ret.mean()
    downside = excess_ret[excess_ret < 0]
    downside_std = downside.std()

    if downside_std == 0 or np.isnan(downside_std):
        return float('nan')
    sortino = mean_excess / downside_std

    if annualize:
        sortino = sortino * np.sqrt(perioids_per_year)
    return sortino

def drawdown_curve(values: pd.Series) -> pd.Series:
    if values.empty:
        return pd.Series(dtype=float)
    cum_max = values.cummax()
    drawdown = values / cum_max - 1.0
    return drawdown

def max_drawdown(values: pd.Series) -> tuple[float, Optional[pd.Timestamp], Optional[pd.Timestamp]]:
    if values.empty:
        return (float('nan'), None, None)
    dd = drawdown_curve(values)
    trough_idx = dd.idxmin()
    max_dd = float(dd.loc[trough_idx])
    peak_idx = values.loc[:trough_idx].idxmax()
    return (max_dd, peak_idx, trough_idx)  # type: ignore

def var_cvar(returns: pd.Series, level: float = 0.95, method: str='historical') -> Tuple[float, float]:
    if returns.empty:
        return (float('nan'), float('nan'))
    a = np.asarray(returns.dropna())
    alpha = 1 - level
    if method == 'gaussian':
        mu, sigma = np.mean(a), np.std(a)
        from scipy.stats import norm
        var = mu + sigma * norm.ppf(alpha)
        cvar = mu - sigma * (norm.pdf(norm.ppf(alpha)) / alpha)
    else:  # historical
        var = np.quantile(a, alpha)
        cvar = a[a <= var].mean() if np.any(a <= var) else float('nan')
    return (float(var), float(cvar))

# verteilu indeksit: alpha ja bheta

def beta_alpha(
    asset_returns: pd.Series,
    benchmark_returns: pd.Series,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
    ) -> Tuple[float, float]:
    """Laskee (beta, annualisoitu alpha) CAPM-tyyppisesti kovarianssin avulla."""
    df = pd.concat([asset_returns, benchmark_returns], axis=1).dropna()
    if df.shape[0] < 2:
        return float("nan"), float("nan")
    df.columns = ["asset", "bench"]
    cov = df.cov().iloc[0, 1]
    var_b = df["bench"].var()
    if var_b == 0 or np.isnan(var_b):
        return float("nan"), float("nan")
    beta = cov / var_b
    # Jensen's alpha approks. vuositasolle
    daily_alpha = df["asset"].mean() - beta * df["bench"].mean()
    alpha_ann = (1 + daily_alpha) ** periods_per_year - 1
    return float(beta), float(alpha_ann)


def build_dashboard_from_series(
    values: pd.Series,
    rf: float = 0.0,
    benchmark_returns: Optional[pd.Series] = None,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
    rolling_vol_window: int = 21,
    rolling_sharpe_window: int = 61,
) -> Dict[str, Any]:
    """
    Build a frontend-friendly dashboard payload using already fetched portfolio values.

    Args:
        values: Series of portfolio values indexed by date (daily close).
        rf: Annual risk-free rate expressed as a decimal (e.g. 0.01 for 1%).
        benchmark_returns: Optional benchmark return series aligned by date.
        periods_per_year: Trading periods per year, defaults to 252.
        rolling_vol_window: Window size for rolling volatility calculation.
        rolling_sharpe_window: Window size for rolling Sharpe calculation.

    Returns:
        Dictionary containing time-series data and scalar risk/return metrics.
    """
    if values.empty:
        return {
            "value_series": [],
            "return_series": [],
            "cumulative_returns_series": [],
            "drawdown_series": [],
            "rolling_volatility_series": [],
            "rolling_sharpe_series": [],
            "latest_value": None,
            "total_return": None,
            "annualized_return": None,
            "volatility": None,
            "sharpe_ratio": None,
            "sortino_ratio": None,
            "max_drawdown": {"value": None, "start": None, "end": None},
            "var_cvar": {"var": None, "cvar": None},
            "beta_alpha": {"beta": None, "alpha": None},
        }

    values = values.sort_index()
    returns = series_simple_return(values)
    cumulative = cumulative_returns(returns)
    drawdown = drawdown_curve(values)
    rolling_vol = rolling_volatility(
        returns,
        window=rolling_vol_window,
        annualize=True,
        perioids_per_year=periods_per_year,
    )
    rolling_sharp = rolling_sharpe(
        returns,
        window=rolling_sharpe_window,
        rf=rf,
        annualize=True,
        perioids_per_year=periods_per_year,
    )

    total_return = float("nan")
    annualized_return = float("nan")
    if not returns.empty:
        total_return = (1 + returns).prod() - 1
        if values.iloc[0] > 0 and values.iloc[-1] > 0 and len(returns) > 0:
            years_factor = periods_per_year / len(returns)
            try:
                growth = values.iloc[-1] / values.iloc[0]
                if growth > 0:
                    annualized_return = growth ** years_factor - 1
            except ZeroDivisionError:
                annualized_return = float("nan")

    vol_metric = volatility(
        returns,
        annualize=True,
        perioids_per_year=periods_per_year,
    )
    sharpe_metric = sharpe_ratio(
        returns,
        rf=rf,
        annualize=True,
        perioids_per_year=periods_per_year,
    )
    sortino_metric = sortino_ratio(
        returns,
        rf=rf,
        annualize=True,
        perioids_per_year=periods_per_year,
    )
    dd_value, dd_start, dd_end = max_drawdown(values)
    var_metric, cvar_metric = var_cvar(returns)

    beta_metric = float("nan")
    alpha_metric = float("nan")
    if benchmark_returns is not None:
        aligned = pd.concat([returns, benchmark_returns], axis=1, join="inner").dropna()
        if not aligned.empty:
            beta_metric, alpha_metric = beta_alpha(
                aligned.iloc[:, 0],
                aligned.iloc[:, 1],
                periods_per_year=periods_per_year,
            )

    dashboard = {
        "value_series": _series_to_records(values, "value"),
        "return_series": _series_to_records(returns, "return"),
        "cumulative_returns_series": _series_to_records(cumulative, "cumulative_return"),
        "drawdown_series": _series_to_records(drawdown, "drawdown"),
        "rolling_volatility_series": _series_to_records(
            rolling_vol.dropna(), "rolling_volatility"
        ),
        "rolling_sharpe_series": _series_to_records(
            rolling_sharp.dropna(), "rolling_sharpe"
        ),
        "latest_value": _safe_float(values.iloc[-1]),
        "total_return": _safe_float(total_return),
        "annualized_return": _safe_float(annualized_return),
        "volatility": _safe_float(vol_metric),
        "sharpe_ratio": _safe_float(sharpe_metric),
        "sortino_ratio": _safe_float(sortino_metric),
        "max_drawdown": {
            "value": _safe_float(dd_value),
            "start": _index_to_label(dd_start) if dd_start is not None else None,
            "end": _index_to_label(dd_end) if dd_end is not None else None,
        },
        "var_cvar": {
            "var": _safe_float(var_metric),
            "cvar": _safe_float(cvar_metric),
        },
        "beta_alpha": {
            "beta": _safe_float(beta_metric),
            "alpha": _safe_float(alpha_metric),
        },
    }
    return dashboard


def build_portfolio_dashboard(
    session: Session,
    portfolio_id: int,
    start: Optional[date] = None,
    end: Optional[date] = None,
    rf: float = 0.0,
    benchmark_returns: Optional[pd.Series] = None,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
    rolling_vol_window: int = 21,
    rolling_sharpe_window: int = 61,
) -> Dict[str, Any]:
    """
    Convenience wrapper to construct dashboard data directly from the database.
    """
    values = portfolio_value_series(
        session,
        portfolio_id,
        start=start,
        end=end,
    )
    return build_dashboard_from_series(
        values,
        rf=rf,
        benchmark_returns=benchmark_returns,
        periods_per_year=periods_per_year,
        rolling_vol_window=rolling_vol_window,
        rolling_sharpe_window=rolling_sharpe_window,
    )
