from app.crud.transaction_crud import TransactionCrud
from app.models.transaction import PortfolioTransaction
import pandas as pd


def transaction_to_df(tx: list[PortfolioTransaction]) -> pd.DataFrame:
    if not tx:
        return pd.DataFrame(columns=["date", "stock_id", "quantity", "price", "type"])


        
    tx_df = pd.DataFrame([{
        "date": t.timestamp,
        "stock_id": t.stock_id,
        "quantity": float(t.quantity),
        "price": float(t.price),
        "type": t.type,
    } for t in tx])

    tx_df["date"] = pd.to_datetime(tx_df["date"])
    tx_df = tx_df.sort_values("date").reset_index(drop=True)
    return tx_df
