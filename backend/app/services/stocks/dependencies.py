from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi import Depends
from app.services.stocks.stock_service import StockService
from app.services.stocks.stock_price_service import StockPriceService
from app.crud.stock_crud import StockCrud
from app.crud.stock_prices_crud import StockPriceCrud
from app.services.stocks.stock_sync_service import StockSyncService
from app.services.stocks.stock_price_sync_service import StockPriceSync
from app.infrastructure.marketdata.dependencies import build_marketdata_provider, build_price_provider

def build_stock_service(db: Session) -> StockService:
    return StockService(
        stock_repo=StockCrud(db),
        db=db
    )

def get_stock_service(
        db: Session = Depends(get_db)
) -> StockService:
    return build_stock_service(db)

def build_stock_price_service(db: Session) -> StockPriceService:
    stock_repo = StockCrud(db)
    stock_price_repo = StockPriceCrud(db)
    return StockPriceService(stock_repo, stock_price_repo)

def get_stock_price_service(
        db: Session = Depends(get_db)
) -> StockPriceService:
    return build_stock_price_service(db)

def build_stock_sync_service(db: Session) -> StockSyncService:
    return StockSyncService(
        stock_service=build_stock_service(db),
        provider=build_marketdata_provider(),
        
    )

def build_stock_price_sync_service(db: Session) -> StockPriceSync:
    
    return StockPriceSync(
        db=db,
        stock_service=build_stock_service(db),
        stock_price_service=build_stock_price_service(db),
        provider=build_price_provider()
    )