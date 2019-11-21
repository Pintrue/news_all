#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 17:26
# @Author  : wjq
# @File    : sdchina.py

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class SdchinaSpider(NewsRCSpider):
    """中国山东网"""
    name = 'sdchina'
    mystart_urls = {
        'http://tour.sdchina.com/list/1205.html': 1301630,  # 中国山东网-旅游
        'http://auto.sdchina.com/list/1.html': 1301631,  # 中国山东网-汽车-业界资讯
    }
    
    rules = (
        # http://tour.sdchina.com/show/4416277.html
        # http://auto.sdchina.com/news/201906/326350.html
        Rule(LinkExtractor(
            allow=(r'tour.sdchina.com/show/\d+.html',
                   r'auto.sdchina.com/news/%s/\d+.html' % datetime.today().strftime('%Y%m'),),
        ),
            callback='parse_item', follow=False),
        
        Rule(LinkExtractor(
            allow=(r'sdchina.com*?\d+.s?htm',),
            deny=(r'/201[0-8]', r'/20190[1-9]', r'/2019-0[1-9]', r'/2019_0[1-9]', r'/20190[1-9]', '/index.htm',
                  )
        ),
            process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            sidv = xp('//*[@class="zleftc"]')[0]
            ps = sidv.re(r'\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}') or sidv.re(
                r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}')
            pubtime = ps[0]  # 2019/6/23 22:56:59   来源：人民人亡
            og = sidv.re(r'来源：\s?\w+')
            origin_name = og[0] if og else ""
            content_div = xp('//div[@class="zleftf"]')[0]
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('_')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
