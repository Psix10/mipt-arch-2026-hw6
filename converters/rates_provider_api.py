import json
import os
import time
from typing import Dict

import requests

from config import API_URL, CACHE_FILE, CACHE_EXPIRY
from converters.rates_provider import RatesProvider
from logger import logger

class ApiRatesProvider(RatesProvider):
    def __init__(self):
        self._rates: Dict[str, float] | None = None
        self._loaded_at: float = 0.0

    def get_rates(self) -> Dict[str, float]:
        now = time.time()
        if self._rates is not None and now - self._loaded_at < CACHE_EXPIRY:
            return self._rates

        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as f:
                    data = json.load(f)
                    if time.time() - data["timestamp"] < CACHE_EXPIRY:
                        self._rates = data["rates"]
                        self._loaded_at = now
                        return self._rates
            except (json.JSONDecodeError, KeyError):
                pass

        try:
            response = requests.get(API_URL, timeout=5)
            response.raise_for_status()
            data = response.json()
            rates = data["rates"]
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error fetching rates from API: {e}") from e
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid response from API: {e}") from e

        try:
            payload = {"timestamp": time.time(), "rates": rates}
            with open(CACHE_FILE, "w") as f:
                json.dump(payload, f)
        except OSError:
            pass

        self._rates = rates
        self._loaded_at = now
        return self._rates