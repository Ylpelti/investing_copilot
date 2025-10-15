from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.stock_price import StockPriceCreate, StockPriceRead
from app.crud import stock_prices_crud
from app.models.stock_price import StockPrice


router = APIRouter(
    prefix="/stock_prices",
    tags=["stock_prices"],

    
)

@router.get("/{stock_price_id}", response_model=StockPriceRead)
def read_stock_price(stock_price_id: int, session: Session = Depends(get_db)):
    stock_price = stock_prices_crud.read_stock_price(session, stock_price_id)
    if not stock_price:
        raise HTTPException(status_code=404, detail="Stock price not found")
    return stock_price

@router.get("/by_stock/{stock_id}", response_model=list[StockPriceRead])
def read_stock_prices_by_stock_id(stock_id: int, session: Session = Depends(get_db)):
    stock_prices = stock_prices_crud.read_stock_prices_by_stock_id(session, stock_id)
    return stock_prices

@router.get("/by_ticker/{ticker}", response_model=list[StockPriceRead])
def read_stock_prices_by_ticker(ticker: str, session: Session = Depends(get_db)):
    stock_prices = stock_prices_crud.read_stock_prices_by_ticker(session, ticker)
    return stock_prices

@router.get("/by_date_range/{stock_id}", response_model=list[StockPriceRead])
def read_stock_prices_by_date_range(stock_id: int, start_date: str, end_date: str, session: Session = Depends(get_db)):
    try:
        from datetime import datetime
        start_date_dt = datetime.fromisoformat(start_date).date()
        end_date_dt = datetime.fromisoformat(end_date).date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format (YYYY-MM-DD).")
    if start_date_dt > end_date_dt:
        raise HTTPException(status_code=400, detail="start_date must be before end_date.")

    stock_prices = stock_prices_crud.read_stock_prices_by_date_range(session, stock_id, start_date_dt, end_date_dt)
    return stock_prices

