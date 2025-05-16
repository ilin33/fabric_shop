import os
import requests
from django.conf import settings

NP_TOKEN = getattr(settings, 'NOVA_POSHTA_API_TOKEN', None)
BASE_URL = 'https://api.novaposhta.ua/v2.0/json/'


def get_np_cities():
    if not NP_TOKEN:
        # Якщо токена немає — повертаємо тестові дані або порожній список
        return [
            {'Description': 'Київ', 'Ref': '1'},
            {'Description': 'Львів', 'Ref': '2'},
            {'Description': 'Харків', 'Ref': '3'},
            {'Description': 'Дніпро', 'Ref': '4'},
        ]

    url = BASE_URL
    data = {
        "apiKey": NP_TOKEN,
        "modelName": "Address",
        "calledMethod": "getCities",
        "methodProperties": {}
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json().get("data", [])
    except requests.RequestException:
        pass
    return []


def get_np_warehouses(city_ref):
    if not NP_TOKEN:
        # Тестові відділення
        return [
            {'Description': 'Відділення 1', 'Ref': '101'},
            {'Description': 'Відділення 2', 'Ref': '102'},
        ]

    url = BASE_URL
    data = {
        "apiKey": NP_TOKEN,
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {"CityRef": city_ref}
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            warehouses = response.json().get("data", [])
            # Повертаємо тільки ті відділення, у яких є Description
            return [
                {'Description': wh['Description'], 'Ref': wh['Ref']}
                for wh in warehouses
                if wh.get('Description') and wh.get('Description').strip()
            ]
    except requests.RequestException:
        pass
    return []

