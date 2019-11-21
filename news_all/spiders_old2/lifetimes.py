# -*- coding: utf-8 -*-


from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class LifetimesSpider(NewsRCSpider):
    '''生命时报'''
    name = 'lifetimes'
    mystart_urls = {
        'http://www.lifetimes.cn/cyjj/': 1301044,  # 生命时报 产业经济-左侧列表
    }
    rules = (
        # http://www.lifetimes.cn/cyjj/2019-06/15046932.html
        Rule(LinkExtractor(allow=(r'lifetimes.cn/cyjj/\d{4}-\d{2}/\d+\.html'),
                           ), callback='parse_item',
             follow=False),
    )
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='list_text bor01']/h1/text()").extract_first()
            content_div = xp("//div[@id='con']")[0]
            pubtime = xp("//div[@class='mess']/span[1]/text()").extract_first().strip()
            origin_name = xp("//div[@class='mess']/span[2]/text()").extract_first()
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
