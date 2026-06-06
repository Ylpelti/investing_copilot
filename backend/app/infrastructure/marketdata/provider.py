from abc import abstractmethod, ABC
from typing import Iterable
from app.dto.stock_dto import ExternalStockDTO

class MarketDataProvider(ABC):

    @abstractmethod
    def fetch_many(self, tickers: dict[str, str]) -> Iterable[ExternalStockDTO]:
        pass
