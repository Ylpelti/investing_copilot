import yfinance as yf
from app.dto.stock_dto import ExternalStockDTO
from app.infrastructure.marketdata.provider import MarketDataProvider

class YahooMarketDataProvider(MarketDataProvider):
        
    def fetch_many(self, tickers: dict[str, str]):

        for ticker, isin in tickers.items():
            try:
                ticker_client = yf.Ticker(ticker)
                data = ticker_client.info

            except Exception:
                continue

            if "regularMarketPrice" not in data:
                continue

            yield ExternalStockDTO(
                ticker = ticker,
                isin = isin,
                name = data.get('shortName', ''),
                close_price=data['regularMarketPrice'],
                sector = data.get("sector")    
            )

