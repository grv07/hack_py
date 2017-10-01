# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from news.models import News, Comment


class NewsBotItem(DjangoItem):
    # define the fields for your item here like:
    hn_id_code = scrapy.Field()
    django_model = News


class CommentBotItem(DjangoItem):
    # define the fields for your item here like:
    news_id = scrapy.Field()
    django_model = Comment
