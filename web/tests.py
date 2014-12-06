# from django.test import TestCase
from utils.testcase import TestCase
from web.models import Search


class SimpleTest(TestCase):

    # Tests that 1 + 1 always equals 2.
    def test_basic_addition(self):
        self.assertEqual(1 + 1, 2)


class ModelTest(TestCase):

    def test_create_search(self):
        search = Search.objects.create(
            url='amazon.com',
            title='Search the Amazon',
            # no webpages
            owner = self.user)
        search.save()

        
