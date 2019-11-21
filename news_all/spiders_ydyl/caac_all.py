# -*- coding: utf-8 -*-


from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Caac_allSpider(NewsRCSpider):
    """中国民用航空局"""
    name = 'caac'
    mystart_urls = {
        'http://www.caac.gov.cn/XWZX/MHYW/': 7635,  # 中国民用航空局
    }
    rules = (
        #http://www.caac.gov.cn/XWZX/MHYW/201906/t20190627_197236.html
        
        Rule(LinkExtractor(allow=(r'caac.gov.cn.*?/t\d+_\d+.html'),
                           ), callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='content_t']/text()").extract_first()
            # source = xp("//div[@class='pageHead']/h3")[0]
            content_div = xp("//div[@class='TRS_Editor']")[0]
            pubtime = xp("//span[@class='p_r10'][2]").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//span[@id='source']/text()").extract_first('')
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

