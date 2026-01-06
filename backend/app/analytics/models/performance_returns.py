import pandas as pd
import numpy as np

def performance_returns(value_series: pd.Series, cf_series: pd.Series) -> pd.Series:
    V = value_series
    C = cf_series
    dV = V.diff()
    r_perf_t = (dV - C) / V.shift(1)
    r__perf_t = r_perf_t.replace([np.inf, -np.inf], np.nan).dropna()
    return r_perf_t

def cumulative_performance_returns(r_perf: pd.Series) -> pd.Series:
    r = r_perf.fillna(0)
    R_cum = (1+r).cumprod() - 1
    return R_cum