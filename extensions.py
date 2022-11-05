import requests
import json
from config import keys

#Создаем исключения (не правильный ввод пользователя ConvertionException)
class ConvertionException(Exception):
    pass

class ValueConvertor:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Вы ввели одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount_ticker = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        url = f"https://api.apilayer.com/fixer/convert?to={base_ticker}&from={quote_ticker}&amount={amount_ticker}"
        headers = {"apikey": "oFzAPtY2RNWxgCSoPniojRj8fo75RhQN"}
        response = requests.request("GET", url, headers=headers)
        total_base = json.loads(response.content)

        return total_base
