# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class News(models.Model):
    story_text = models.CharField(max_length=255)
    link_href = models.CharField(max_length=255)
    hn_user = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    show_on_site = models.BooleanField(default=True)

    class Meta:
        ordering = ['rank']

    def __str__(self):
        print self.story_text
        return self.story_text

    def __unicode__(self):
        return self.story_text


class Comment(models.Model):
    news = models.ForeignKey(News, null=False)
    hn_user = models.CharField(max_length=50, null=False)
    text = models.TextField(null=False, blank=False)
    age = models.CharField(max_length=50, null=False)
    score = models.IntegerField(default=0)
    is_reply = models.BooleanField(default=False)
    reply_nested_level = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    parent_comment = models.ForeignKey('news.Comment', null=True)

    show_on_site = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['parent_comment__id', 'created_time']

    def __unicode__(self):
        return self.text

# Create your models here.
