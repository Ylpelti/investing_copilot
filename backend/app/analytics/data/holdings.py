import pandas as pd


def build_holdings_df(txs_df: pd.DataFrame, prices_df: pd.DataFrame) -> pd.DataFrame:
    tx_df = txs_df.copy()
    tx_df["signed_qty"] = tx_df.apply(
        lambda x: x["quantity"] if x["type"].upper() == "BUY" else -x["quantity"], axis=1
    )
    daily_tx = (
        tx_df.groupby(["date", "stock_id"])["signed_qty"]
        .sum()
        .unstack(fill_value=0)
        .sort_index()
    )

    all_dates = prices_df.index
    daily_tx = daily_tx.reindex(all_dates, fill_value=0)
    holdings_df = daily_tx.cumsum()
    holdings_df = holdings_df.reindex(columns=prices_df.columns, fill_value=0)
    holdings_df.index.name = "date"
    holdings_df.columns.name = "stock_id"
    holdings_df.index = pd.to_datetime(holdings_df.index)
    
    return holdings_df
