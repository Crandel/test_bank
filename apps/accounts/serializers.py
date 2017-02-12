from rest_framework import serializers

from accounts.models import Account
from transactions.serializers import TransactionDefaultSerializer


class AccountDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'balance', 'currency', 'user')
        extra_kwargs = {
            'balance': {'write_only': True},
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
        return TransactionDefaultSerializer(transactions, many=True).data
