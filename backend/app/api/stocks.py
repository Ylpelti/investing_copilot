from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.stock import StockCreate, StockRead
from app.crud.stock_crud import StockCrud

router = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
)   

@router.post("/", response_model=StockRead, status_code=201)
def create_stock(stock: StockCreate, db: Session = Depends(get_db)):
    crud = StockCrud(db)
    return crud.create_stock(stock)


@router.get("/{stock_id}", response_model=StockRead)
def read_stock_by_id(stock_id: int, db: Session = Depends(get_db)):
    crud = StockCrud(db)
    stock = crud.get_id_or_404(stock_id)
    return stock

@router.get("/ticker/{ticker}", response_model=StockRead)
def read_stock_by_ticker(ticker: str, db: Session = Depends(get_db)):
    crud = StockCrud(db)
    return crud.get_stock_by_ticker(ticker)

@router.get("/search", response_model=list[StockRead])
def search_stocks(q: str, db:Session = Depends(get_db)):
    crud = StockCrud(db)
    return crud.search_stock_by_ticker(q)



