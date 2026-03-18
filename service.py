import requests
import os
import time
import json

from config import API_URL, CACHE_FILE, CACHE_EXPIRY, CURRENTLY_LIST
from logger import log_operation



@log_operation("Ввод кол-во валюты")
def read_amount() -> float:
    while True:
        raw = input("Введите значение в USD: \n").strip()
        try:
            amount = float(raw.replace(",", "."))
            if amount <= 0:
                print("Сумма должна быть положительным числом, попробуйте ещё раз.")
                continue
            return amount
        except ValueError:
            print("Некорректный ввод. Введите число, например: 100 или 100.50")

@log_operation("Ввод вид валюты")
def read_currency() -> str:
    while True:
        raw = input("Введите аббревиатуру валюты, например 'CNY', 'EUR', 'GBP', 'RUB': \n").strip().upper()
        if raw in CURRENTLY_LIST:
            return raw
        print("Некорректная валюта. Попробуйте ещё раз.")

def take_rates_from_api():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["rates"]
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching rates from API: {e}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from API: {e}") from e
    except KeyError as e:
        raise KeyError(f"'rates' key not found in API response: {e}") from e

def save_cache_to_file(rates):
    try:
        data = {'timestamp' : time.time(), 'rates': rates}
        with open(CACHE_FILE, 'w', encoding="UTF-8") as f:
            json.dump(data, f)
    except OSError as e:
        raise IOError(f"Error saving to cache {e}")
    
    
def load_rates_with_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                data = json.load(f)
                if time.time() - data['timestamp'] < CACHE_EXPIRY:
                    return data['rates']
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid JSON from API: {e}")
    # если кэш невалиден или устарел
    rates = take_rates_from_api()
    save_cache_to_file(rates)
    return rates