from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from forms import URLForm
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader


def home_view(request):
    print 'getting home view'
    if request.method == 'POST':
        print 'request is POST'
        form = URLForm(request.POST)
        if form.is_valid():
            print 'form is valid'
            # set search url here
            print form.cleaned_data['url']
        print 'form is not valid'
    else:
        print 'method is not POST'
        form = URLForm() # An unbound form
    return render_to_response('home.html', {'form': form}, RequestContext(request))
