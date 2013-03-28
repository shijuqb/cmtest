from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TwitterProfile(models.Model):
    USER_TYPE = (
        ('1', 'editor'),
        ('2', 'author')
    )
    """holds additional fields of a user"""
    user = models.OneToOneField(User, unique=True, related_name='twitter_profile')
    level = models.CharField(max_length=20, choices=USER_TYPE, blank=False, null=False)

    def __unicode__(self):
        return self.user.username


class Tweet(models.Model):
    tweet_id = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=140)
    created_by = models.ForeignKey(User, related_name='tweets')
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    is_dirty = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content[:20]+"..."
