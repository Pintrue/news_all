#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 10:50
# @Author  : wjq
# @File    : beijing_review.py

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class TyrbSpider(NewsRCSpider):
    """太原日报"""
    name = 'tyrb'
    mystart_urls = {
        'http://paper.tywbw.com/jyxw/': 1301497,  # 太原日报 教育列表
    }
    rules = (
        # http://paper.tywbw.com/jyxw/c/2019-06/26/content_150341.htm
        Rule(LinkExtractor(allow=(r'paper.tywbw.com/jyxw/c/%s/\d{2}/content_\d+.htm' % datetime.today().strftime('%Y-%m'),),
                           # deny=(r'',)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'paper.tywbw.com/jyxw.*?\d+.s?htm',), deny=(r'/201[0-8]', r'/2019/0[1-9]', r'index_\d+.htm')
                           ),
             process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            sidv = xp('//p[@class="ly"]')[0]
            pubtime = sidv.re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')[0]  # 2019-06-26 07:29:35
            content_div = xp('//div[@class="detail"]')[0]
            og = sidv.re(r'来源：\w+')  # 来源：太原晚报
            origin_name = og[0] if og else "太原晚报"
            content, media, _, _ = self.content_clean(content_div)
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")
        
        return self.produce_item(
            response=response,
            title=xp('//h1/text()').extract_first('') or self.get_page_title(response).split('-')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
