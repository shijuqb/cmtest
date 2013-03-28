from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #redirecting to tweet app
    url(r'^$', lambda x: HttpResponseRedirect(reverse('index'))),
    url(r'^tweet/', include('tweet.urls')),
    url(r'login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
