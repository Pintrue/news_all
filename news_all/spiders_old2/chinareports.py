#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 17:26
# @Author  : wjq
# @File    : chinareports.py


from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class ChinareportsSpider(NewsRCSpider):
    """中国报道杂志"""
    name = 'chinareports'
    mystart_urls = {
        'http://ctsc.chinareports.org.cn/szyw/': 1301587,  # 中国报道杂志-时政要闻-左侧列表
        # 'http://sdjd.chinareports.org.cn/dfdt/': 1301296,   #  中国报道杂志-深度解读-地方动态  打不开
    }
    rules = (
        # http://ctsc.chinareports.org.cn/szyw/2019/0618/5732.html
        # http://ctsc.chinareports.org.cn/szyw/2019/0611/5605.html
        # http://ctsc.chinareports.org.cn/szyw/2019/0716/6173.html
        Rule(LinkExtractor(allow=(r'ctsc.chinareports.org.cn/szyw/%s\d{2}/\d+.html' % datetime.today().strftime('%Y/%m'),),
                           deny=(r'/list\w+.htm',)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(
            allow=(r'ctsc.chinareports.org.cn.*?\d+.html',),
            deny=(
                r'/201[0-8]', r'/2019/0[1-9]', r'/2019-0[1-9]', r'/2019_0[1-9]', r'/20190[1-9]',
                '/index.htm', r'/list\w+.htm',)
            ),
             process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            sidv = xp('//div[@class="time"]')[0]
            pubtime = sidv.re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')[0]  # 发布时间：2019-06-05 17:05 来源：中国报道
            og = sidv.re(r'来源：\w+')
            origin_name = og[0] if og else ""
            content_div = xp('//div[@class="row article"]/p')
            content, media, _, _ = self.content_clean(content_div,
                                                      kill_xpaths='//img[contains(@src, "5-1Z6051G0035R.jpg")]/parent::p')
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('-')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
