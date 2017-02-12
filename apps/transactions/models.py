from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from accounts.models import get_random_id


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True, default=get_random_id, editable=False)
    source_account = models.ForeignKey('accounts.Account', related_name='source_account',
                                       verbose_name=_('Source Account'), blank=True, null=True)
    destination_account = models.ForeignKey('accounts.Account', related_name='destination_account',
                                            verbose_name=_('Destination Account'), blank=True, null=True)
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    create_time = models.DateTimeField(_('Create time'), default=timezone.now)

    def __str__(self):
        return '%s - %s: %.2f' % (
            self.source_account, self.destination_account, self.amount)
