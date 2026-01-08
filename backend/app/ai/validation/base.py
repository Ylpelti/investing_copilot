from abc import ABC, abstractmethod

class BaseValidation(ABC):
    @abstractmethod
    def validate(self, text:str) -> str:
        raise NotImplementedError