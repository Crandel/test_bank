from django.urls import path, re_path

from django.conf import settings
from accounts import api

app_name = 'accounts'

urlpatterns = [
    path('', api.AccountCreateAPIView.as_view(), name='create_account'),
    path('list', api.AccountListAPIView.as_view(), name='account_list'),
    re_path(r'^(?P<pk>{UUID})$'.format(UUID=settings.UUID_REGEX),
        api.AccountDetailAPIView.as_view(), name='account_detail'),
]
