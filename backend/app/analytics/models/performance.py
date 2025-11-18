import pandas as pd
import numpy as np

def sharpe_ratio(returns:pd.Series, rf_daily: float, perioids: int = 252, annualize: bool = True) -> float:
    
    if len(returns) < 2:
        return np.nan
    
    excess = returns - rf_daily
    std = excess.std()

    if std == 0 or np.isnan(std):
        return np.nan
    
    sharpe = excess.mean() / std

    if annualize:
        sharpe *= np.sqrt(perioids)
    
    return sharpe