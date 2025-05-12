import os
import requests
from django.conf import settings

UP_TOKEN = getattr(settings, 'UKRPOSHTA_API_TOKEN', None)
BASE_URL = 'https://www.ukrposhta.ua/address-classifier-ws'


def get_up_cities():
    if not UP_TOKEN:
        # Якщо токена немає — повертаємо тестові дані або порожній список
        return [
            {'city': 'Київ', 'id': '1'},
            {'city': 'Львів', 'id': '2'},
            {'city': 'Харків', 'id': '3'}
        ]

    url = f'{BASE_URL}/rest/address/search-city?token={UP_TOKEN}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass
    return []


def get_up_warehouses(city_id):
    if not UP_TOKEN:
        # Тестові відділення
        return [
            {'name': 'Відділення 1', 'id': '101'},
            {'name': 'Відділення 2', 'id': '102'},
        ]

    url = f'{BASE_URL}/rest/address/warehouses/{city_id}?token={UP_TOKEN}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass
    return []
