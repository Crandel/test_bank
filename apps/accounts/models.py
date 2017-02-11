from random import randint
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


CURRENCY = (
    (0, 'EUR'),
    (1, 'USD'),
    (2, 'GBR'),
    (3, 'CHF'),
)


def get_random_id():
    return randint(10000000, 99999999)


class Account(models.Model):
    id = models.IntegerField(primary_key=True, default=get_random_id, editable=False)
    user = models.ForeignKey('users.User', related_name='account_owner', verbose_name=_('Account Owner'))
    balance = models.FloatField(_('Balance'), default=0.0)
    currency = models.PositiveIntegerField(_('Currency'), choices=CURRENCY, default=0)
    create_time = models.DateTimeField(_('Create time'), default=timezone.now)


class Transaction(models.Model):
    source_account = models.ForeignKey('accounts.Account', related_name='source_account',
                                       verbose_name=_('Source Account'))
    destination_account = models.ForeignKey('accounts.Account', related_name='destination_account',
                                            verbose_name=_('Destination Account'))
    amount = models.FloatField(_('Balance'), default=0.0)
    create_time = models.DateTimeField(_('Create time'), default=timezone.now)
