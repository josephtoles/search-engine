from bs4 import BeautifulSoup
from django.db import models
from datetime import datetime, timedelta, tzinfo
from web.time_util import UTC
from urlparse import urljoin


#############
# CONSTANTS #
#############

UPDATE_ROBOTS_TIME_DELTA = timedelta(days=1)
UPDATE_WEBPAGE_TIME_DELTA = timedelta(days=1)

##########
# MODELS #
##########

class Website(models.Model):
    url = models.URLField(unique=True, blank=False)  # netloc in urlparse
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    exists = models.BooleanField()

    # robots.txt
    robots_exists = models.BooleanField()
    robots_content = models.TextField()
    robots_updated = models.DateTimeField(null=True)

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
    robots_allowed = models.BooleanField()
    website = models.ForeignKey('Website')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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

