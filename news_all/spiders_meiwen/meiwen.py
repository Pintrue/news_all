# -*- coding: utf-8 -*-


from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider
from copy import deepcopy
from scrapy.conf import settings


class meiwenspider(NewsRCSpider):
    name = 'meiwen'
    mystart_urls = {
                'http://www.666n.com/list/meiwenzhaichao.html':644,
                'http://www.666n.com/list/jingdianmeiwen.html':645,
                'http://www.666n.com/list/meiwenxinshang.html':647,
                'http://www.666n.com/list/meiwenmeiju.html':649,
                'http://www.666n.com/list/weimeiwenzi.html':650,
                'http://www.666n.com/list/youmeiwenzhang.html':652,
                'http://www.666n.com/list/zhaichaomeiwen.html':653,
                'http://www.666n.com/list/qingganmeiwen.html':687,
                'http://www.666n.com/list/meiwenshangxi.html':821,
                'http://www.666n.com/list/weimeiwenzhang.html':855,
    }

    rules = (
        Rule(LinkExtractor(allow=(r'666n.com/.*?/\d+.html'),deny=r'666n.com/html'),
        callback='parse_item', follow=False),  # 没有最后的一个,会返回TypeError: 'Rule' object is not iterable
    )
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='hd']/h2/text()").extract_first() or self.get_page_title(response).split('_')[0]
            # pubtime = xp("//span[@class='time']/text()").extract_first('')

            cv = xp("//div[@id='CntArticle']")
            content,media,_,_=self.content_clean(cv)
        except IndexError:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,  # must
            title=title,
            pubtime=datetime.now(),
            content=content,
            media=media,
        )