from app.crud.stock_prices_crud import StockPriceCrud
from app.models.transaction import PortfolioTransaction
import pandas as pd
from typing import List
from datetime import date

def prices_to_df(db, txs: List[PortfolioTransaction], forward_fill: bool = True) -> pd.DataFrame:
    prices = []
    crud = StockPriceCrud(db)
    stock_ids = list({tx.stock_id for tx in txs})

    start_date = min(tx.timestamp.date() for tx in txs)
    end_date = date.today()

    prices = crud.read_prices_bu_stock_ids_and_date(stock_ids, start_date, end_date)

    df = pd.DataFrame([
        {"date":p.date, "stock_id": p.stock_id, "close": p.close_price} for p in prices
    ])

    df = df.sort_values(by=["stock_id", "date"]).reset_index(drop=True)

    df = df.pivot(index="date", columns="stock_id", values="close").sort_index()

    df.index = pd.to_datetime(df.index)
    return df


