from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi import Depends
from app.services.stocks.stock_service import StockService
from app.services.stocks.stock_price_service import StockPriceService
from app.crud.stock_crud import StockCrud
from app.crud.stock_prices_crud import StockPriceCrud

def get_stock_service(
        db: Session = Depends(get_db)
) -> StockService:
    stock_repo = StockCrud(db)
    return StockService(stock_repo=stock_repo)


def get_stock_price_service(
        db: Session = Depends(get_db)
) -> StockPriceService:
    stock_repo = StockCrud(db)
    stock_price_repo = StockPriceCrud(db)
    return StockPriceService(stock_repo, stock_price_repo)