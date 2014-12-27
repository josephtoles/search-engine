from django.conf.urls import url, include
import web.views
from django.contrib import admin
from rest_framework import routers
import api.views

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'searches', api.views.SearchViewSet)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', web.views.home_view, name='home'),
    url(r'^login/$', web.views.login_view, name='login'),
    url(r'^account/$', web.views.account_view, name='account'),
    url(r'^search/(?P<id>[0-9]+)/$', web.views.search_view, name='search'),

    # not sure exactly
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

    # Django REST framework
    url(r'^api/', include(router.urls), name='api'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # url(r'^$', 'search.views.home', name='home'),
    # url(r'^search/', include('search.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
