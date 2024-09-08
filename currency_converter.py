import requests
from requests import RequestException


def convert(from_currency, to_currency, amount):
    if from_currency == to_currency:
        return amount
    from_currency = from_currency.lower()
    URL = f'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{from_currency}.json'

    try:
        res = requests.get(URL).json()[from_currency][to_currency.lower()]
    except RequestException:
        return -1
    return res * amount


