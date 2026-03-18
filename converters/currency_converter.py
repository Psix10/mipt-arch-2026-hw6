from abc import ABC, abstractmethod

class CurrencyConverter(ABC):
    @abstractmethod
    def convert(self, amount: float, target_currency: str) -> float:
        raise NotImplementedError