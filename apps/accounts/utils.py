import requests
import logging

from django.conf import settings
from rest_framework import status

log = logging.getLogger(__name__)


def get_currency_rate(base, opposite):
    '''
    Unfortunatelly base currency always EUR, so we need to calculate rates manually
    '''
    params = {
        'access_key': settings.FIXER_ACCESS_KEY,
        'symbols': f'{base},{opposite}'
    }

    result = requests.get(settings.FIXER_BASE_URL, params=params)
    if result.status_code == status.HTTP_200_OK:
        # We need to check, because fixer sometimes return response with 200 code and error message
        result = result.json()
        rates = result.get('rates', {})
        if rates:
            base_rate = rates.get(base)
            opposite_rate = rates.get(opposite)
            return opposite_rate / base_rate
        else:
            log.error(f'Response from Fixer: "{result}"')
    return 0
