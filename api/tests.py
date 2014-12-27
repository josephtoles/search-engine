from django.test import TestCase
from django.core.urlresolvers import reverse
from brain.models import Search
import json


class APITest(TestCase):

    def test_api(self):
        url = reverse('search-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.content, '[]')

    def test_create_search(self):
        self.assertEqual(Search.objects.count(), 0)
        url = reverse('search-list')
        data = json.dumps({
            'url': 'amazon.com',
            'title': 'this is a title',
            #'owner': user,
        })
        response = self.client.post(url, data=data, content_type='application/json',)
        print response.status_code
        print response.content
