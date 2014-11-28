from django.core.management.base import BaseCommand, CommandError
from web.crawler import crawl_url_subdomains
from web.models import Webpage

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        while True:
            source_pages = Webpage.objects.order_by('-last_human_request').all()
            webpage = source_pages[0]  # do something more sophisticated than grant the last request
            print 'webpage is a %s' % type(webpage)
            crawl_url_subdomains(webpage.full_url)
        