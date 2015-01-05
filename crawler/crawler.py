from random import random
import time
from bs4 import BeautifulSoup
import urllib2
from robotexclusionrulesparser import RobotExclusionRulesParser
from urlparse import urlparse, urljoin
from datetime import datetime
from models import Website, Webpage


# Flow
# When crawl_url is called, exactly one new link should be acquired from the website



#############
# FUNCTIONS #
#############

# Input an entire url
# This extracts the local path from url
# so if you input 'http://www.amazon.com/hello' then it would return '/hello'
# Note: url must begin with 'http' or 'https' or this will return an erroneous result.
def parse_url(url):
    if not url.startswith('http'):
        raise ValueError('url {url} could not be parsed'.format(url=url))
    return urlparse(url).path


# eliminates bad urls like javascript.void(0) and truncates off query parameters
# return boolean representing whether url can be used appropriately
def is_a_local_url(url):
    if '(' in url or ')' in url:  # quick hack to avoid what seems to be a JavaScript function
        return False
    if '?' in url:
        return False
    if not url.startswith('/'):
        return False
    return True


# add a single url to the database from a website
# returns False if no url can be added
def crawl_website(website):
    website.update_robots_txt()  # only updates if necessary
    rules = RobotExclusionRulesParser()
    rules.parse(website.robots_content)

    #TODO add check for site last updated timestamp

    # Has the index been retrieved yet?
    if not website.webpage_set.exists():
        # get index
        if rules.is_allowed('*', '/'):
            webpage = Webpage.objects.create(
                local_url='/',
                robots_allowed=True,
                website=website,
            )
            crawl_existing_webpage(webpage, rules)
        else:
            # create a placeholder index webpage
            webpage = Webpage.objects.create(
                local_url='/',
                robots_allowed=False,
                website=website,
            )
            return None

    # Are there webpages to be accessed?
    allowed_webpages = website.webpage_set.filter(robots_allowed=True)
    if not allowed_webpages.exists():
        return None

    # Are there new links to try out?
    new_webpages = allowed_webpages.filter(exists=None)
    if new_webpages.exists():
        # start with the oldest first
        # created and updated are the same for newly-created webpages
        webpage = new_webpages.order_by('created').first()
        return crawl_existing_webpage(webpage, rules)

    # Crawl an existing webpage
    if rules.is_allowed('*', '/foo.html'):
        webpage = allowed_webpages.filter(exists=True).order_by('updated')
        return crawl_existing_webpage(webpage, rules)


# does not check whether webpage has been updated recently
# rules is the robotexclusionrulesparser to be compared against
# returns the webpage model, after update
# returns None if the webpage could not be crawled
# TODO make this a class method for webpage
def crawl_existing_webpage(webpage, rules):
    print 'crawling webpage {webpage} from site {website}'.format(webpage=webpage.local_url,
                                                                  website=webpage.website.url)

    if rules.is_allowed('*', webpage.local_url):
        full_url = urljoin('http://' + webpage.website.url, webpage.local_url)
        try:
            response = urllib2.urlopen(full_url)
            html = response.read()
            parse_links(webpage.website, html)
            webpage.content = unicode(html, 'unicode-escape')
            webpage.exists = True
            webpage.save()
            return webpage
        except urllib2.URLError:  # url not accessible
            print 'webpage {full_url} does not exist'.format(full_url=full_url)
            webpage.exists = False
            webpage.save()
            return webpage
        # The following exceptions are included as a backup measure
        # They should not be necessary is input is properly cleaned first
        except ValueError:  # urllib2 unknown url type (ex #lkjsdf, I think maybe)
            print 'ValueError: webpage {full_url} does not exist'.format(full_url=full_url)
            webpage.exists = False
            webpage.save()
            return webpage
        except urllib2.HTTPError:  # urllib2 503 error
            print 'HTTPError: webpage {full_url} does not exist'.format(full_url=full_url)
            webpage.exists = False
            webpage.save()
            return webpage
    else:
        return None


# adds links from html to website
def parse_links(website, html):
    urls = []
    soup = BeautifulSoup(html)
    links = soup.find_all('a')

    for tag in links:
        link = tag.get('href', None)
        if link is not None:  # must handle '' and None differently
            urls.append(link)

    for url in urls:
        if is_a_local_url(url):  # TODO handle absolute urls to same website
            if not website.webpage_set.filter(local_url=url).exists():
                Webpage.objects.create(
                    local_url=url,
                    exists=None,
                    website=website,
                )
