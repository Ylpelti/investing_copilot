from sqlalchemy.orm import Session
from app.models.stock_price import StockPrice
from app.schemas.stock_price import StockPriceRead
from datetime import datetime, date

def read_stock_price(db: Session, stock_price_id: int) -> StockPrice | None:
    return db.query(StockPrice).filter(StockPrice.id == stock_price_id).first()

def read_stock_prices_by_stock_id(db: Session, stock_id: int) -> list[StockPrice]:
    return db.query(StockPrice).filter(StockPrice.stock_id == stock_id).all()

def read_stock_prices_by_ticker(db: Session, ticker: str) -> list[StockPrice]:
    return db.query(StockPrice).join(StockPrice.stock).filter(StockPrice.stock.has(ticker=ticker)).all()

def read_stock_prices_by_date_range(db: Session, stock_id: int, start_date: date, end_date: date) -> list[StockPrice]:
    print(f"Fetching stock prices for stock_id {stock_id} from {start_date} to {end_date}")
    return db.query(StockPrice).filter(
        StockPrice.stock_id == stock_id,
        StockPrice.date >= start_date,
        StockPrice.date <= end_date).all()
