import pandas as pd

def market_value(holdings_df: pd.DataFrame, prices_df: pd.DataFrame):
    MV_t = (holdings_df * prices_df).sum(axis=1)

    return MV_t