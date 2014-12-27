from django.test import TestCase
from django.core.urlresolvers import reverse
from brain.models import Search
import json
from rest_framework.test import APIClient


class APITest(TestCase):

    def test_api(self):
        url = reverse('search-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.content, '[]')

    def test_create_search(self):

        client = APIClient()
        res = client.post(reverse('search-list'),
                          {
                              'url': 'http://www.google.com',
                              'title': 'this is a title',
                          },
                          format='json')
        self.assertEqual(res.status_code, 201)
