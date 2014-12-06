from utils.testcase import TestCase
from models import Website

class CrawlerTest(TestCase):

    def test_create_website_model(self):
        Website.objects.create(url='Amazon.com')
        self.assertEqual(Website.objects.count(), 1)

    def test_url_cannot_be_blank(self):
        Website.objects.create(url='')
        self.assertEqual(Website.objects.count(), 0)

