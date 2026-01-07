import numpy as np
import pandas as pd
import pytest

from app.analytics.data.cash_flow_internal import build_cf_series
from app.analytics.data.holdings import build_holdings_df
from app.analytics.data.market_value import market_value
from app.analytics.data.transaction_data import transaction_to_df
from app.analytics.models.performance import sharpe_ratio
from app.analytics.models.returns import cumulative_returns, log_returns, simple_returns
from app.analytics.models.risks import (
    drawdown_curve,
    max_drawdown,
    var_cvar,
    volatility,
)
from types import SimpleNamespace


def test_simple_returns_with_external_cash():
    nav = pd.Series([100, 110, 120], index=pd.date_range("2024-01-01", periods=3))
    external_cash = pd.Series([0, 5, -10], index=nav.index)

    result = simple_returns(nav, external_cash)

    expected = pd.Series(
        [(110 - 100 - 5) / 100, (120 - 110 + 10) / 110],
        index=nav.index[1:],
    )
    pd.testing.assert_series_equal(result, expected, check_exact=False)

def test_simple_returns_with_weekly_series():
    nav = pd.Series(
        [100, 105, 103],
        index=pd.date_range("2024-01-07", periods=3, freq="W"),
    )
    external_cash = pd.Series([0, 0, 5], index=nav.index)

    result = simple_returns(nav, external_cash)

    expected = pd.Series(
        [(105 - 100 - 0) / 100, (103 - 105 - 5) / 105],
        index=nav.index[1:],
    )
    pd.testing.assert_series_equal(result, expected, check_exact=False)


def test_cumulative_returns_compounds():
    simple_ret = pd.Series([0.1, -0.05], index=[0, 1])
    result = cumulative_returns(simple_ret)

    assert result.iloc[-1] == pytest.approx((1.1 * 0.95) - 1)


def test_log_returns_matches_log1p():
    simple_ret = pd.Series([0.1, -0.05], index=[0, 1])
    result = log_returns(simple_ret)

    expected = pd.Series(np.log1p(simple_ret), index=simple_ret.index)
    pd.testing.assert_series_equal(result, expected, check_exact=False)


def test_drawdown_curve_and_max_drawdown():
    values = pd.Series([100, 120, 90, 130], index=[0, 1, 2, 3])

    dd_curve = drawdown_curve(values)

    assert dd_curve.iloc[2] == pytest.approx(-0.25)
    assert max_drawdown(values) == pytest.approx(-0.25)


def test_volatility_without_annualization():
    returns = pd.Series([0.1, -0.1, 0.2, -0.2], index=[0, 1, 2, 3])

    result = volatility(returns, annualize=False)

    assert result == pytest.approx(returns.std())


def test_var_cvar_matches_quantile_and_tail_mean():
    returns = pd.Series([0.1, -0.1, 0.2, -0.2, 0.0], index=[0, 1, 2, 3, 4])

    var, cvar = var_cvar(returns, level=0.8)
    expected_var = float(np.quantile(returns.dropna(), 0.2))
    expected_cvar = float(returns[returns <= expected_var].mean())

    assert var == pytest.approx(expected_var)
    assert cvar == pytest.approx(expected_cvar)


def test_sharpe_ratio_annualized_and_nan_cases():
    returns = pd.Series([0.01, 0.02, 0.03, 0.04], index=[0, 1, 2, 3])

    result = sharpe_ratio(returns, rf_daily=0.0, perioids=252, annualize=True)
    expected = (returns.mean() / returns.std()) * np.sqrt(252)

    assert result == pytest.approx(expected)
    assert np.isnan(sharpe_ratio(pd.Series([0.01]), rf_daily=0.0))
    assert np.isnan(sharpe_ratio(pd.Series([0.0, 0.0, 0.0]), rf_daily=0.0))


def test_transaction_to_df_sorts_and_handles_empty():
    assert transaction_to_df([]).empty

    txs = [
        SimpleNamespace(
            timestamp=pd.Timestamp("2024-01-05"),
            stock_id=1,
            quantity=10,
            price=5.0,
            type="BUY",
        ),
        SimpleNamespace(
            timestamp=pd.Timestamp("2024-02-10"),
            stock_id=1,
            quantity=4,
            price=6.0,
            type="SELL",
        ),
        SimpleNamespace(
            timestamp=pd.Timestamp("2024-01-20"),
            stock_id=2,
            quantity=3,
            price=12.0,
            type="BUY",
        ),
        SimpleNamespace(
            timestamp=pd.Timestamp("2024-02-25"),
            stock_id=3,
            quantity=2,
            price=20.0,
            type="BUY",
        ),
        SimpleNamespace(
            timestamp=pd.Timestamp("2024-03-15"),
            stock_id=2,
            quantity=1,
            price=13.0,
            type="SELL",
        ),
    ]

    df = transaction_to_df(txs)

    assert list(df["date"]) == [
        pd.Timestamp("2024-01-05"),
        pd.Timestamp("2024-01-20"),
        pd.Timestamp("2024-02-10"),
        pd.Timestamp("2024-02-25"),
        pd.Timestamp("2024-03-15"),
    ]
    assert list(df["stock_id"]) == [1, 2, 1, 3, 2]
    assert list(df["quantity"]) == [10, 3, 4, 2, 1]


def test_build_holdings_df_aligns_to_price_dates():
    tx_df = pd.DataFrame(
        {
            "date": [
                pd.Timestamp("2024-01-05"),
                pd.Timestamp("2024-01-20"),
                pd.Timestamp("2024-02-10"),
                pd.Timestamp("2024-02-25"),
            ],
            "stock_id": [1, 2, 1, 3],
            "quantity": [10, 3, 4, 2],
            "price": [5.0, 12.0, 6.0, 20.0],
            "type": ["BUY", "BUY", "SELL", "BUY"],
        }
    )
    prices_df = pd.DataFrame(
        {
            1: [5.0, 6.0, 6.5, 6.0, 6.2],
            2: [12.0, 12.5, 12.8, 13.0, 13.2],
            3: [20.0, 20.5, 21.0, 21.5, 22.0],
        },
        index=pd.to_datetime(
            [
                "2024-01-05",
                "2024-01-20",
                "2024-02-10",
                "2024-02-25",
                "2024-03-15",
            ]
        ),
    )

    holdings_df = build_holdings_df(tx_df, prices_df)

    expected = pd.DataFrame(
        {1: [10, 10, 6, 6, 6], 2: [0, 3, 3, 3, 3], 3: [0, 0, 0, 2, 2]},
        index=prices_df.index,
    )
    expected.index.name = "date"
    expected.columns.name = "stock_id"
    pd.testing.assert_frame_equal(holdings_df, expected)


def test_market_value_sums_across_holdings():
    holdings_df = pd.DataFrame(
        {1: [2, 3], 2: [1, 0]},
        index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
    )
    prices_df = pd.DataFrame(
        {1: [10.0, 12.0], 2: [5.0, 6.0]},
        index=holdings_df.index,
    )

    result = market_value(holdings_df, prices_df)

    expected = pd.Series([25.0, 36.0], index=holdings_df.index)
    pd.testing.assert_series_equal(result, expected)


def test_build_cf_series_internal_and_external_cashflows():
    tx_df = pd.DataFrame(
        {
            "date": [
                pd.Timestamp("2024-01-02"),
                pd.Timestamp("2024-01-03"),
                pd.Timestamp("2024-01-05"),
            ],
            "stock_id": [1, 1, 1],
            "quantity": [10, 5, 2],
            "price": [10.0, 10.0, 10.0],
            "type": ["BUY", "SELL", "BUY"],
        }
    )
    prices_df = pd.DataFrame(
        {1: [10.0, 11.0, 12.0, 13.0]},
        index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]),
    )

    internal_cash, external_cf = build_cf_series(tx_df, prices_df)

    expected_internal = pd.Series([0.0, 50.0, 50.0, 30.0], index=prices_df.index.normalize())
    expected_external = pd.Series([100.0, 0.0, 0.0, 0.0], index=prices_df.index.normalize())

    pd.testing.assert_series_equal(internal_cash, expected_internal)
    pd.testing.assert_series_equal(external_cf, expected_external)
