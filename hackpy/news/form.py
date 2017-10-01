from django import forms
from django.forms import ModelForm
from models import *


class NewsForm(ModelForm):
    # hn_user = forms.CharField(required=True, widget=forms.HiddenInput)
    link_href = forms.URLField(required=True)
    story_text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = News
        fields = ['link_href', 'story_text']


class CommentForm(ModelForm):
    news_id = forms.IntegerField(required=True)
    reply_nested_level = forms.IntegerField(required=False)
    parent_comment_id = forms.IntegerField(required=False)
    is_reply = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = Comment
        fields = ['hn_user', 'text', 'news_id', 'reply_nested_level', 'is_reply',
                  'parent_comment_id']


class RegisterForm(forms.Form):
    user_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()

