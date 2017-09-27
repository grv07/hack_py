# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import NewsBotItem, CommentBotItem


class NewsBotPipeline(object):
    last_save_news_obj = {}

    def process_item(self, item, spider):
        if isinstance(item, NewsBotItem):
            news_id = item['comment_url_id']
            item = item.save()
            self.last_save_news_obj.setdefault(str(news_id), [item, None])

        elif isinstance(item, CommentBotItem):
            news_id = item['news_id']
            item['news'] = self.last_save_news_obj[str(news_id)][0]
            item['parent_comment'] = self.last_save_news_obj[str(news_id)][1]
            item = item.save()
            self.last_save_news_obj[str(news_id)][1] = item
        return item

