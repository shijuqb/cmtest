from django.forms import ModelForm, Textarea, CharField
from tweet.models import Tweet
from django import forms


# Create the form class.
class TweetForm(ModelForm):
    content = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'cols': 30, 'rows': 5, 'maxlength': 140}))

    class Meta:
        model = Tweet
        exclude = ('tweet_id', 'created_by', 'created_at', 'is_dirty')
