import urllib2
from urlparse import urlparse, urljoin
from models import Website
from datetime import datetime, timedelta

UPDATE_ROBOTS_TXT_TIME_DELTA = timedelta(days=1)

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
def robots_txt_updated_recently(website):
    return (not website.robots_updated) or \
        website.robots_updated + UPDATE_ROBOTS_TXT_TIME_DELTA < datetime.now()

def update_robots_txt(website):
    if not robots_txt_updated_recently(website):
        robots_url = urljoin('http://'+website.url, 'robots.txt')
        print 'robots_url is %s' % robots_url
        print 'website.url is %s' % website.url
        # update robots.txt if it's been a while since the last time.
        website.robots_updated = datetime.now()
    pass

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


