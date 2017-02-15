from django.conf.urls import url

from django.conf import settings
from accounts import api

urlpatterns = [
    url(r'^$', api.AccountCreateAPIView.as_view(), name='create_account'),
    url(r'^list$', api.AccountListAPIView.as_view(), name='account_list'),
    url(r'^(?P<pk>{UUID})$'.format(UUID=settings.UUID_REGEX),
        api.AccountDetailAPIView.as_view(), name='account_detail'),
]
