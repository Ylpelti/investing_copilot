from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.stock import StockCreate, StockRead
from app.crud.stock_crud import StockCrud
import logging
from typing import Annotated
from app.schemas.stock_price import StockPriceRead
from datetime import date
from app.services.stocks.dependencies import get_stock_service, get_stock_price_service
from app.services.stocks.stock_service import StockService
from app.services.stocks.stock_price_service import StockPriceService

logger = logging.getLogger("uvicorn.error")

router = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
)   

@router.post("/", response_model=StockRead, status_code=201)
def create_stock(
    stock: StockCreate,
    stock_service: StockService = Depends(get_stock_service)):
    return stock_service.create_stock(stock)

@router.get("/", response_model=list[StockRead])
def list_stocks(
    q: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0, 
    stock_service: StockService = Depends(get_stock_service)
):
    return stock_service.list_stocks(q, limit, offset)
    
@router.get("/{stock_id}/prices", response_model=list[StockPriceRead])
def get_stock_prices(
    stock_id: Annotated[int, Path(gt=0)],
    start: Annotated[date | None, Query()] = None, 
    end: Annotated[date | None, Query()] = None,
    limit: Annotated[int, Query(gt = 2, lt = 1000)] = 10,
    order: Annotated[str, Query(pattern="^(asc|desc)$")] = "asc",
    stock_price_service: StockPriceService = Depends(get_stock_price_service)
):
    return stock_price_service.get_prices(stock_id, start, end, limit, order)

@router.get("/{stock_id}/prices/latest", response_model=StockPriceRead)
def get_latest_stock_price(
    stock_id: Annotated[int, Path(gt=0)],
    stock_price_service: StockPriceService = Depends(get_stock_price_service)
):
    return stock_price_service.get_latest_price(stock_id)

@router.get("/{stock_id}", response_model=StockRead)
def read_stock_by_id(
    stock_id: int,
    stock_service: StockService = Depends(get_stock_service)):
    return stock_service.get_stock_by_id_or_404(stock_id)

@router.get("/by-ticker/{ticker}", response_model=StockRead)
def read_stock_by_ticker(
    ticker: str,
    stock_service: StockService = Depends(get_stock_service)):
    return stock_service.get_stock_by_ticker(ticker)





