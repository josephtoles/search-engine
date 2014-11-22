from django.db import models
from datetime import datetime, timedelta, tzinfo
from web.time_util import UTC


#############
# CONSTANTS #
#############

UPDATE_ROBOTS_TIME_DELTA = timedelta(days=1)


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

