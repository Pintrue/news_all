#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 10:50
# @Author  : wjq
# @File    : my399.py

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class My399Spider(NewsRCSpider):
    """哈尔滨新闻网-体育"""
    name = 'my399'
    mystart_urls = {
        'http://news.my399.com/sports/': 1301413,  # 哈尔滨新闻网-体育
    }
    rules = (
        # http://news.my399.com/sports/content/2019-06/24/content_2444807.htm
        Rule(LinkExtractor(
            allow=(r'news.my399.com/sports/content/%s/\d{2}/content_\d+.htm' % datetime.today().strftime('%Y-%m'),),
            # deny=(r'',)
            ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'my399.com.*?\d+.s?htm',),
                           deny=(r'/201[0-8]', r'/2019/0[1-9]', r'/2019-0[1-9]', r'/node_\d+.htm', r'index_\d+.htm')
                           ),
             process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            sdiv = xp('//div[@class="n10"] | //span[@class="n10"]')[0]
            pubtime = sdiv.re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')[0]  # 2019-06-24 11:17
            content_div = xp('//div[@id="newscontent"]')[0]

            origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first("")
            content, media, _, _ = self.content_clean(content_div)
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")
            
        return self.produce_item(
            response=response,
            title=self.get_page_title(response).replace('|my399.com', ''),
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
