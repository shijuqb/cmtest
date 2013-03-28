from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tweet.models import Tweet, TwitterProfile
from tweet.forms import TweetForm
from tweet.utilities import *
from django.core.urlresolvers import reverse
from django.contrib import messages
import twitter


@login_required
def index(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    try:
        user_level = request.user.twitter_profile.level
        page_num = request.GET.get('page')
        twitter_api = get_twitter_api()
        #editor
        if user_level == '1':
            q_reviewed = request.GET.get('is_reviewed', 0)
            tweets = Tweet.objects.filter(is_reviewed=q_reviewed).order_by('-created_at')
            # paginate tweets
            tweets = paginate(query_set=tweets, page=page_num, per_page_count=10)
            # loop to retrieve retweet count
            for tweet in tweets:
                if tweet.tweet_id:
                    try:
                        tweet.retweet_count = twitter_api.GetStatus(tweet.tweet_id).retweet_count
                    except:
                        tweet.retweet_count = 0
                else:
                    tweet.retweet_count = 0
            if request.is_ajax():
                return render_to_response('editor/includes/tweets_list.html',
                                          {'tweets': tweets, 'is_reviewed': q_reviewed},
                                          context_instance=RequestContext(request))
            else:
                return render_to_response('editor/index.html',
                                          {'tweets': tweets, 'is_reviewed': q_reviewed},
                                          context_instance=RequestContext(request))
        #author
        else:
            tweet_form = TweetForm()
            tweets = Tweet.objects.filter(is_reviewed=True,
                                          created_by=request.user).order_by('-created_at')
            # paginate tweets
            tweets = paginate(query_set=tweets, page=page_num, per_page_count=None)
            # loop to retrieve retweet count
            for tweet in tweets:
                if tweet.tweet_id:
                    try:
                        tweet.retweet_count = twitter_api.GetStatus(tweet.tweet_id).retweet_count
                    except:
                        tweet.retweet_count = 0
                else:
                    tweet.retweet_count = 0
            if request.is_ajax():
                return render_to_response('author/includes/tweets_list.html',
                                          {'tweets': tweets},
                                          context_instance=RequestContext(request))
            else:
                corrected_tweet = request.session.get('brand_corrected_tweet', None)
                original_tweet = request.session.get('content', None)
                if 'brand_corrected_tweet' in request.session:
                    request.session.__delitem__('brand_corrected_tweet')
                    request.session.__delitem__('content')
                    messages.add_message(request, messages.INFO, "Your tweet content has been brand corrected: '"+original_tweet+"'")    
                return render_to_response('author/index.html',
                                          {'tweets': tweets, 'corrected_tweet': corrected_tweet,
                                          'original_tweet': original_tweet,
                                          'form': tweet_form},
                                          context_instance=RequestContext(request))
    #logged in user is neither author nor editor
    except TwitterProfile.DoesNotExist:
        return render_to_response('permission_denied.html', context_instance=RequestContext(request))


def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')


@assert_author
def post_tweet(request, message=None, *args, **kwargs):
    """
        post tweet and re-direct user to the main page
    """  
    tweet_content = request.POST['content']
    tweet_form = TweetForm({'content': tweet_content})
    if tweet_form.is_valid():
        if is_dirty(content=tweet_content):
            messages.add_message(request, messages.ERROR, 'Shame on you')
            #save tweet
            tweet = tweet_form.save(commit=False)
            tweet.created_by = request.user
            tweet.save()
        else:
            brand_corrected = brand_correct_tweet(content=request.POST['content'])
            brand_corrected_tweet = brand_corrected[0]
            brand_corrected_flag = brand_corrected[1]
            if brand_corrected_flag:
                request.session.__setitem__('brand_corrected_tweet', brand_corrected_tweet)
                request.session.__setitem__('content', request.POST['content'])
                return HttpResponseRedirect(reverse('index'))
            else:
                api = get_twitter_api()
                try:
                    status = api.PostUpdate(tweet_content)
                    messages.add_message(request, messages.SUCCESS, 'Your tweet has been posted')
                    #save tweet
                    tweet = tweet_form.save(commit=False)
                    tweet.created_by = request.user
                    tweet.tweet_id = status.id
                    if not is_dirty(content=tweet_content):
                        tweet.is_reviewed = True
                    tweet.save()
                except Exception, e:
                    print e
                    messages.add_message(request, messages.ERROR, 'Same tweet content already posted')
    return HttpResponseRedirect(reverse('index'))
