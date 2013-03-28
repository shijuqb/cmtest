from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url


urlpatterns = patterns('tweet.views',
    url(r'^$', 'index', name='index'),
    url(r'^post/$', 'post_tweet', name='tweet'),
)