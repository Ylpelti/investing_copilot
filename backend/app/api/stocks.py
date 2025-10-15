from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.stock import StockCreate, StockRead
from app.crud import stock_crud

router = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
)   

@router.post("/", response_model=StockRead)
def create_stock(stock: StockCreate, session: Session = Depends(get_db)):
    return stock_crud.create_stock(session, stock)

@router.get("/{stock_id}", response_model=StockRead)
def read_stock(stock_id: int, session: Session = Depends(get_db)):
    stock = stock_crud.get_stock(session, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


