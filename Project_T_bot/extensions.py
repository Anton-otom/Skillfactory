import requests
import json
from config import keys, API_KEY


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException('Задайте разные валюты')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Введено некорректное количество валюты')

        r = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_ticker}")
        total_base = json.loads(r.content)["conversion_rates"][quote_ticker] * amount
        return total_base
