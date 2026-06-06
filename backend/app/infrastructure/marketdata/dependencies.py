from app.infrastructure.marketdata.price_provider import PriceProvider
from app.infrastructure.marketdata.provider import MarketDataProvider
from app.infrastructure.marketdata.yahoo_provider import YahooMarketDataProvider
from app.infrastructure.marketdata.yahoo_price_provider import YahooPriceProvider

def build_marketdata_provider() -> MarketDataProvider:
    return YahooMarketDataProvider()

def build_price_provider() -> PriceProvider:
    return YahooPriceProvider()