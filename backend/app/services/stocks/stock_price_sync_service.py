from app.services.stocks.stock_price_service import StockPriceService
from app.services.stocks.stock_service import StockService
from sqlalchemy.orm import Session
from app.infrastructure.marketdata.price_provider import PriceProvider

class StockPriceSync:
    def __init__(
            self,
            db: Session,
            stock_service: StockService,
            stock_price_service: StockPriceService,
            provider: PriceProvider
    ):
        self.db = db
        self.stock_service = stock_service
        self.stock_price_service = stock_price_service
        self.provider = provider

    def sync_all(self):
        stocks = self.stock_service.list_stocks(q = None, limit = 100000, offset = 0)
        
        for stock in stocks:
            for dto in  self.provider.fetch_history(stock.ticker):
                self.stock_price_service.add_price_if_missing(stock.id, dto)

        self.db.commit()