# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Nea_allSpider(NewsRCSpider):
    """国家能源局"""
    name = 'nea'
    mystart_urls = {
        'http://www.nea.gov.cn/xwzx/nyyw.htm': 7633,  # 国家能源局
    }
    rules = (
        # http://www.nea.gov.cn/2019-06/24/c_138169494.htm
        
        Rule(LinkExtractor(allow=(r'nea.gov.cn.*?/c_\d+.htm')
                           ), callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='titles']/text()").extract_first()
            # source = xp("//div[@class='pageHead']/h3")[0]
            content_div = xp("//div[@class='article-content']")[0]
            pubtime = xp("//span[@class='times']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//span[@class='author']/text()").extract_first('')
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
