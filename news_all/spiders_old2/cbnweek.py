#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 9:31
# @Author  : wjq
# @File    : cbnweek.py


import logging
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from news_all.spider_models import NewsRCSpider, otherurl_meta


class CbnweekSpider(NewsRCSpider):
    """第一财经周刊"""
    name = 'cbnweek'
    mystart_urls = {
        'https://www.cbnweek.com/': 1301148,  # 第一财经周刊 资讯
    }
    rules = (
        # https://www.cbnweek.com/articles/normal/23699
        Rule(LinkExtractor(allow=(r'cbnweek.com/articles/normal/\d+',),
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'cbnweek.com.*?\d+',),
                           deny=(r'/topics/', r'/theme/', r'/magazine/' )
                           ),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            pubtime = xp('//*[@class="article-time"]/text()')[0].extract()
            
            
            content_div = xp('////div[@class="article-content"]')[0]

        except Exception as e:
            return self.produce_debugitem(response, "xpath error")
        title = xp('//h1/text()').extract_first('')
        content, media, _, _ = self.content_clean(content_div)
    
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="第一财经杂志",

            content=content,
            media=media
        )
