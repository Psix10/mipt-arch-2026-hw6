from typing import Dict

from converters import CurrencyConverter
from converters.rates_provider import RatesProvider
from logger import log_operation


class UsdConverter(CurrencyConverter):
    def __init__(self, rates_provider: RatesProvider):
        self._rates_provider = rates_provider
        self._rates: Dict[str, float] = self._rates_provider.get_rates()

    @log_operation("Конвертируем")
    def convert(self, amount: float, target_currency: str) -> float:
        try:
            rate = self._rates[target_currency]
        except KeyError:
            raise ValueError(f"Unsupported currency: {target_currency}")
        return amount * rate
