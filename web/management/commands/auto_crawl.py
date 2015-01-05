from django.core.management.base import BaseCommand
from crawler.models import Website
from crawler.crawler import crawl_website
import time


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        if Website.objects.exists():
            while True:
                websites = Website.objects.all()
                for website in websites:
                    crawl_website(website)
                time.sleep(2)
        else:
            print 'You need Websites before I can begin crawling'
