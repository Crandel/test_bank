from django.urls import path

from transactions import api

app_name = 'transactions'

urlpatterns = [
    path('', api.TransactionCreateAPIView.as_view(), name='create_transaction'),
]
