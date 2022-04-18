import requests
import json
from config import keys

class APIException(Exception):
    pass

class Converter():
    @staticmethod
    def get_price(*values):
        if len(values) > 3:
            raise APIException('Слишком много параметров')

        if len(values) < 3:
            raise APIException('Слишком мало параметров')

        amount, base, quote = values

        if base == quote:
            raise APIException('Невозможно перевести одинаковый валюты')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        if base == 'евро':
            r = requests.get(
                f"http://api.exchangeratesapi.io/v1/latest?access_key=b5a6c940400ca4d7304e4a09c20d57f9&symbols={quote_ticker}&format=1")
            answer = json.loads(r.content)['rates'][quote_ticker] * float(amount)
            answer = f"{amount} {base} = {answer:.2f} {quote}"
            return answer

        elif quote == 'евро':
            r = requests.get(
                f"http://api.exchangeratesapi.io/v1/latest?access_key=b5a6c940400ca4d7304e4a09c20d57f9&symbols={base_ticker}&format=1")
            answer = 1 / json.loads(r.content)['rates'][base_ticker] * float(amount)
            answer = f"{amount} {base} = {answer:.2f} {quote}"
            return answer

        else:
            raise APIException('Одна из валют должна быть "евро". Введите корректный запрос')
