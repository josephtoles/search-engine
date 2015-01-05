from bs4 import BeautifulSoup
from django.db import models
from datetime import datetime, timedelta
from web.time_util import UTC
from urlparse import urljoin
import urllib2


#############
# CONSTANTS #
#############

UPDATE_ROBOTS_TIME_DELTA = timedelta(days=5)  # How frequently robotx.txt is updated
UPDATE_WEBPAGE_TIME_DELTA = timedelta(days=4)  # How frequently webpages are updated

##########
# MODELS #
##########


# Stores information unique to a root domain
class Website(models.Model):
    url = models.URLField(unique=True, blank=False)  # netloc in urlparse
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    exists = models.BooleanField(null=False, default=False, blank=True)

    # robots.txt
    robots_exists = models.BooleanField(null=False, default=False)
    robots_content = models.TextField()
    robots_updated = models.DateTimeField(null=True)  # null iff robots.txt has never been read

    class Meta:
        ordering = ['url']

    @property
    def robots_txt_updated_recently(self):
        if not self.robots_updated:
            return False
        try:
            return datetime.now() - self.robots_updated < UPDATE_ROBOTS_TIME_DELTA
        except TypeError:  # TODO figure out why this is necessary
            return datetime.now(UTC()) - self.robots_updated < UPDATE_ROBOTS_TIME_DELTA

    # update robots.txt if it's been a while since the last time.
    def update_robots_txt(self):
        if not self.robots_txt_updated_recently:
            robots_url = urljoin('http://' + self.url, 'robots.txt')  # TODO do this cleaner
            response = urllib2.urlopen(robots_url)
            html = response.read()
            self.robots_content = html
            self.robots_updated = datetime.now()
            self.save()


# Stores a particular webpage downloaded from the internet
class Webpage(models.Model):
    local_url = models.URLField()  # full or local url, beginning with a '/'
    robots_allowed = models.BooleanField(null=False, default=True)
    website = models.ForeignKey('Website')
    content = models.TextField(null=False, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # exists marks whether this webpage has been crawled
    #   cexists == null means the webpage has never been crawled
    #   exists == True means the webpage has been successfully crawled
    #   exists == False means the webpage tried to be crawled and this failed
    exists = models.NullBooleanField()

    class Meta:
        ordering = ['local_url']
        unique_together = ['local_url', 'website']

    @property
    def crawled_recently(self):
        return datetime.now(UTC()) - self.updated < UPDATE_WEBPAGE_TIME_DELTA

    @property
    def get_title(self):
        soup = BeautifulSoup(self.content)
        return soup.title.string

    @property
    def full_url(self):
        # Cheap hack. TODO do this properly
        if self.url.startswith('/'):
            return 'http://www.' + self.website.url + self.url
        return self.url
