from app.crud.stock_crud import StockCrud
from app.schemas.stock import StockCreate
from app.core.errors.exceptions import DuplicateStockError, NotFound
from app.models.stock import Stock

class StockService:
    def __init__(
            self,
            stock_repo: StockCrud
    ):
        self.stock_repo = stock_repo


    def create_stock(self, stock:StockCreate):
        existing = self.stock_repo.get_stock_by_ticker(stock.ticker)
        if existing:
            raise DuplicateStockError()
        return self.stock_repo.create_stock(stock)

    def get_stock_by_id_or_404(self, stock_id:int) -> Stock:

        stock = self.stock_repo.get_by_id(stock_id) 
        if not stock:
            raise NotFound(message="Stock not found")
        return stock
    
    def list_stocks(self, q, limit, offset):
        return self.stock_repo.list_or_search(q, limit, offset)
    
    def get_stock_by_ticker(self, ticker:str):
        return self.stock_repo.get_stock_by_ticker(ticker)
    
    def get_stock_by_isin(self, isin:str):
        return self.stock_repo.get_stock_by_isin(isin)