from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from forms import URLForm
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
from crawler import crawl_url, crawl_url_subdomains
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
            pages = crawl_url_subdomains(url, num_left=5)

            # get links
            site = Website.objects.get(url=urlparse(url).netloc)
            context['links'] = Webpage.objects.filter(website=site).all()[:10]
    else:
        form = URLForm() # An unbound form
    context['form'] = form
    return render_to_response('home.html', context, RequestContext(request))
