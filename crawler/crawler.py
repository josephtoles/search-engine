import urllib2
from urlparse import urlparse, urljoin
from models import Website
from datetime import datetime, timedelta, tzinfo
import robotparser

UPDATE_ROBOTS_TIME_DELTA = timedelta(days=1)

ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

# return appropriate pages from a url
# TODO move this into filter app
def get_pages(url):
    crawl_url(url)
    return []

# parses the base url out of a full url
def get_base_url(url):
    result = urlparse(url)
    print 'result is %s' % str(result)
    return result.netloc

# move this function into models method
# TODO clean up logic
# TODO write unit test for this function
def robots_txt_updated_recently(website):
    if not website.robots_updated:
        print 'not website.robots_updated'
        return False
    now = datetime.now(UTC())
    print 'type of updated is %s' % website.robots_updated
    print 'type of now is %s' % now
    if website.robots_updated + UPDATE_ROBOTS_TIME_DELTA > now:
        print 'wrong time'
        return True
    print 'not updated recently'
    return False
        
def update_robots_txt(website):
    if not robots_txt_updated_recently(website):
        print 'getting robots.txt for %s' % website.url
        robots_url = urljoin('http://'+website.url, 'robots.txt')
        print 'robots_url is %s' % robots_url
        print 'website.url is %s' % website.url
        response = urllib2.urlopen(robots_url)
        html = response.read()
        print 'html is %s' % html
        website.robots_content = html
        # update robots.txt if it's been a while since the last time.
        website.robots_updated = datetime.now()
        website.save()
        print 'got robots.txt for %s' % website.url
    else:
        print 'not getting robots.txt for %s' % website.url

def crawl_url(url):
    base_url = get_base_url(url)
    print 'base_url is %s' % base_url
    website, created = Website.objects.get_or_create(url=base_url)
    print 'website is %s' % str(website)
    update_robots_txt(website)
    # crawls through a url and subdomains and adds them to the database if not added recently
    # accesses target url once. Then updates new links only
    # TODO implement
    pass

def crawl_robots_txt(url):
    # attempts to download a url's robots.txt file it not already accessed recently
    # TODO implement
    pass

def is_forbidden(url):
    crawl_robots_txt(url)
    # has robots.txt been downloaded recently?
    # tests whether a url is forbidden to be accessed by a robots.txt file
    # TODO implement
    pass


