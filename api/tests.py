from django.test import TestCase
from django.core.urlresolvers import reverse
from brain.models import Search
import json
from rest_framework.test import APIClient


class APITest(TestCase):

    def test_api(self):
        url = reverse('search-list')
        self.assertEqual(reverse('search-list'), '/api/searches/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.content, '[]')

    def test_create_search(self):
        client = APIClient()
        TARGET_URL = 'http://www.google.com'
        TITLE = 'this is a title'
        response = client.post(
            reverse('search-list'),
            {
                'url': TARGET_URL,
                'title': TITLE,
            },
            format='json')
        self.assertEqual(response.status_code, 201)
        search = Search.objects.get(id=json.loads(response.content)['id'])
        self.assertEqual(search.title, TITLE)
        self.assertEqual(search.url, TARGET_URL)
