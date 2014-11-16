# This is the web scraper

def crawl_url(url):
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


