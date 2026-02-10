from dataclasses import dataclass
import pandas as pd

@dataclass
class PortfolioAnalyticsResult:
    nav: pd.Series
    simple_ret: pd.Series
    cum_ret: pd.Series
    log_ret: pd.Series
    risk: dict