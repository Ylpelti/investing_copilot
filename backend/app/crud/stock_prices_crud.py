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

    def read_stock_price(self, stock_price_id: int) -> StockPrice | None:
        stock_price = self.db.query(StockPrice).filter(StockPrice.id == stock_price_id).first()
        if not stock_price:
            raise NotFound(message="Stock prices not found")
        return stock_price

    def read_stock_prices_by_stock_id(self, stock_id: int) -> list[StockPrice]:
        prices = self.db.query(StockPrice).filter(StockPrice.stock_id == stock_id).order_by(StockPrice.date.asc()).all()
        if not prices:
            raise NotFound(message="Stock prices not found")
        return prices

    def read_stock_prices_by_ticker(self, ticker: str) -> list[StockPrice]:
        prices = self.db.query(StockPrice).join(Stock).filter(Stock.ticker == ticker).order_by(StockPrice.date.asc()).all()
        if not prices:
            raise NotFound(message="Stock prices not found")
        return prices

    def read_stock_prices_by_date_range(self, stock_id: int, start_date: str, end_date: str) -> list[StockPrice]:
        logger.info(f"Fetching stock prices for stock_id {stock_id} from {start_date} to {end_date}")
        try:
            start_date_dt = datetime.fromisoformat(start_date).date()
            end_date_dt = datetime.fromisoformat(end_date).date()
        except ValueError:
            raise BadRequest(message="Invalid date format. Use ISO format (YYYY-MM-DD).")
        if start_date_dt > end_date_dt:
            raise BadRequest(message="start_date must be before end_date.")
        prices = (self.db.query(StockPrice).filter(
            StockPrice.stock_id == stock_id,
            StockPrice.date >= start_date_dt,
            StockPrice.date <= end_date_dt)
        .order_by(StockPrice.date.asc())
        .all())
        if not prices:
            raise NotFound(message=f"No prices found for stock_id={stock_id} in given date range")
        return prices
