from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from forms import URLForm
from django.views.decorators.csrf import csrf_exempt


#@csrf_exempt  # TODO remove this when you figure out how to get CSRF to work
def home_view(request):
    print 'getting home view'
    if request.method == 'POST':
        print 'request is POST'
        form = URLForm(request.POST)
        if form.is_valid():
            print 'form is valid'
            # set search url here
            print form.cleaned_data['url']
            return render_to_response('home.html', {'form': form})
        print 'form is not valid'
        return render_to_response('home.html', {'form': form})
    else:
        print 'method is not POST'
        form = URLForm() # An unbound form
        return render_to_response('home.html', {'form': form})

