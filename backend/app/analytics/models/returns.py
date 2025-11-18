import pandas as pd
import numpy as np

def simple_returns(s: pd.Series) -> pd.Series:
    return s.pct_change().dropna()

def log_returns(s: pd.Series) -> pd.Series:
    return np.log(s / s.shift(1)).dropna()