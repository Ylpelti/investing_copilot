import pandas as pd
import numpy as np

import numpy as np, pandas as pd
def drawdown_curve(values: pd.Series) -> pd.Series:
    cm = values.cummax()
    return values / cm - 1.0

def max_drawdown(values: pd.Series) -> float:
    dd = drawdown_curve(values)
    return float(dd.min())

def volatility(returns: pd.Series, periods_per_year=252, annualize: bool = True) -> float:
    vol = returns.std()
    if annualize:
        vol *= np.sqrt(periods_per_year)
    return vol

def var_cvar(returns: pd.Series, level=0.95):
    alpha = 1 - level
    var = float(np.quantile(returns.dropna(), alpha))
    tail = returns[returns <= var]
    cvar = float(tail.mean()) if len(tail) else float('nan')
    return var, cvar