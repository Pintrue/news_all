# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Safe_allSpider(NewsRCSpider):
    """国家外汇管理局"""
    name = 'safe'
    mystart_urls = {
        'http://www.safe.gov.cn/safe/whxw/index.html': 7638,  # 国家外汇管理局
        'http://www.safe.gov.cn/safe/ywfb/index.html': 7639,  # 国家外汇管理局
    }
    rules = (
        # http://www.safe.gov.cn/safe/2019/0621/13485.html
        Rule(LinkExtractor(allow=(r'safe.gov.cn.*?/\d{4}/\d{4}/\d+.html'),
                           ), callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='detail_tit']/text()").extract_first()
            # source = xp("//div[@class='pageHead']/h3")[0]
            content_div = xp("//div[@id='content']")[0]
            pubtime = xp("//div[@class='condition']/ul/li[4]/dd").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//li[@id='ly_li']/dd[@id='ly']/text()").extract_first('')
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
