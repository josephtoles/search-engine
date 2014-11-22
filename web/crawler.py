import robotexclusionrulesparser
import time
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
    try:
        return website.robots_updated + UPDATE_ROBOTS_TIME_DELTA > datetime.now(UTC())
    except TypeError:  # something to do with internal datetimes
        print 'caught internal time error'
        return False
        
# update robots.txt if it's been a while since the last time.
def update_robots_txt_if_necessary(website):
    print 'handling robots.txt'
    if not robots_txt_updated_recently(website):
        robots_url = urljoin('http://' + website.url, 'robots.txt')
        print 'robots_url is %s' % robots_url
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
def crawl_url(url, website, force=False):
    http_error_count = 0
    update_robots_txt_if_necessary(website)
    rerp = RobotExclusionRulesParser()
    rerp.parse(website.robots_content)
    if rerp.is_allowed('*', '/foo.html'):
        print 'trying website=%s and url=%s' % (website, url)
        webpage, created = Webpage.objects.get_or_create(url=url, website=website)
        # update webpage content
        if created or force or not crawled_recently(webpage):
            print 'opening url %s' % url
            if url.startswith('/'):  # TODO clean up this hack
                url = urljoin('http://' + website.url, url)
            try:
                response = urllib2.urlopen(url)
                html = response.read()
                #webpage.content = str(html)  # 8-bit to unicode
                webpage.content = unicode(html, 'unicode-escape')
                webpage.save()
                updated = True
            except ValueError:  # urllib2 unknown url type
                webpage.delete()
                return (None, False)
            except urllib2.HTTPError:  # urllib2 503 error
                http_error_count += 1
                print 'http_error_count is %s' % http_error_count
                webpage.delete()
                return (None, False)
        else: # Already have page
            updated = False
        return (webpage, updated)
    else:
        Webpage.objects.filter(url=url).delete()
        return (None, False)

# get links from a block of html
def get_links(html, website):
    urls = []
    soup = BeautifulSoup(html)
    links = soup.find_all('a')

    for tag in links:
        link = tag.get('href',None)
        if link != None:
            urls.append(link)

    # remove external links to other websites
    indices = range(0, len(urls))
    indices.reverse()
    for i in indices:
        netloc = urlparse(urls[i]).netloc
        if netloc and netloc != website.url:
            del(urls[i])

    # TODO 
    return urls

# breadth-first recusive url search
# input a domain and then get that and all subdomains
# when first called, set base_url = current_url
def crawl_url_subdomains(url, num_left=20):
    base_url = urlparse(url).netloc
    website, created = Website.objects.get_or_create(url=base_url)
    if not base_url:
        raise ValueError('base_url cannot be blank')
    print 'crawling url subdomains'
    links = [str(url)]
    i = 0
    while(i <= len(links) and num_left >= 0):
        print 'crawling recursive, i=%s of %s' % (i, len(links))
        print 'num_left=%s' % num_left
        webpage, updated = crawl_url(links[i], website, i==0)
        if updated:
            time.sleep(1)  # randomize
        if updated:
            # TODO add sleep command here
            num_left -= 1
        if webpage:
            html = webpage.content
            links.extend(get_links(html, webpage.website))
        i += 1

