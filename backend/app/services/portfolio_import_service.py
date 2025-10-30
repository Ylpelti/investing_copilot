
import pandas as pd
from typing import IO, Any
import app.crud.position_crud
import app.crud.stock_crud
from app.schemas.positio import PositionCreate





def parse_csv(file: IO[str], portfolio_id: int, db):
    df = pd.read_csv(file, encoding='utf-16', sep='\t', decimal=',')
    for _,row in df.iterrows():
        quantity = row['Määrä']
        isin = row['ISIN']
        buy_price = row["Hankinta-arvo (Noteerausvaluutta)"]
        position = normalize_position(isin, quantity, buy_price, db, portfolio_id)
        if not position:
            continue
        app.crud.position_crud.create_position(db, position)        
        

def normalize_position(isin:str, quantity: int, buy_price: int, db, portfolio_id):
    stock = app.crud.stock_crud.get_stock_by_isin(db, isin)
    if not stock:
        print('stock not found with that isin')
        return None
    
    return PositionCreate(
        symbol=stock.ticker,
        quantity=quantity,
        portfolio_id=portfolio_id,
        stock_id=stock.id,
        buy_price=buy_price
    )