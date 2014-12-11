from utils.testcase import TestCase
from models import Website


class CrawlerTest(TestCase):

    def test_create_website_model(self):
        Website.objects.create(url='Amazon.com')
        self.assertEqual(Website.objects.count(), 1)

    '''
    # This doesn't work because blank=False is only validated
    # when creating a model through a form. TODO resolve this
    def test_url_cannot_be_blank(self):
        Website.objects.create(url='')
        self.assertEqual(Website.objects.count(), 0)
    '''
