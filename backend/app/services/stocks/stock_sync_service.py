from app.services.stocks.stock_service import StockService
from app.infrastructure.marketdata.provider import MarketDataProvider
from app.schemas.stock import StockCreate

class StockSyncService:
    def __init__(
            self,
            stock_service: StockService,
            provider: MarketDataProvider,
            
    ):
        self.stock_service = stock_service
        self.provider = provider
        

    def sync_from_mapping(self, ticker_map: dict[str, str]):

        for dto in self.provider.fetch_many(ticker_map):

            stock_create = StockCreate(
                ticker=dto.ticker,
                isin=dto.isin,
                name=dto.name,
                close_price=dto.close_price,
                sector=dto.sector,
            )

            self.stock_service.create_stock(stock_create)
