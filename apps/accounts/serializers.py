from django.core.validators import MinValueValidator
from rest_framework import serializers

from accounts.models import Account
from transactions.serializers import TransactionListSerializer


class AccountDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'balance', 'currency', 'user')
        extra_kwargs = {
            'balance': {'write_only': True, 'validators': [MinValueValidator(limit_value=0)]},
            'currency': {'write_only': True},
            'user': {'write_only': True},
        }


class AccountDetailSerializer(AccountDefaultSerializer):
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('balance', 'currency_type', 'create_time', 'transactions')

    def get_transactions(self, obj):
        transactions = obj.source_account.all()
        return TransactionListSerializer(transactions, many=True).data


class AccountListSerializer(AccountDefaultSerializer):
    transactions_count = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('id', 'balance', 'currency_type', 'create_time', 'transactions_count')

    def get_transactions_count(self, obj):
        return obj.source_account.count()
