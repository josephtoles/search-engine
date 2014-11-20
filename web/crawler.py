import urllib2
import robotparser
from urlparse import urlparse, urljoin
from datetime import datetime, timedelta, tzinfo
from models import Website
# robotparser documentation at https://docs.python.org/2/library/robotparser.html

#############
# CONSTANTS #
#############

UPDATE_ROBOTS_TIME_DELTA = timedelta(days=1)

#####################
# TIMEZONE HANDLING #
#####################

ZERO = timedelta(0)
class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

#############
# FUNCTIONS #
#############

def robots_txt_updated_recently(website):
    if not website.robots_updated:
        return False
    return website.robots_updated + UPDATE_ROBOTS_TIME_DELTA > datetime.now(UTC())
        
# update robots.txt if it's been a while since the last time.
def update_robots_txt_if_necessary(website):
    if not robots_txt_updated_recently(website):
        robots_url = urljoin('http://'+website.url, 'robots.txt')
        response = urllib2.urlopen(robots_url)
        html = response.read()
        website.robots_content = html
        website.robots_updated = datetime.now()
        website.save()

def crawl_url(url):
    base_url = urlparse(url).netloc
    website, created = Website.objects.get_or_create(url=base_url)
    update_robots_txt_if_necessary(website)
    # crawls through a url and subdomains and adds them to the database if not added recently
    # accesses target url once. Then updates new links only
    # TODO implement
    pass


