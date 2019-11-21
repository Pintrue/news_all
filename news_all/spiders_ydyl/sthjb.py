# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class SthjbSpider(NewsRCSpider):
    '''生态环境部'''
    name = 'sthjb'
    mystart_urls = {
        "http://www.mee.gov.cn/xxgk/xwfb/": 7613,
    }
    rules = (
        # http://www.mee.gov.cn/xxgk2018/xxgk/xxgk15/201906/t20190625_707658.html
        # http://www.mee.gov.cn/xxgk2018/xxgk/xxgk15/201906/t20190624_707535.html
        Rule(LinkExtractor(allow=(r'mee.gov.cn/xxgk\d+/xxgk/xxgk\d+/\d{6}/t\d{8}_\d+\.html',),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='content_body']/h1/text()").extract_first()
            content_div = xp("//div[@class='Custom_UnionStyle']")[0]
            pubtime = xp("//div[@class='content_top_box']/ul/li[3]/div[2]/text()").extract_first().strip()
            origin_name = xp("//div[@class='content_top_box']/ul/li[3]/div[1]/text()").extract_first()
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='content_body']/h1/text()").extract_first()
            content_div = xp("//p[@class='Custom_UnionStyle']")[0]
            pubtime = xp("//div[@class='content_top_box']/ul/li[3]/div[2]/text()").extract_first().strip()
            origin_name = xp("//div[@class='content_top_box']/ul/li[3]/div[1]/text()").extract_first()
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
