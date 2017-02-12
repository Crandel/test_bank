from django.db.models.signals import post_save
from django.dispatch import receiver

from transactions.models import Transaction


@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created, **kwargs):
    if created:
        destination_account = instance.destination_account
        source_account = instance.source_account
        amount = instance.amount
        if destination_account and source_account:
            k = source_account.get_coefficient(amount, destination_account.currency_type)
            amount = amount * k
            if amount:
                source_account.balance -= amount
                source_account.save()
                destination_account.balance += amount
                destination_account.save()
        elif source_account:
            source_account.balance -= amount
            source_account.save()
        else:
            destination_account.balance += amount
            destination_account.save()
