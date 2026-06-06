from abc import abstractmethod, ABC
from typing import Iterable
from app.dto.stock_price_dto import ExternalStockPriceDTO

class PriceProvider(ABC):
    @abstractmethod
    def fetch_history(self, ticker: str) -> Iterable[ExternalStockPriceDTO]:
        pass