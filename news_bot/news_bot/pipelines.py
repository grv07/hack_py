# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import NewsBotItem, CommentBotItem
from news.models import News, Comment


class NewsBotPipeline(object):
    last_save_news_obj = {}

    def process_item(self, item, spider):
        if isinstance(item, NewsBotItem):
            news_id = item['hn_id_code']
            try:
                from datetime import datetime
                obj = News.objects.get(hn_id_code=news_id)
                obj.page = 1
                obj.rank = item.get('rank', 0)
                obj.total_comments = item.get('total_comments', 0)
                obj.score = item.get('score', 0)
                obj.latest_created_time = datetime.now()
                obj.save()
                item = obj
            except Exception as e:
                # try:
                #     obj = News.objects.get(rank=item.get('rank'), page=1)
                #     obj.page = 2
                #     obj.save()
                # except Exception as e:
                #     print e.args
                item['page'] = 1
                item = item.save()
            self.last_save_news_obj.setdefault(str(news_id), [item, None])

        elif isinstance(item, CommentBotItem):
            news_id = item['news_id']
            try:
                item = Comment.objects.get(hn_id_code=item['hn_id_code'])
            except Exception as e:
                item['news'] = self.last_save_news_obj[str(news_id)][0]
                item['parent_comment'] = self.last_save_news_obj[str(news_id)][1]
                item = item.save()
            self.last_save_news_obj[str(news_id)][1] = item
        return item

