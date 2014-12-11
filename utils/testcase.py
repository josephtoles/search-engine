# Includes helper code for testing
from django.test import TestCase as BaseTestCase
from django.contrib.auth.models import User


DEFAULT_USER = {
    'username': 'Lisbeth Salander',
    'email': 'wasp@anonymous.ru',
    'password': 'password', }


# Overloads default Django TestCase to provide useful features
class TestCase(BaseTestCase):

    def setUp(self):
        # Create a default user
        self.user = User.objects.create_user(
            username=DEFAULT_USER['username'],
            email=DEFAULT_USER['email'],
            password=DEFAULT_USER['password'], )
