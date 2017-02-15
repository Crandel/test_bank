import decimal
from random import randint
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from accounts.utils import get_currency_rate


CURRENCY = (
    (0, 'EUR'),
    (1, 'USD'),
    (2, 'GBP'),
    (3, 'CHF'),
)


def get_random_id():
    return randint(10000000, 99999999)


class Account(models.Model):
    id = models.IntegerField(primary_key=True, default=get_random_id, editable=False)
    user = models.ForeignKey('users.User', related_name='account_owner', verbose_name=_('Account Owner'))
    balance = models.DecimalField(_('Balance'), max_digits=10, default=0.0, decimal_places=2)
    currency = models.PositiveIntegerField(_('Currency'), choices=CURRENCY, default=0)
    create_time = models.DateTimeField(_('Create time'), default=timezone.now)

    @property
    def currency_type(self):
        return CURRENCY[self.currency][1]

    def get_coefficient(self, amount, other_currency):
        k = decimal.Decimal(1.0)
        cur_type = self.currency_type
        if cur_type != other_currency:
            k = decimal.Decimal(get_currency_rate(cur_type, other_currency))
        return k

    def check_result(self, amount, other_currency):
        k = self.get_coefficient(amount, other_currency)
        amount = amount * k
        if amount:
            return self.balance - amount > 0

    def __str__(self):
        return '%.2f %s' % (self.balance, self.currency_type)
