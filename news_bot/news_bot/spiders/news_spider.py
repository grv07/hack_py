from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
import scrapy, urlparse
from news_bot.items import NewsBotItem, CommentBotItem


def represents_int(s):
    try:
        if s:
            int(s)
            return True
        raise ValueError
    except ValueError:
        return False


class CommentSpider(BaseSpider):
    name = "comment"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = ['news.ycombinator.com/item?id=15318440']

    @classmethod
    def update_start_url(cls, value):
        cls.start_urls.append(value)
        return cls.start_urls

    def parse(self, response):
        print 'parse begain for ------'
        print self.start_urls


class ExampleSpider(BaseSpider):
    name = "example"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = ['https://news.ycombinator.com/news']
    comment_url = []

    @staticmethod
    def get_default_row_dict():
        base_k_list = ['rank', 'story_text', 'total_comments', 'link_href', 'hn_user',
                         'age', 'score', 'hn_id_code']
        return dict(zip(base_k_list, [None]*len(base_k_list)))

    def parse_comment(self, response):
        description = response.xpath("//table[@class='comment-tree']/tr").extract()[:100]
        yield response.meta["item"]
        for i, v in enumerate(description):
            comment_dict = {}
            if not comment_dict.setdefault('hn_user', None):
                value = Selector(text=v).xpath('//div/span[@class="comhead"]/a/text()').extract_first()
                comment_dict['hn_user'] = value
            if not comment_dict.setdefault('hn_id_code', None):
                value = Selector(text=v).xpath('//div[@class="reply"]/p/font/u/a/@href').extract_first()
                par = urlparse.parse_qs(urlparse.urlparse(value).query) if value else {'id': [0]}
                comment_dict['hn_id_code'] = par.get('id', [0])[0]
            if not comment_dict.setdefault('text', None):
                value = Selector(text=v).xpath('//div[@class="comment"]/span/text()').extract_first('')
                value += Selector(text=v).xpath('//div[@class="comment"]/span/i/text()').extract_first('')
                value += Selector(text=v).xpath('//div[@class="comment"]/span/p/text()').extract_first('')
                comment_dict['text'] = value if value else 'NA'
            if not comment_dict.setdefault('age', None):
                value = Selector(text=v).xpath('//span/span[@class="age"]/a/text()').extract_first()
                value = value if value else ''
                comment_dict['age'] = value
            if not comment_dict.setdefault('is_reply', False):
                value = Selector(text=v).xpath('//td[@class="ind"]/img/@width').extract_first()
                value = int(value) if value else 0
                if  value > 0:
                    comment_dict['is_reply'] = True
                    comment_dict['reply_nested_level'] = value if value >= 40 else 0
                else:
                    comment_dict['reply_nested_level'] = 0
            comment_dict['news_id'] = response.meta['news_id']
            item = CommentBotItem(comment_dict)
            yield item

    def parse(self, response):
        description = response.xpath("//table[@class='itemlist']/tr[not(re:test(@class, "
                                     "'(spacer)'))]").extract()
        row = self.get_default_row_dict()
        # print description
        for i, v in enumerate(description):
            index = i
            if not row['rank']:
                value = Selector(text=v).xpath('//td[1]/span[@class="rank"]/text()').extract_first()
                row['rank'] = int(value.replace('.', '')) if value else 0

            if not row['story_text']:
                value = Selector(text=v).xpath('//td[3]/a[@class="storylink"]/text()').extract_first()
                row['story_text'] = value.encode("utf8") if value else ''

            if not row['link_href']:
                value = Selector(text=v).xpath('//td[3]/a[@class="storylink"]/@href').extract_first()
                # print value
                row['link_href'] = value if value else ''

            if not row['hn_user']:
                value = Selector(text=v).xpath('//a[@class="hnuser"]/text()').extract_first()
                row['hn_user'] = value.encode("utf8") if value else ''

            if not row['age']:
                value = Selector(text=v).xpath('//span[@class="age"]/a/text()').extract_first()
                row['age'] = int(value.split(' ')[0]) if value else 0

            if not row['total_comments']:
                value = Selector(text=v).xpath(
                    '//td[@class="subtext"]/a[contains(@href, "item?id=")]/text()').extract_first()
                if value:
                    value = value.encode('ascii', 'ignore').replace('comments', '') if value else ''
                    value = value.encode('ascii', 'ignore').replace('comment', '') if value else ''
                    row['total_comments'] = int(value) if represents_int(value) else 0

            if not row['score']:
                value = Selector(text=v).xpath('//span[@class="score"]/text()').extract_first()
                row['score'] = int(value.split(' ')[0]) if value else 0

            if not row['hn_id_code']:
                value = Selector(text=v).xpath('//tr[@class="athing"]/@id').extract_first()
                row['hn_id_code'] = int(value) if represents_int(value) else 0

            if all([None for i, v in row.items() if v==None]):
                print 'Go for save >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
                data = row.copy()
                row = self.get_default_row_dict()
                self.comment_url.append('https://news.ycombinator.com/item?id=15318440')
                news_id = data['hn_id_code']
                item = NewsBotItem(data)
                yield item
                request = scrapy.Request(url='https://news.ycombinator.com/item?id='+str(news_id),
                                         callback=self.parse_comment)
                request.meta['item'] = item
                request.meta['news_id'] = int(news_id)
                yield request

            if index % 2:
                row = self.get_default_row_dict()
