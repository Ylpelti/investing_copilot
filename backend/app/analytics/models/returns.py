import pandas as pd
import numpy as np

def simple_returns(NAV_r: pd.Series, external_cash:pd.Series) -> pd.Series:
    V_t = NAV_r.copy()
    V_t_1 = V_t.shift(1)
    
    r_raw_t = (V_t - V_t_1-external_cash) / V_t_1


    return r_raw_t.dropna()

def cumulative_returns(simple_ret: pd.Series) -> pd.Series:
    R_c = (simple_ret + 1).cumprod() - 1
    return R_c

def log_returns(r_raw_t: pd.Series) -> pd.Series: 
    return (1+r_raw_t).apply(np.log)
    