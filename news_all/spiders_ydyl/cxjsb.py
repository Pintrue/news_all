# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class CxjsbSpider(NewsRCSpider):
    '''住房和城乡建设部'''
    name = 'cxjsb'
    mystart_urls = {
        "http://www.mohurd.gov.cn/xwfb/index.html": 7614,
    }
    rules = (
        # http://www.mohurd.gov.cn/xwfb/201906/t20190618_240898.html
        # http://www.mohurd.gov.cn/jsbfld/201906/t20190624_240951.html
        Rule(LinkExtractor(allow=(r'mohurd.gov.cn/[a-z]+/\d{6}/t\d{8}_\d+\.html',),
                           deny=(r'http://www.mohurd.gov.cn/xwfb/201906/t20190618_240898.html',
                                 r'http://www.mohurd.gov.cn/jsbfld/201905/t20190521_240625.html',
                                 r'http://www.mohurd.gov.cn/gywz/200804/t20080424_162520.html')
                           ), callback='parse_item',
             follow=False),
    )
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//td[@class='tit']/text()").extract_first()
            content_div = xp("//div[@class='union']")[0]
            pubtime = xp("//div[@class='union']/p[last()]/text()").re(r'\d{4}.\d{2}.\d{2}')[0]
            origin_name = xp("//div[@class='union']/p[last()]/text()").extract_first().split('\u3000')[1]
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
    def parse_item_2(self, response):
        
        xp = response.xpath
        try:
            title = xp("//td[@class='tit']/text()").extract_first()
            content_div = xp("//div[@class='union']")[0]
            pubtime = xp("//div[@class='union']/p[last()-1]/text()").re(r'\d{4}.\d{2}.\d{2}')[0]
            
                
            origin_name = xp("//div[@class='union']/p[last()-1]/text()").extract_first().split('\u3000')[1]
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
