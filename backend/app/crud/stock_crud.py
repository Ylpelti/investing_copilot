from datetime import datetime
from sqlalchemy.orm import Session

from app.models.stock import Stock
from app.schemas.stock import StockCreate
from fastapi import HTTPException

def create_stock(db: Session, stock: StockCreate) -> Stock:
    existing = db.query(Stock).filter(Stock.ticker == stock.ticker).first()
    if existing:
        updated = False
        if stock.isin and not existing.isin:
            existing.isin = stock.isin
            updated = True
        if stock.name and stock.name != existing.name:
            existing.name = stock.name
            updated = True
        if stock.sector and stock.sector != existing.sector:
            existing.sector = stock.sector
            updated = True
        if stock.close_price and stock.close_price != existing.close_price:
            existing.close_price = stock.close_price
            updated = True
        if stock.updated_at:
            existing.updated_at = stock.updated_at
            updated = True

        if updated:
            db.add(existing)
            db.commit()
            db.refresh(existing)
        else:
            print("Stock already exists in the database.")
        return existing

    db_stock = Stock(
        ticker=stock.ticker,
        name=stock.name,
        isin=stock.isin,
        close_price=stock.close_price,
        updated_at=stock.updated_at or datetime.utcnow(),
        sector=stock.sector,
    )
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def get_stock(db: Session, stock_id: int):
    stock =  db.get(Stock, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock
        

def get_stock_by_isin(db: Session, isin:str):
    stock = db.query(Stock).filter(Stock.isin == isin).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found with that ISIN")

    return stock
