# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class XxhgabSpider(NewsRCSpider):
    '''工业和信息化部'''
    name = 'xxhgab'
    mystart_urls = {
        "http://www.miit.gov.cn/n1146290/n4388791/index.html": 7608,
    }
    rules = (
        # http://www.miit.gov.cn/n1146290/n4388791/c7015722/content.html
        # http://www.mps.gov.cn/n2254098/n4904352/c6548322/content.html
        Rule(LinkExtractor(allow=(r'gov.cn/n\d+/n\d+/c\d+/content\.html',),
                           deny=(r'http://miit.gov.cn/n1146322/n1147103/c4508890/content.html'),
                           ), callback='parse_item',
             follow=False),
    )
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@id='con_title']/text()").extract_first()
            content_div = xp("//div[@id='con_con']")[0]
            pubtime = xp("//span[@id='con_time']/text()").re(r'\d{4}-\d{2}-\d{2}')[0]
            origin_name = xp("//div[@class='cinfo center']/span[2]/text()").extract_first()
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
