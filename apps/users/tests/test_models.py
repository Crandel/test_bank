from test_plus.test import TestCase

from users.factories import UserFactory


class TestUser(TestCase):
    def setUp(self):
        self.user = UserFactory.create(username='Test User')

    def test__str__(self):
        self.assertEqual(self.user.__str__(), "Test User")
