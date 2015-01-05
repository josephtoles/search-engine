from utils.testcase import TestCase
from models import Website
from crawler import parse_url, is_a_local_url


class CrawlerTest(TestCase):

    def test_parse_url_function(self):
        self.assertEqual(parse_url('http://www.amazon.com/extension'), '/extension')
        self.assertEqual(parse_url('https://www.amazon.com/extension'), '/extension')
        with self.assertRaises(ValueError):
            parse_url('amazon.com/extension')
        with self.assertRaises(ValueError):
            parse_url('www.amazon.com/ext')

    def test_is_a_url_function(self):
        self.assertFalse(is_a_local_url('javascript.void(0)'))
        self.assertFalse(is_a_local_url('https://www.amazon.com/extension'))
        self.assertTrue(is_a_local_url('/extension'))

    # not really much of a test
    def test_create_website_model(self):
        Website.objects.create(url='Amazon.com')
        self.assertEqual(Website.objects.count(), 1)

