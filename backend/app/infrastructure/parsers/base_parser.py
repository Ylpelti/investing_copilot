from abc import ABC, abstractmethod
from typing import IO
from app.dto.transaction_dto import NormalizedTransactionDTO


class BaseParser(ABC):
    
    @abstractmethod
    def parse(self, file: IO) -> list[NormalizedTransactionDTO]:
        pass