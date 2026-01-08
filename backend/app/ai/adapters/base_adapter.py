from abc import ABC, abstractmethod
from typing import List, Dict

class LLMAdapter(ABC):
    @abstractmethod
    def generate(self, messages: List[Dict[str, str]]) -> str:
        pass
