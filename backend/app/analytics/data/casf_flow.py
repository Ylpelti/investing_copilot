import pandas as pd

def casf_flow(tx_df:pd.DataFrame, prices_ix: pd.Index) -> pd.Series:

    if tx_df.empty:
        return pd.Series(0, index=prices_ix)
    
    df = tx_df.copy()

    df["cash flow"] = df["quantity"] * df["price"]

    df.loc[df["type"] == "BUY", "cash flow"] *= -1

    daily_cf = df.groupby("date")["cash flow"].sum()

    daily_cf = daily_cf.reindex(prices_ix, fill_value=0.0)

    return daily_cf.cumsum()
