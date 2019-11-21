# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class TqwSpider(NewsRCSpider):
    """天气网"""
    name = 'tqw'
    mystart_urls = {
        'https://www.tianqi.com/news/list_404_1.html': 1302264,   #  天气网
    }
    rules = (
        #https://www.tianqi.com/news/248423.html
        Rule(LinkExtractor(allow=(r'tianqi.com.*?/\d+.html'),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='left']/h1/text()").extract_first()
            source = xp("//div[@class='time']")[0]
            content_div = xp("//div[@class='texts']")[0]

            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            
            
            origin_name =xp('//div[@class="time"]/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )
