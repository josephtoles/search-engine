# from django.test import TestCase
from utils.testcase import TestCase
from web.models import Search


class SimpleTest(TestCase):

    # Tests that 1 + 1 always equals 2.
    def test_basic_addition(self):
        self.assertEqual(1 + 1, 2)


class ModelTest(TestCase):

    def test_create_search(self):
        URL = 'amazon.com'
        TITLE = 'Search the Amazon'
        search = Search.objects.create(
            url=URL,
            title=TITLE,
            # no webpages
            owner = self.user)
        self.assertEqual(Search.objects.count(), 1)
        self.assertEqual(search.url, URL)
        self.assertEqual(search.title, TITLE)

