from django.db import models


class Website(models.Model):
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Robots.txt
    robots_html = models.TextField()
    robots_updated = models.DateTimeField()
    robots_get_count = models.PositiveIntegerField()

    class Meta:
        ordering = ['url']


class Webpage(models.Model):
    # field: foreign key to Website
    website = models.ForeignKey('Website')
    url = models.URLField()  # Full URL including website's base URL

    # whether this page exists
    exists = models.BooleanField()

    # HTML content of Webpage
    content = models.TextField()

    # number of times this page has been crawled
    crawl_count = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

