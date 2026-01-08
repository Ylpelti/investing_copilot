from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseContext(ABC):
    @abstractmethod
    def build(self, analytic_result:Dict[str, Any]) -> Dict[str, Any]:
        pass


