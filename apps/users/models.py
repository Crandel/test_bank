import logging
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)


class User(AbstractUser):

    def __str__(self):
        return self.username

    @property
    def get_token(self):
        token, created = Token.objects.get_or_create(user=self)
        return token.key
