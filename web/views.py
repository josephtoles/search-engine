from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from forms import URLForm
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader


def home_view(request):
    context = {}
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            context['root'] = url
            # crawl target url
            # get list of sub-pages and add them to content
    else:
        form = URLForm() # An unbound form
    context['form'] = form
    return render_to_response('home.html', context, RequestContext(request))
