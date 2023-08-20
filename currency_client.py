import requests
import json


def parse_json_to_currencies(json_file):
    currencies_dict = json.loads(json_file)
    return currencies_dict["data"]


class Client:

    def __init__(self, api_key):
        self.__API_KEY__ = api_key

    def get_currencies(self, base_currency, *currencies):
        if len(currencies) < 1:
            raise ValueError("Currencies must be at least 1")

        format_currencies = "%2C".join(currencies)
        url = f"https://api.freecurrencyapi.com/v1/latest?apikey={self.__API_KEY__}&currencies={format_currencies}&base_currency={base_currency}"
        response = requests.get(url)

        # Проверка успешности ответа
        if response.status_code == 200:
            return parse_json_to_currencies(response.text)
        else:
            print(f"fail status: {response.status_code}")
            return None
