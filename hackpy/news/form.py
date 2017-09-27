from django import forms
from django.forms import ModelForm
from models import *


class NewsForm(ModelForm):
    hn_user = forms.CharField(required=True, show_hidden_initial=True)

    class Meta:
        model = News
        fields = ['story_text', 'link_href', 'hn_user']


class CommentForm(ModelForm):
    news_id = forms.IntegerField(required=True)
    reply_nested_level = forms.IntegerField(required=False)
    parent_comment_id = forms.IntegerField(required=False)
    is_reply = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = Comment
        fields = ['hn_user', 'text', 'news_id', 'reply_nested_level', 'is_reply',
                  'parent_comment_id']