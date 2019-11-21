# -*- coding: utf-8 -*-
import logging
from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider, NewsCrawlSpider

import time


class CpnewsSpider(NewsRCSpider):
    """华龙网"""
    name = 'cpnews'
    mystart_urls = {
        'http://cq.cqnews.net/szjz/index.htm': 1301187,
        'http://cq.cqnews.net/jzcj/': 1301433,
        'http://car.cqnews.net/node_123312.htm': 1301188,
    }
    # http://cq.cqnews.net/html/2019-06/20/content_50522561.html
    # http://car.cqnews.net/html/2018-08/28/content_44822383.htm
    rules = (
        Rule(LinkExtractor(allow=r'cqnews\.net/html/%s.*?/content_\d+\.s?html?' % time.strftime("%Y-%m/%d"),
                           deny=('video', 'audio', 'search.php', 'zt'),
                           ),
             callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//div[@class="left_news"]/h1/text()').extract()[0].strip()
            # 2019-4-1 21:55
            pubtime = xp('//div[@class="left_news"]/div[@class="pl"]/span[1]/text()').extract()[0].strip()
            
                
            cv = xp('//div[@id="_h5_content"]')[0]
            content, media, video, cover = self.content_clean(cv)
            origin_name = xp('//span[@class="author"]').re('来源：([\w-]+)')[0]
        except:
            # return self.parse_item_2(response)
            return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media,
        )
