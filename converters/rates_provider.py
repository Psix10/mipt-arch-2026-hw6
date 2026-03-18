from abc import ABC, abstractmethod
from typing import Dict


class RatesProvider(ABC):
    @abstractmethod
    def get_rates(self) -> Dict[str, float]:
        """Возвращает словарь курсов, например {'EUR': 0.86, 'RUB': 82.27}."""
        raise NotImplementedError
