from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.stock_price import StockPriceCreate, StockPriceRead
from app.crud.stock_prices_crud import StockPriceCrud
from app.models.stock_price import StockPrice

router = APIRouter(
    prefix="/stock_prices",
    tags=["stock_prices"],
)

@router.get("/{stock_price_id}", response_model=StockPriceRead)
def read_stock_price(stock_price_id: int, db: Session = Depends(get_db)):
    crud = StockPriceCrud(db)
    return crud.read_stock_price(stock_price_id)
    
@router.get("/{stock_id}/prices", response_model=list[StockPriceRead])
def read_stock_prices_by_stock_id(stock_id: int, db: Session = Depends(get_db)):
    crud = StockPriceCrud(db)
    return crud.read_stock_prices_by_stock_id(stock_id)
    
@router.get("/{ticker}/prices", response_model=list[StockPriceRead])
def read_stock_prices_by_ticker(ticker: str, db: Session = Depends(get_db)):
    crud = StockPriceCrud(db)
    return crud.read_stock_prices_by_ticker(ticker)
    
@router.get("/by_date_range/{stock_id}", response_model=list[StockPriceRead])
def read_stock_prices_by_date_range(stock_id: int, start_date: str, end_date: str, db: Session = Depends(get_db)):
    crud = StockPriceCrud(db)
    return crud.read_stock_prices_by_date_range(stock_id, start_date, end_date)

@router.get("/by_date/{stock_id}", response_model=StockPriceRead)
def read_stock_price_by_date(stock_id: int, date: str, db: Session = Depends(get_db)):
    crud = StockPriceCrud(db)
    return crud.read_stock_price_by_date(stock_id, date)