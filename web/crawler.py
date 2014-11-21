import robotexclusionrulesparser
from bs4 import BeautifulSoup
import urllib2
from robotexclusionrulesparser import RobotExclusionRulesParser
from urlparse import urlparse, urljoin
from datetime import datetime, timedelta, tzinfo
from models import Website, Webpage

# custom django commands
# https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
# http://stackoverflow.com/questions/4291895/django-should-i-kick-off-a-separate-process
# use call_command, extract to a Process http://stackoverflow.com/questions/13239087/django-multiprocessing-oddity

#############
# CONSTANTS #
#############

UPDATE_ROBOTS_TIME_DELTA = timedelta(days=1)
UPDATE_WEBPAGE_TIME_DELTA = timedelta(days=1)

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
    print 'handling robots.txt'
    if not robots_txt_updated_recently(website):
        robots_url = urljoin('http://' + website.url, 'robots.txt')
        response = urllib2.urlopen(robots_url)
        html = response.read()
        website.robots_content = html
        website.robots_updated = datetime.now()
        website.save()

def crawled_recently(webpage):
    return datetime.now(UTC()) - webpage.updated < UPDATE_WEBPAGE_TIME_DELTA

# add a single url to the database if necessary
# returns a tuple (webpage, created)
# where webpage is the webpage (None if not accessible)
# and created is a boolean representing whether the webpage was actually fetched with this call
def crawl_url(url):
    print 'crawling url'
    base_url = urlparse(url).netloc
    website, created = Website.objects.get_or_create(url=base_url)
    update_robots_txt_if_necessary(website)
    rerp = RobotExclusionRulesParser()
    rerp.parse(website.robots_content)
    if rerp.is_allowed('*', '/foo.html'):
        webpage, created = Webpage.objects.get_or_create(url=url, website=website)
        # update webpage content
        if created or not crawled_recently(webpage):
            response = urllib2.urlopen(url)
            html = response.read()
            #webpage.content = str(html)  # 8-bit to unicode
            webpage.content = unicode(html, 'unicode-escape')
            webpage.save()
            updated = True
        else: # Already have page
            updated = False
        return (webpage, updated)
    else:
        Webpage.objects.filter(url=url).delete()
        return (None, False)

# get links from a block of html
def get_links(html):
    print 'getting links'
    soup = BeautifulSoup(html)
    return soup.find_all('a')

# breadth-first recusive url search
# input a domain and then get that and all subdomains
# when first called, set base_url = current_url
def crawl_url_subdomains(base_url, num_left=20):
    print 'crawling url subdomains'
    links = [str(base_url)]
    i = 0
    while(i <= len(links)):
        print 'crawling recursive, i=%s' % i
        webpage, updated = crawl_url(links[i])
        if updated:
            # TODO add sleep command here
            num_left -= 1
        if webpage:
            html = webpage.content
            links.extend(get_links(html))
        i += 1

