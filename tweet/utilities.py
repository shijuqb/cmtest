from tweet.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import re
import twitter
import os


def assert_author(function):
    """
    Decorator function to check whether logged-in user is author
    """
    def check_is_author(request, *args, **kwargs):
        logged_in_user = get_object_or_404(User, id=request.user.id)
        if logged_in_user.twitter_profile.level == '2':
            return function(request, *args, **kwargs)
        else:
            return HttpResponse('Permission Denied')
    return check_is_author


def assert_editor(function):
    """
    Decorator function to check whether logged-in user is editor
    """
    def check_is_editor(request, *args, **kwargs):
        logged_in_user = get_object_or_404(User, id=request.user.id)
        print logged_in_user.twitter_profile.level
        if logged_in_user.twitter_profile.level == '1':
            return function(request, *args, **kwargs)
        else:
            return HttpResponse('Permission Denied')
    return check_is_editor


def is_dirty(*args, **kwargs):
    """
        function should be called with 'content' as argument,
        which will hold the content to be checked for dirty words
    """
    if 'content' in kwargs and kwargs['content']:
        # get current directory
        app_dir = os.path.dirname(__file__)
        # get bad words file
        bad_words_file = os.path.join(app_dir, 'bad_words.txt')
        # open bad word file for line by line read
        with open(bad_words_file, 'r') as f:
            for bad_word in f:
                bad_word = bad_word.strip().replace(' ', '\D*')
                pattern = re.compile(r'\b('+bad_word+')\\b', re.I,)
                print pattern.pattern
                dirty = re.search(pattern, kwargs['content'])
                if not dirty:
                    dirty = re.search(r'\b[A-Z]+\b', kwargs['content'])
                return dirty
    else:
        return None


def brand_correct_tweet(*args, **kwargs):
    """
        function should be called with 'content' as argument,
        which will hold the content to be checked for brand correction
    """
    if 'content' in kwargs and kwargs['content']:
        content = kwargs['content']
        branding_dict = {('consumer', 'Consumer'): 'Buyer',
                         ('maker', 'subscriber', 'Subscriber'): 'Maker',
                         ('Custom Made', 'custom made', 'Custommade', 'customade', 'Customade'): 'CustomMade',
                         ('admin', 'back end', 'backend'): 'Dashboard',
                         ('conback', 'ConBack', 'Con back'): 'Buyer Dashboard',
                         ('subback', 'SubBack', 'Subback'): 'Maker Dashboard'}
        flag = False
        for i, j in branding_dict.iteritems():
            for item in i:
                if item in content.split(' '):
                    content = content.replace(item, j)
                    if not flag:
                        flag = True
        return (content, flag)
    else:
        return None


def paginate(query_set=None, page=None, per_page_count=None):
    """
        paginate query_set and return paginated query_set
    """
    if not per_page_count:
        per_page_count = 10
    paginator = Paginator(query_set, per_page_count)
    try:
        paginated_query_set = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_query_set = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_query_set = paginator.page(paginator.num_pages)
    return paginated_query_set


def get_twitter_api():
    """
        create and return twitter api object
    """
    api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                              consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                              access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
                              access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
    return api
