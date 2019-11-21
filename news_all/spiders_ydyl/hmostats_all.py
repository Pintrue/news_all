# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Hmostats_allSpider(NewsRCSpider):
    """国务院港澳事务办公室&国家统计局"""
    name = 'hmostats'
    mystart_urls = {
        'http://www.hmo.gov.cn/xwzx/ndsgayw/': 7625,  # 国务院港澳事务办公室
        'http://www.hmo.gov.cn/xwzx/gayw/': 7626,  # 国务院港澳事务办公室
        'http://www.hmo.gov.cn/xwzx/zwyw/': 7627,  # 国务院港澳事务办公室
        'http://www.stats.gov.cn/tjsj/zxfb/': 7623,  # 国家统计局
        'http://www.stats.gov.cn/tjsj/sjjd/': 7624,  # 国家统计局
    }
    rules = (
        # http://www.hmo.gov.cn/xwzx/gayw/201905/t20190516_20878.html
        # http://www.hmo.gov.cn/xwzx/ndsgayw/201905/t20190523_20913.html
        # http://www.stats.gov.cn/tjsj/zxfb/201906/t20190624_1671928.html
        # http://www.stats.gov.cn/tjsj/sjjd/201906/t20190614_1670402.html
        
        Rule(LinkExtractor(allow=(r'(?:hmo|stats).gov.cn.*?/\d{6}/t\d+_\d+.html'),
                           ), callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='pageHead']/h2/text()").extract_first()
            source = xp("//div[@class='pageHead']/h3")[0]
            content_div = xp("//div[@class='detailCon']")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//div[@class='pageHead']/h3/text()").extract_first('')
        except:
            return self.parse_item_2(response)
        
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    # http://www.stats.gov.cn/tjsj/sjjd/201906/t20190614_1670402.html
    def parse_item_2(self, response):
        
        xp = response.xpath
        try:
            title = xp("//h2[@class='xilan_tit']/text()").extract_first()
            source = xp("//font[@class='xilan_titf']/font")[0]
            # content_div = xp("//p[@class='MsoNormal']")[0]
            content_div = xp("//div[@class='TRS_PreAppend']")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//font[@class='xilan_titf']/font/font/text()").extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media
        )
