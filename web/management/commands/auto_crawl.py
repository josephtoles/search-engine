from django.core.management.base import BaseCommand
from crawler.crawler import crawl_url_subdomains
from crawler.models import Webpage


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        if Webpage.objects.order_by('-last_human_request'):
            while True:
                source_pages = Webpage.objects.order_by('-last_human_request').all()
                webpage = source_pages[0]  # do something more sophisticated than grant the last request
                print 'webpage is a %s' % type(webpage)
                crawl_url_subdomains(webpage.full_url)
        else:
            print 'No pages to search'
