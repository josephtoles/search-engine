import robotexclusionrulesparser
from random import random
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
        return datetime.now() - website.robots_updated < UPDATE_ROBOTS_TIME_DELTA
    except TypeError:  # something to do with internal datetimes
        return datetime.now(UTC()) - website.robots_updated < UPDATE_ROBOTS_TIME_DELTA
        
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

# eliminates bad urls like javascript.void(0) and truncates off query parametersw
# reurns boolean representing whether url can be used appropriately
def parse_url(url):
    return urlparse(url).path

def url_is_valid(url):
    if '(' in url or ')' in url:
        return False
    return True

# add a single url to the database if necessary
# returns a tuple (webpage, created)
# where webpage is the webpage (None if not accessible)
# and created is a boolean representing whether the webpage was actually fetched with this call
def crawl_url(url, website, force=False):
    update_robots_txt_if_necessary(website)
    rerp = RobotExclusionRulesParser()
    rerp.parse(website.robots_content)
    if rerp.is_allowed('*', '/foo.html'):
        url = parse_url(url)
        if not url_is_valid(url):
            return (None, False)
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
            except ValueError:  # urllib2 unknown url type (ex #lkjsdf, I think maybe)
                webpage.delete()
                return (None, False)
            except urllib2.URLError:  # urllib2 unknown url type (ex Javascript)
                webpage.delete()
                return (None, False)
            except urllib2.HTTPError:  # urllib2 503 error
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
def crawl_url_subdomains(url, num_left=5, max_tries=1000):
    base_url = urlparse(url).netloc
    if base_url.startswith('www.'):  # dirty hack
        base_url = base_url[len('www.'):]
    website, created = Website.objects.get_or_create(url=base_url)
    if not base_url:
        raise ValueError('base_url cannot be blank')
    links = [str(url)]
    i = 0
    while(i < len(links) and num_left >= 0 and max_tries >= 0):
        print 'crawling recursive, i=%s of %s' % (i, len(links))
        print 'num_left=%s' % num_left
        webpage, updated = crawl_url(links[i], website, i==0)
        if updated:
            time.sleep(0.5 + random())  # randomize
            num_left -= 1
        if webpage:
            html = webpage.content
            new_links = get_links(html, webpage.website)
            for link in new_links:  # poorly optomized
                link = parse_url(link)
                if link not in links:
                    links.append(link)
        i += 1
        max_tries -= 1

