from management import commands
from multiprocessing import Process
from django.core.management import call_command
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from forms import URLForm
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
from crawler import crawl_url, crawl_url_subdomains, mark_to_crawl
from models import Website, Webpage
from urlparse import urlparse
from datetime import datetime


def home_view(request):
    context = {}
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            # Get url
            url = form.cleaned_data['url']

            # crawl
            # Very poorly managed. This should have some safety features
            #p = Process(target=call_command, args=('crawl_url_subdomains', url))
            #p.start()
            # you should really just create a seperate crawl command to search important domains. It should be running whenever the server is running
            mark_to_crawl(url)
            #crawl_url_subdomains(url)

            # get links
            try:
                site = Website.objects.get(url=urlparse(url).netloc)
                context['pages'] = Webpage.objects.filter(website=site).all()[:10]
            except Website.DoesNotExist:
                # add 'please wait message to output'
                pass
    else:
        form = URLForm() # An unbound form
    context['form'] = form
    return render_to_response('home.html', context, RequestContext(request))
