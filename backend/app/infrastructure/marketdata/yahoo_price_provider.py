from app.infrastructure.marketdata.price_provider import PriceProvider
import yfinance as yf
from app.dto.stock_price_dto import ExternalStockPriceDTO
from decimal import Decimal
import pandas as pd



class YahooPriceProvider(PriceProvider):
    def fetch_history(self, ticker: str):

        stock_data = yf.Ticker(ticker)
        hist = stock_data.history(period="5y")

        for date, row in hist.iterrows(): #type: ignore
            date: pd.Timestamp
            yield ExternalStockPriceDTO(
                date=date.date(),
                open_price=Decimal(str(row["Open"])),
                high_price=Decimal(str(row["High"])),
                low_price=Decimal(str(row["Low"])),
                close_price=Decimal(str(row["Close"])),
                volume=int(row["Volume"]) if row["Volume"] else 0,
            )