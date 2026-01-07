from abc import ABC, abstractmethod

class BaseContext(ABC):
    @abstractmethod
    def build(self, analytic_result:dict):
        pass


