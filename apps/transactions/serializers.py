from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from rest_framework import serializers

from transactions.models import Transaction


class TransactionDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'source_account', 'destination_account', 'amount', 'create_time')
        extra_kwargs = {
            'amount': {'validators': [MinValueValidator(limit_value=0.01)]},
        }

    def is_valid(self, raise_exception=False):
        is_validated = super().is_valid(raise_exception=False)

        if is_validated:
            destination_account = self.validated_data.get('destination_account')
            source_account = self.validated_data.get('source_account')
            amount = self.validated_data.get('amount')
            if destination_account and source_account:
                result = source_account.check_result(amount, destination_account.currency_type)
            elif source_account:
                result = source_account.balance - amount > 0
            if not result:
                self._errors['amount'] = _('Amount exceeds the limit')
            is_validated = result
        return is_validated


class TransactionListSerializer(TransactionDefaultSerializer):

    destination = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('source', 'destination', 'amount', 'create_time')

    def get_destination(self, obj):
        return str(obj.destination_account)

    def get_source(self, obj):
        return str(obj.source_account)
