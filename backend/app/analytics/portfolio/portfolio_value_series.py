import pandas as pd

def build_portfolio_value_series(holdings_df:pd.DataFrame, prices_df:pd.DataFrame) -> pd.Series:

    value_series = (holdings_df * prices_df).sum(axis=1)
    value_series.name = "portfolio value"

    return value_series