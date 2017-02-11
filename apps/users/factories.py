import factory
from django.contrib.auth.hashers import make_password

from users.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    @factory.sequence
    def email(n):
        return '{0}_{1}@example.com'.format('user', n)

    @factory.sequence
    def username(n):
        return '{0}_{1}'.format('user', n)

    @factory.lazy_attribute
    def password(self):
        return make_password('test1234')

    is_active = True
