from app.crud.stock_prices_crud import StockPriceCrud
from app.models.transaction import PortfolioTransaction
import pandas as pd
from typing import List

def prices_to_df(db, txs: List[PortfolioTransaction], forward_fill: bool = True) -> pd.DataFrame:
    prices = []
    crud = StockPriceCrud(db)
    stock_ids = list({tx.stock_id for tx in txs})

    start_date = min(tx.timestamp.date() for tx in txs)
    end_date = max(tx.timestamp.date() for tx in txs)

    print(f"[DEBUG] stock_ids: {stock_ids}")
    print(f"[DEBUG] date range: {start_date} → {end_date}")

    prices = crud.read_prices_bu_stock_ids_and_date(stock_ids, start_date, end_date)

    if prices:
        print(f"[DEBUG] type(prices[0]): {type(prices[0])}")
        print(f"[DEBUG] dir(prices[0]) -> first 10 attrs: {dir(prices[0])[:10]}")
        if hasattr(prices[0], "__dict__"):
            print(f"[DEBUG] sample object dict: {prices[0].__dict__}")
        else:
            print(f"[DEBUG] sample row: {prices[0]}")

    df = pd.DataFrame([
        {"date":p.date, "stock_id": p.stock_id, "close": p.close_price} for p in prices
    ])

    df = df.sort_values(by=["stock_id", "date"]).reset_index(drop=True)

    df = df.pivot(index="date", columns="stock_id", values="close").sort_index()

    

    df.index = pd.to_datetime(df.index)
    return df


