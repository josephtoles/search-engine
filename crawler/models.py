from django.db import models


def Website(models.Model):
    url = models.URLField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # robots.txt
    robots_exists = models.BooleanField()
    robots_content = models.TextField()
    robots_updated = models.DateTimeField()

    class Meta:
        ordering = ['url']
    

def Webpage(models.Model):
    url = models.URLField(unique=True)
    robots_allowed = models.BooleanField()
    website = models.ForeignKey('Website')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['url']

