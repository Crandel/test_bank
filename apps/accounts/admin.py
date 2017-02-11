from django.contrib import admin

from accounts.models import Account, Transaction


admin.register(Account)
admin.register(Transaction)
