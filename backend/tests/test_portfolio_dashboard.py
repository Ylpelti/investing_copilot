import json
import math
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


# Ensure the backend package is importable when tests run from repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.tasks.portfolio_analyysi import (  # noqa: E402
    TRADING_DAYS_PER_YEAR,
    beta_alpha,
    build_dashboard_from_series,
    cumulative_returns,
    drawdown_curve,
    max_drawdown,
    series_log_return,
    series_simple_return,
    sharpe_ratio,
    sortino_ratio,
    var_cvar,
    volatility,
)

try:
    from scipy import stats as scipy_stats
except ImportError:  # pragma: no cover - optional dependency for gaussian VaR
    scipy_stats = None


class PortfolioAnalysisTests(unittest.TestCase):
    def test_series_return_calculations(self) -> None:
        dates = pd.bdate_range("2023-01-02", periods=5)
        prices = pd.Series([100, 101, 103, 102, 105], index=dates)

        simple_returns = series_simple_return(prices)
        expected_simple = pd.Series(
            np.array([101, 103, 102, 105], dtype=float)
            / np.array([100, 101, 103, 102], dtype=float)
            - 1,
            index=dates[1:],
        )

        log_returns = series_log_return(prices)
        expected_log = pd.Series(
            np.log(
                np.array([101, 103, 102, 105], dtype=float)
                / np.array([100, 101, 103, 102], dtype=float)
            ),
            index=dates[1:],
        )

        np.testing.assert_allclose(simple_returns.values, expected_simple.values)
        np.testing.assert_allclose(log_returns.values, expected_log.values)

        cumulative = cumulative_returns(simple_returns)
        expected_cumulative = (1 + expected_simple).cumprod() - 1
        np.testing.assert_allclose(cumulative.values, expected_cumulative.values)

    def test_risk_metrics_match_manual_calculations(self) -> None:
        returns = pd.Series([0.01, -0.02, 0.015, -0.005, 0.007])

        sample_std = returns.std(ddof=1)
        expected_sharpe = returns.mean() / sample_std

        downside = returns[returns < 0]
        downside_std = downside.std(ddof=1)
        expected_sortino = returns.mean() / downside_std

        self.assertTrue(math.isclose(volatility(returns, annualize=False), sample_std))
        self.assertTrue(
            math.isclose(sharpe_ratio(returns, rf=0.0, annualize=False), expected_sharpe)
        )
        self.assertTrue(
            math.isclose(sortino_ratio(returns, rf=0.0, annualize=False), expected_sortino)
        )

    def test_drawdown_metrics_identify_peak_trough(self) -> None:
        dates = pd.bdate_range("2023-01-02", periods=6)
        values = pd.Series([100, 120, 110, 130, 90, 95], index=dates)

        expected_drawdown = values / values.cummax() - 1
        pd.testing.assert_series_equal(drawdown_curve(values), expected_drawdown)

        dd_value, dd_start, dd_end = max_drawdown(values)
        expected_trough = expected_drawdown.idxmin()
        expected_peak = values.loc[:expected_trough].idxmax()

        self.assertTrue(math.isclose(dd_value, expected_drawdown.min()))
        self.assertEqual(dd_start, expected_peak)
        self.assertEqual(dd_end, expected_trough)

    def test_var_cvar_historical(self) -> None:
        returns = pd.Series([-0.04, -0.02, 0.01, 0.015, 0.02, -0.01])
        level = 0.95

        var_hist, cvar_hist = var_cvar(returns, level=level, method="historical")

        expected_var = np.quantile(returns, 1 - level)
        expected_cvar = returns[returns <= expected_var].mean()

        self.assertTrue(math.isclose(var_hist, expected_var))
        self.assertTrue(math.isclose(cvar_hist, expected_cvar))

    @unittest.skipUnless(scipy_stats is not None, "scipy is required for gaussian VaR test")
    def test_var_cvar_gaussian(self) -> None:
        returns = pd.Series([-0.04, -0.02, 0.01, 0.015, 0.02, -0.01])
        level = 0.95

        var_gauss, cvar_gauss = var_cvar(returns, level=level, method="gaussian")

        mu = returns.mean()
        sigma = returns.std(ddof=0)
        alpha = 1 - level
        expected_var_gauss = mu + sigma * scipy_stats.norm.ppf(alpha)
        expected_cvar_gauss = mu - sigma * (scipy_stats.norm.pdf(scipy_stats.norm.ppf(alpha)) / alpha)

        self.assertTrue(math.isclose(var_gauss, expected_var_gauss))
        self.assertTrue(math.isclose(cvar_gauss, expected_cvar_gauss))

    def test_beta_alpha_matches_covariance_formula(self) -> None:
        dates = pd.bdate_range("2023-01-02", periods=5)
        asset_returns = pd.Series([0.01, 0.015, -0.005, 0.02], index=dates[1:])
        benchmark_returns = pd.Series([0.008, 0.01, -0.004, 0.018], index=dates[1:])

        beta, alpha = beta_alpha(
            asset_returns, benchmark_returns, periods_per_year=TRADING_DAYS_PER_YEAR
        )

        df = pd.concat([asset_returns, benchmark_returns], axis=1)
        df.columns = ["asset", "bench"]
        cov = df.cov().iloc[0, 1]
        var_bench = df["bench"].var()
        expected_beta = cov / var_bench
        daily_alpha = df["asset"].mean() - expected_beta * df["bench"].mean()
        expected_alpha = (1 + daily_alpha) ** TRADING_DAYS_PER_YEAR - 1

        self.assertTrue(math.isclose(beta, expected_beta))
        self.assertTrue(math.isclose(alpha, expected_alpha))

    def test_dashboard_from_series_formats_metrics_for_frontend(self) -> None:
        dates = pd.bdate_range("2023-01-02", periods=6)
        values = pd.Series([100, 102, 101, 105, 107, 110], index=dates)
        benchmark_returns = pd.Series([0.009, 0.011, -0.006, 0.013, 0.01], index=dates[1:])

        dashboard = build_dashboard_from_series(
            values,
            rf=0.01,
            benchmark_returns=benchmark_returns,
            periods_per_year=TRADING_DAYS_PER_YEAR,
            rolling_vol_window=2,
            rolling_sharpe_window=2,
        )

        # Debug helper for inspecting the payload during focused runs.
        print(json.dumps(dashboard, indent=2, sort_keys=True))

        self.assertAlmostEqual(dashboard["value_series"][0]["value"], 100.0)
        self.assertEqual(dashboard["value_series"][0]["date"], "2023-01-02")
        self.assertEqual(len(dashboard["return_series"]), len(values) - 1)
        self.assertAlmostEqual(
            dashboard["total_return"], values.iloc[-1] / values.iloc[0] - 1
        )

        dd_value, dd_start, dd_end = max_drawdown(values)
        self.assertAlmostEqual(dashboard["max_drawdown"]["value"], dd_value)
        self.assertEqual(dashboard["max_drawdown"]["start"], dd_start.date().isoformat())
        self.assertEqual(dashboard["max_drawdown"]["end"], dd_end.date().isoformat())

        beta_expected, alpha_expected = beta_alpha(
            series_simple_return(values),
            benchmark_returns,
            periods_per_year=TRADING_DAYS_PER_YEAR,
        )
        self.assertAlmostEqual(dashboard["beta_alpha"]["beta"], beta_expected)
        self.assertAlmostEqual(dashboard["beta_alpha"]["alpha"], alpha_expected)

        self.assertGreater(len(dashboard["rolling_volatility_series"]), 0)
        self.assertGreater(len(dashboard["rolling_sharpe_series"]), 0)

    def test_dashboard_handles_empty_values(self) -> None:
        empty_dashboard = build_dashboard_from_series(pd.Series(dtype=float))

        self.assertEqual(empty_dashboard["value_series"], [])
        self.assertIsNone(empty_dashboard["total_return"])
        self.assertIsNone(empty_dashboard["beta_alpha"]["beta"])
        self.assertIsNone(empty_dashboard["var_cvar"]["var"])


if __name__ == "__main__":
    unittest.main()
