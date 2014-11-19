from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from forms import URLForm
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
from crawler.crawler import get_pages
from crawler.models import Website
from urlparse import urlparse
from datetime import datetime


def home_view(request):
    context = {}
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            # Get url
            url = form.cleaned_data['url']
            context['root'] = url
            pages = get_pages(url)
            print 'pages are %s' % str(pages)
            # crawl target url
            # get list of sub-pages and add them to content

            # Robots testing
            print 'listing'
            for site in Website.objects.all():
                print site.url
            site = Website.objects.get(url=urlparse(url).netloc)
            robots_updated = site.robots_updated
            context['robots_last_updated'] = robots_updated
            context['current_time'] = datetime.now()
    else:
        form = URLForm() # An unbound form
    context['form'] = form
    return render_to_response('home.html', context, RequestContext(request))
