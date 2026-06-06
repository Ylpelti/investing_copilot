from app.crud.stock_crud import StockCrud
from app.schemas.stock import StockCreate
from app.core.errors.exceptions import DuplicateStockError, NotFound
from app.models.stock import Stock
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

class StockService:
    def __init__(
            self,
            stock_repo: StockCrud,
            db: Session
    ):
        self.stock_repo = stock_repo
        self.db = db


    def create_stock(self, data: StockCreate) -> Stock | None:
        existing = self.stock_repo.get_by_isin(data.isin)
        if existing:
            raise DuplicateStockError(message="Stock already in database")
        stock = Stock(
            ticker = data.ticker,
            isin = data.isin,
            name = data.name,
            close_price = data.close_price,
            sector = data.sector
        )

        try:
            self.stock_repo.add(stock)
            self.db.commit()
            self.db.refresh(stock)
            return stock
        except IntegrityError:
            self.db.rollback()
            return self.stock_repo.get_by_isin(data.isin)

    def get_stock_by_id_or_404(self, stock_id:int) -> Stock:
        stock = self.stock_repo.get_by_id(stock_id) 
        if not stock:
            raise NotFound(message="Stock not found")
        return stock
    
    def list_stocks(self, q, limit, offset):
        return self.stock_repo.list_or_search(q, limit, offset)
    
    def get_stock_by_ticker(self, ticker:str):
        stock = self.stock_repo.get_by_ticker(ticker)
        if not stock:
            raise NotFound(message="Stock not found by ticker")
        return stock
    
    def get_stock_by_isin(self, isin:str):
        stock = self.stock_repo.get_by_isin(isin)
        if not stock:
            raise NotFound(message="Stock not found by isin")
        return stock