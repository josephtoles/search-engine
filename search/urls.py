# from django.conf.urls import patterns, include
from django.conf.urls import url
import web.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', web.views.home_view, name='home'),
    url(r'^login/$', web.views.login_view, name='login'),
    url(r'^account/$', web.views.account_view, name='account'),
    url(r'^search/(?P<id>[0-9]+)/$', web.views.search_view, name='search'),

    # Django REST framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

    # url(r'^$', 'search.views.home', name='home'),
    # url(r'^search/', include('search.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
