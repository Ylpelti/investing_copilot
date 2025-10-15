import yfinance as yf
import pandas as pd
from datetime import datetime 
from sqlalchemy.orm import Session
from app.schemas.stock_price import StockPriceCreate
from app.models.stock_price import StockPrice
from app.models.stock import Stock

def fetch_and_store_stock_prices(session: Session, stock_id: int, ticker: str):
    try:
        stock_data = yf.Ticker(ticker)
        hist = stock_data.history(period="1y")  # Fetch 1 year of historical data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return

    for date,row in hist.iterrows(): #type:ignore
        date: pd.Timestamp
        stock_price = StockPriceCreate(

            stock_id=stock_id,
            date=date.date(),
            open_price=row['Open'],
            high_price=row['High'],
            low_price=row['Low'],
            close_price=row['Close'],
            volume=int(row['Volume']) if not pd.isna(row['Volume']) else 0
        )
        # Check if the record already exists to avoid duplicates
        existing_record = session.query(StockPrice).filter_by(stock_id=stock_id, date=stock_price.date).first()
        if not existing_record:
            db_stock_price = StockPrice(
                stock_id=stock_price.stock_id,
                date=stock_price.date,
                open_price=stock_price.open_price,
                high_price=stock_price.high_price,
                low_price=stock_price.low_price,
                close_price=stock_price.close_price,
                volume=stock_price.volume
            )
            session.add(db_stock_price)
    session.commit()
    
def fetch_and_store_stock_price(session: Session):
    existing_stocks = session.query(Stock).all()
    for stock in existing_stocks:
        fetch_and_store_stock_prices(session, stock.id, stock.ticker)
        print(f"Fetched and stored prices for {stock.ticker}")