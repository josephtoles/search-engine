from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from management import commands
from multiprocessing import Process
from django.core.management import call_command
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from forms import URLForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
from crawler import crawl_url, crawl_url_subdomains, mark_to_crawl
from models import Website, Webpage
from urlparse import urlparse
from datetime import datetime


def account_view(request):
    context = {'user': request.user}
    return render_to_response('account.html', context, RequestContext(request))

def home_view(request):
    context = {}
    context['user'] = request.user
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
            found = mark_to_crawl(url)
            if not found:
                context['not_found'] = 'Site not found'
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

def login_view(request):
    def errorHandle(error):
        form = LoginForm()
        return render_to_response('login_view.html', {
                'error' : error,
                'form' : form,
        })
    if request.method == 'POST': # If the form has been submitted...
        print 'method is post'
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            print 'form is valid'
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # Redirect to a success page.
                    login(request, user)
                    return render_to_response('account.html', {
                        'user': request.user,
                    }, RequestContext(request))
                else:
                    # Return a 'disabled account' error message
                    error = u'account disabled'
                    return errorHandle(error)
            else:
                 # Return an 'invalid login' error message.
                error = u'invalid login'
                return errorHandle(error)
        else: 
            print 'form is invalid'
            error = u'form is invalid'
            return errorHandle(error)       
    else:
        print 'method is not post'
        form = LoginForm() # An unbound form
        return render_to_response('login_view.html', {'form': form}, RequestContext(request))
