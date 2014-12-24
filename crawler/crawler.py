from random import random
import time
from bs4 import BeautifulSoup
import urllib2
from robotexclusionrulesparser import RobotExclusionRulesParser
from urlparse import urlparse, urljoin
from datetime import datetime
from models import Website, Webpage

# custom django commands
# https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
# http://stackoverflow.com/questions/4291895/django-should-i-kick-off-a-separate-process
# use call_command, extract to a Process http://stackoverflow.com/questions/13239087/django-multiprocessing-oddity


#############
# FUNCTIONS #
#############

# eliminates bad urls like javascript.void(0) and truncates off query parametersw
# reurns boolean representing whether url can be used appropriately
def parse_url(url):
    return urlparse(url).path


def url_is_valid(url):
    if '(' in url or ')' in url:  # quick hack to avoid what seems to be a JavaScript function
        return False
    return True


def mark_to_crawl(url):
    base_url = urlparse(url).netloc
    if base_url.startswith('www.'):  # TODO clean up this hack
        base_url = base_url[len('www.'):]
    website, created = Website.objects.get_or_create(url=base_url, defaults={'robots_updated': datetime.now()})
    if not base_url:
        raise ValueError('base_url cannot be blank. (url is {url})'.format(url=url))
    webpage, updated = crawl_url(url, website)
    webpage.last_human_request = datetime.now()
    webpage.save()
    return webpage  # returns None if webpage not found


# add a single url to the database if necessary
# returns a tuple (webpage, updated)
# where webpage is the webpage (None if not accessible)
# and created is a boolean representing whether the webpage was actually fetched with this call
def crawl_url(url, website, force=False):
    website.update_robots_txt()
    rerp = RobotExclusionRulesParser()
    rerp.parse(website.robots_content)
    if rerp.is_allowed('*', '/foo.html'):
        url = parse_url(url)
        if not url_is_valid(url):
            return (None, False)
        print '\ntrying website=%s and url=%s' % (website.url, url)
        webpage, created = Webpage.objects.get_or_create(url=url, website=website)
        # update webpage content
        if created or force or not webpage.crawled_recently:
            print 'opening url %s' % url
            if url.startswith('/'):  # TODO clean up this hack
                url = urljoin('http://' + website.url, url)
            try:
                response = urllib2.urlopen(url)
                html = response.read()
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
        else:  # Already have page updated = False
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
        link = tag.get('href', None)
        if link is not None:  # must handle '' and None differently
            urls.append(link)

    # remove external links to other websites
    indices = range(0, len(urls))
    indices.reverse()
    for i in indices:
        netloc = urlparse(urls[i]).netloc
        if netloc and netloc != website.url:
            del(urls[i])

    # TODO more code goes here
    return urls


# breadth-first recusive url search
# input a domain and then get that and all subdomains
# when first called, set base_url = current_url
def crawl_url_subdomains(url, num_left=5, max_tries=1000):
    print 'crawling url subdomains'
    base_url = urlparse(url).netloc
    if base_url.startswith('www.'):  # dirty hack
        base_url = base_url[len('www.'):]
    website, created = Website.objects.get_or_create(url=base_url)
    if not base_url:
        raise ValueError('base_url cannot be blank. (url is {url})'.format(url=url))
    links = [str(url)]
    i = 0
    while(i < len(links) and num_left >= 0 and max_tries >= 0):
        print 'crawling recursive, i=%s of %s, max_tries=%s' % (i, len(links), max_tries)
        print 'num_left=%s' % num_left
        webpage, updated = crawl_url(links[i], website, i == 0)
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
