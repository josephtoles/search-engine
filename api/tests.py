from django.test import TestCase
from django.core.urlresolvers import reverse


class APITest(TestCase):

    def test_api(self):
        url = reverse('search-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.content, '[]')