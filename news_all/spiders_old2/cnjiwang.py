#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 17:08
# @Author  : wjq
# @File    : cnjiwang.py


from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class CnjiwangSpider(NewsRCSpider):
    """中国吉林网"""
    name = 'cnjiwang'
    mystart_urls = {
        'http://auto.cnjiwang.com/cx/': 1301594,  # 中国吉林网-汽车资讯
        # 'http://eat.cnjiwang.com/stx/': 1301297,  # 中国吉林网-食天下  旧新闻
    }
    
    rules = (
        # http://auto.cnjiwang.com/cx/201906/2903027.html
        Rule(LinkExtractor(
            allow=(r'auto.cnjiwang.com.*?/%s/\d+.htm' % datetime.today().strftime('%Y%m'),),
            # deny=(r'',)
            ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(
            allow=(r'auto.cnjiwang.com.*?\d+.htm',),
            deny=(
                r'/201[0-8]', r'/20190[1-9]/', r'/2019-0[1-9]', r'/2019_0[1-9]', r'/20190[1-9]/',
                '/index.htm', r'/list\w+.htm',)
        ),
            process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            sidv = xp('//div[@class="zxdata mt20"]')[0]
            pubtime = sidv.re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')[0]  # 2019-06-21 14:11
            content_div = xp('//div[@class="content"]/p')
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('-')[0],
            pubtime=pubtime,
            content=content,
            media=media
        )