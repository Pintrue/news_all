# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class ZrzybSpider(NewsRCSpider):
    '''自然资源部'''
    name = 'zrzyb'
    mystart_urls = {
        "http://www.mnr.gov.cn/dt/ywbb/": 7612,
    }
    rules = (
        # http://www.mnr.gov.cn/dt/ywbb/201906/t20190626_2442076.html
        # http://www.mnr.gov.cn/dt/ywbb/201906/t20190626_2442078.html
        Rule(LinkExtractor(allow=(r'mnr.gov.cn/dt/ywbb/\d{6}/t\d+_\d+\.html',),
                           ), callback='parse_item',
             follow=False),
    )
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h2[@id='doctitle']/text()").extract_first()
            content_div = xp("//div[@class='Custom_UnionStyle']")[0]
            pubtime = xp("//div[@class='fl clearfix ky_fx']/span[1]/text()").extract_first().strip()
            
                
            origin_name = xp("//div[@class='fl clearfix ky_fx']/span[2]/text()").extract_first()
        except:
            return self.parse_item_2(response)
        # 过滤视频


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
    def parse_item_2(self, response):
        
        xp = response.xpath
        try:
            title = xp("//h2[@id='doctitle']/text()").extract_first()
            content_div = xp("//div[@class='TRS_Editor']")[0]
            pubtime = xp("//div[@class='fl clearfix ky_fx']/span[1]/text()").extract_first().strip()
            
                
            origin_name = xp("//div[@class='fl clearfix ky_fx']/span[2]/text()").extract_first()
        except:
            return self.produce_debugitem(response, "xpath error")
            # return self.parse_item_2(response)
        # 过滤视频


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
