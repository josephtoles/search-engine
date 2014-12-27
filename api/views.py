import rest_framework.permissions
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from brain.models import Search
from brain.serializers import SearchSerializer
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseBadRequest
import json
import rest_framework.permissions
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm


def logout_view(request):
    logout(request)
    return HttpResponse()


def login_view(request):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        auth_login(request, form.get_user())
        return HttpResponse()
    else:
        return HttpResponseBadRequest(json.dumps(form.errors.items()), content_type='application/json')



class SearchViewSet(ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    # permission_classes = (,)  # add later
    permission_classes = (rest_framework.permissions.AllowAny,)
    filter_backends = (filters.OrderingFilter,)

    def pre_save(self, obj):
        print 'pre-saving'
        if obj:
            print 'there is an object'
            obj.creator = self.request.user
