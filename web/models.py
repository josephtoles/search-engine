from bs4 import BeautifulSoup
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, tzinfo
from web.time_util import UTC
from urlparse import urljoin
import urllib2


#############
# CONSTANTS #
#############

UPDATE_ROBOTS_TIME_DELTA = timedelta(days=1)
UPDATE_WEBPAGE_TIME_DELTA = timedelta(days=1)

##########
# MODELS #
##########

class Search(models.Model):
    url = models.URLField()
    webpages = models.ManyToManyField('Webpage', through='WebpageRating')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)

class WebpageRating(models.Model):
    webpage = models.ForeignKey('Webpage')
    search = models.ForeignKey('Search')
    rating = models.IntegerField()  # 1 is good, -1 is bad

class Website(models.Model):
    url = models.URLField(unique=True, blank=False)  # netloc in urlparse
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    exists = models.BooleanField(null=False, default=False, blank=True)

    # robots.txt
    robots_exists = models.BooleanField(null=False, default=False)
    robots_content = models.TextField()
    robots_updated = models.DateTimeField()

    class Meta:
        ordering = ['url']
    
    @property
    def robots_txt_updated_recently(self):
        if not self.robots_updated:
            return False
        try:
            return datetime.now() - self.robots_updated < UPDATE_ROBOTS_TIME_DELTA
        except TypeError:  # something to do with internal datetimes
            return datetime.now(UTC()) - self.robots_updated < UPDATE_ROBOTS_TIME_DELTA

    # update robots.txt if it's been a while since the last time.
    def update_robots_txt_if_necessary(self):
        if not self.robots_txt_updated_recently:
            robots_url = urljoin('http://' + self.url, 'robots.txt')
            response = urllib2.urlopen(robots_url)
            html = response.read()
            self.robots_content = html
            self.robots_updated = datetime.now()
            self.save()

class Webpage(models.Model):
    url = models.URLField()  # full or local url, I think
    robots_allowed = models.BooleanField(null=False, default=True)
    website = models.ForeignKey('Website')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_human_request = models.DateTimeField(null=True, default=None)

    class Meta:
        ordering = ['url']
        unique_together = ['url', 'website']

    @property
    def crawled_recently(self):
        return datetime.now(UTC()) - self.updated < UPDATE_WEBPAGE_TIME_DELTA

    @property
    def get_title(self):
        soup = BeautifulSoup(self.content)
        return soup.title.string

    @property
    def full_url(self):
        # Cheap hack. You should do this properly instead.
        if self.url.startswith('/'):
            return 'http://www.' + self.website.url + self.url
        return self.url

