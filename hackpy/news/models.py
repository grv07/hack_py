# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User
import utils


class News(models.Model):
    story_text = models.CharField(max_length=255)
    link_href = models.CharField(max_length=255)
    hn_user = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    show_on_site = models.BooleanField(default=True)
    is_crawled = models.BooleanField(default=True)
    hn_id_code = models.CharField(max_length=150)
    page = models.IntegerField(default=1)

    created_time = models.DateTimeField(auto_now_add=True)
    latest_created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['page', 'rank', '-created_time']

    def __str__(self):
        return self.story_text

    def __unicode__(self):
        return self.story_text

    def get_time_diff(self):
        return utils.get_time_diff(self)


class Comment(models.Model):
    news = models.ForeignKey(News, null=False)
    hn_user = models.CharField(max_length=50, null=False)
    text = models.TextField(null=False, blank=False)
    age = models.CharField(max_length=50, null=False)
    score = models.IntegerField(default=0)
    is_reply = models.BooleanField(default=False)
    reply_nested_level = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    is_crawled = models.BooleanField(default=True)
    parent_comment = models.ForeignKey('news.Comment', null=True)
    hn_id_code = models.CharField(max_length=150)

    show_on_site = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_time', 'parent_comment__id']

    def __unicode__(self):
        return self.text

    def save(self, *args, **kwargs):
        if self.news and not self.is_crawled:
            self.news.total_comments += 1
            self.news.save()
        super(Comment, self).save(*args, **kwargs)

    def get_time_diff(self):
        return utils.get_time_diff(self)


class UpVoteCounter(models.Model):
    count = models.IntegerField(default=1)
    user = models.ForeignKey(User)
    news = models.ForeignKey(News, null=True)
    comment = models.ForeignKey(Comment, null=True)


@receiver(pre_delete, sender=Comment)
def _mymodel_delete(sender, instance, **kwargs):
    if instance.news:
        instance.news.total_comments -= 1
        instance.news.save()

# Create your models here.
