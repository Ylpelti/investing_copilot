import yfinance as yf
from datetime import datetime, UTC
from sqlalchemy.orm import Session
from app.schemas.stock import StockCreate
from app.crud.stock_crud import StockCrud
import json




def fetch_and_store_stocks(db: Session):
    crud = StockCrud(db)
    #File will be changed to EOD api
    with open("app/json/stock_data.json") as f:
        Helsinki_Tickers = json.load(f)
    for ticker, isin in Helsinki_Tickers.items():
        try: 
            ticker_client = yf.Ticker(ticker)
            stock_data = ticker_client.info
            
        except Exception:
            print('\ndid not fetch data for', ticker, '\n')
            continue
        if 'regularMarketPrice' in stock_data:
            stock = StockCreate(
                ticker=ticker,
                isin=isin,
                name=stock_data.get('shortName', ''),
                close_price=stock_data['regularMarketPrice'],
                updated_at=datetime.now(UTC),
                sector=stock_data.get('sector', '')
            )
            crud.create_stock(stock)
