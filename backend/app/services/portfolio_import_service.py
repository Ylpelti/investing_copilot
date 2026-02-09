
import pandas as pd
from typing import IO
from app.crud.transaction_crud import TransactionCrud
from app.schemas.transactions import TransactionCreate
from app.crud.stock_crud import StockCrud
from app.core.errors.exceptions import NotFound
from datetime import datetime
from decimal import Decimal
from app.models.transaction import TransactionType







def parse_csv(file: IO[str], portfolio_id: int, db, current_user_id:int):
    crud = TransactionCrud(db)
    df = pd.read_csv(file, encoding='utf-16', sep='\t', decimal=',')
    for _,row in df.iterrows():
        quantity = row['Määrä']
        isin = row['ISIN']
        buy_price = row["Hankinta-arvo (Noteerausvaluutta)"]
        trade_date = pd.to_datetime(row["Hankintapäivä"], format="%d.%m.%Y", errors="coerce")
        transaction = normalize_transaction(isin, quantity, buy_price, trade_date, db, portfolio_id)
        if not transaction:
            continue
        crud.ceate_transaction(transaction, current_user_id)        
        

def normalize_transaction(isin:str, quantity: Decimal, buy_price: Decimal, trade_date:datetime, db, portfolio_id):
    crud = StockCrud(db)
    stock = crud.get_stock_by_isin(isin)
    if not stock:
        raise NotFound(message="Stock not found with that isin")
        
    
    return TransactionCreate(
         portfolio_id=portfolio_id,
         stock_id=stock.id,
         type=TransactionType.BUY,
         quantity=quantity,
         price=buy_price,
         timestamp=trade_date       
    )