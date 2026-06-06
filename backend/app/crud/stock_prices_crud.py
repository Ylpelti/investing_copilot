from sqlalchemy.orm import Session
from app.models.stock_price import StockPrice
from app.schemas.stock_price import StockPriceRead
from datetime import datetime, date
from app.core.errors.exceptions import NotFound, BadRequest
from app.models.stock import Stock
import logging
from app.crud.base_crud import BaseCrud

logger = logging.getLogger(__name__)

class StockPriceCrud(BaseCrud):

    def add(self, stock_price: StockPrice) -> None:
        self.db.add(stock_price)

    def get_prices(
            self,
            stock_id: int,
            start_date: date | None,
            end_date: date | None,
            limit: int,
            order: str
    ) -> list[StockPrice]:
        query = self.db.query(StockPrice)
        query = query.filter(StockPrice.stock_id == stock_id)
        if start_date:
            query = query.filter(StockPrice.date >= start_date)
        
        if end_date:
            query = query.filter(StockPrice.date <= end_date)

        if order == "asc":
            query = query.order_by(StockPrice.date.asc())
        else: 
            query = query.order_by(StockPrice.date.desc())
        return query.limit(limit).all()

    def get_latest_price(self, stock_id: int) -> StockPrice | None:
        return self.db.query(StockPrice).filter(StockPrice.stock_id == stock_id).order_by(StockPrice.date.desc()).first()
        
        
    def get_by_id_and_date(self, stock_id:int, date: date) -> StockPrice | None:
        return self.db.query(StockPrice).filter(StockPrice.stock_id == stock_id, StockPrice.date == date).first()