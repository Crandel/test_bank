import requests
from django.conf import settings
from rest_framework import status


def get_currency_rate(base, opposite):
    params = {
        'base': base,
        'symbols': opposite
    }
    result = requests.get(settings.FIXER_BASE_URL, params=params)
    if result.status_code == status.HTTP_200_OK:
        return result.json().get('rates', {}).get(opposite, 0)
    return 0
