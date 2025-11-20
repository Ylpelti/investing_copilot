import pandas as pd

def build_portfolio_value_series(holdings_df:pd.DataFrame, prices_df:pd.DataFrame, cf:pd.Series) -> pd.Series:

    holdings = (holdings_df * prices_df).sum(axis=1)
    value_series = holdings + cf + 5960

    value_series.name = "portfolio value"

    return value_series