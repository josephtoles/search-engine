from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .permissions import IsStaffOrTargetUser
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm


def logout_view(request):
    logout(request)
    return HttpResponse()


def login_view(request):
    print '\n\nhit login view'
    form = AuthenticationForm(request, data=request.POST)
    import pdb; pdb.set_trace()
    if form.is_valid():
        print 'form is valid'
        auth_login(request, form.get_user())
        return HttpResponse()
    else:
        print 'form is not valid'
        return HttpResponseBadRequest(json.dumps(form.errors.items()), content_type='application/json')



class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User
 
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),