from django.test import TestCase
import json
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse


# Create your tests here.

class UserTest(TestCase):

    def test_user(self):
        client = APIClient()
        data = {
            'email': "new@user.com",
            'password': 'password',
        }
        response = client.post(reverse('user-list'),
                               data,
                               format='json')
        self.assertEqual(response.status_code, 201)