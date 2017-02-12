from django.conf.urls import url

from transactions import api

urlpatterns = [
    url(r'^$', api.TransactionCreateAPIView.as_view(), name='create_transaction'),
]
