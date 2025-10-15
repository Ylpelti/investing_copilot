from sqlalchemy.orm import Session
from app.models.stock import Stock
from app.schemas.stock import StockCreate

def create_stock(db: Session, stock: StockCreate) -> Stock:
    db_stock = Stock(
        ticker=stock.ticker,
        name=stock.name,
        close_price=stock.close_price,
        updated_at=stock.updated_at,
        sector=stock.sector
    )
    if (db.query(Stock).filter(Stock.ticker == stock.ticker).first()):
        print("Stock already exists in the database.")
        return db.query(Stock).filter(Stock.ticker == stock.ticker).first()
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def get_stock(db: Session, stock_id: int):
    return db.get(Stock, stock_id)