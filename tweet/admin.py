from django.contrib import admin
from tweet.models import TwitterProfile, Tweet

admin.site.register(TwitterProfile)
admin.site.register(Tweet)
