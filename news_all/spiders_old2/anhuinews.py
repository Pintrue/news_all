#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 17:26
# @Author  : wjq
# @File    : anhuinews.py


from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from news_all.spider_models import NewsRCSpider, otherurl_meta


class AnhuinewsSpider(NewsRCSpider):
    """中国安徽在线"""
    name = 'anhuinews'
    mystart_urls = {
        'http://sports.anhuinews.com/': 1301583,  # 中国安徽在线-体育-列表
        'http://news.anhuinews.com/shh/shhxw/': 1301582,  # 中国安徽在线-社会新闻列表
        'http://auto.anhuinews.com/qcxw/ctzx/': 1301581,  # 中国安徽在线-车坛资讯
    }
    rules = (
        # http://sports.anhuinews.com/system/2019/06/14/008164106.shtml
        Rule(LinkExtractor(allow=(r'anhuinews.com.*?/%s/\d{2}/\d+.shtml' % datetime.today().strftime('%Y/%m'),),
                           # deny=(r'',)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'anhuinews.com.*?\d+.s?htm',), deny=(r'/201[0-8]', r'/2019/0[1-9]')
                           ),
             process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            pubtime = xp('/html/head/meta[@name="publishdate"]/@content').extract_first()
            content_div = xp('.//div[@class="info"]')[0]
            ogs = xp('//div[@class="source"]//text()').extract()
            origin_name = ogs[1] if len(ogs) > 1 else ""
            content, media, _, _ = self.content_clean(content_div)
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('-')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
