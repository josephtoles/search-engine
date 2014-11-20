from django.db import models


class Website(models.Model):
    url = models.URLField(unique=True)  # netloc in urlparse
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    exists = models.BooleanField()

    # robots.txt
    robots_exists = models.BooleanField()
    robots_content = models.TextField()
    robots_updated = models.DateTimeField(null=True)

    class Meta:
        ordering = ['url']
    

class Webpage(models.Model):
    url = models.URLField(unique=True)  # full url
    robots_allowed = models.BooleanField()
    website = models.ForeignKey('Website')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['url']

