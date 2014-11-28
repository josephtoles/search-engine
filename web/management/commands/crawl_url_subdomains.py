from django.core.management.base import BaseCommand, CommandError
from web.crawler import crawl_url_subdomains

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print 'you have hit crawl_url_subdomains'
        print 'args are %s' % str(args)
        crawl_url_subdomains(url=args[0])
        

