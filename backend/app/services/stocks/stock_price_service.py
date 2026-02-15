from datetime import date
from app.crud.stock_prices_crud import StockPriceCrud
from app.crud.stock_crud import StockCrud
from app.core.errors.exceptions import NotFound, BadRequest



class StockPriceService:
    def __init__(
            self,
            stock_repo: StockCrud,
            stock_price_repo: StockPriceCrud
    ):
        self.stock_repo = stock_repo
        self.stock_price_repo = stock_price_repo

    def get_prices(
            self,
            stock_id: int,
            start: date | None,
            end: date | None,
            limit: int,
            order: str,
    ):
        if not self.stock_repo.get_by_id(stock_id):
            raise NotFound(message="Not found that stock")
        if start and end and start > end:
            raise BadRequest(message="invalid date ranges")

        return self.stock_price_repo.get_prices(stock_id, start, end, limit, order)
    
    def get_latest_price(self, stock_id: int):
        stock = self.stock_repo.get_by_id(stock_id):
        if not stock:
            raise NotFound(message="Not found stock")
        
        latest = self.stock_price_repo.get_latest_price(stock_id)
        if not latest:
            raise NotFound(message="Not found latest price")
        return latest