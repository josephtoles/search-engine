from django.db import models
from django.contrib.auth.models import User
from crawler.models import Webpage


# Model defining a search
# This is for the search defined by existing webpages
class Search(models.Model):
    url = models.URLField()  # root url of search
    title = models.CharField(max_length=100, default='', blank=True)  # optional designator
    webpages = models.ManyToManyField(Webpage, through='WebpageRating')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)

    # add unicode formatting title if present. default constructed otherwise


# Model of a user's evaluation of a webpage
class WebpageRating(models.Model):
    webpage = models.ForeignKey(Webpage)
    search = models.ForeignKey('Search')
    rating = models.IntegerField()  # 1 is good, -1 is bad
