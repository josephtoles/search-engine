from utils.testcase import TestCase
from models import Website
from crawler import parse_url

class CrawlerTest(TestCase):

    def test_parse_url_function(self):
        self.assertEqual(parse_url('http://www.amazon.com/extension'), '/extension')
        self.assertEqual(parse_url('https://www.amazon.com/extension'), '/extension')
        with self.assertRaises(ValueError):
            parse_url('amazon.com/extension')
        with self.assertRaises(ValueError):
            parse_url('www.amazon.com/ext')

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
