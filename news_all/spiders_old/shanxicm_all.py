# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Shanxichuanmei_allSpider(NewsRCSpider):
    """陕西传媒网"""
    name = 'sxcm'
    mystart_urls = {
        'http://www.sxdaily.com.cn/GB/26/508/index.html': 1301227,  # 陕西传媒网 原创-资讯聚焦
        'http://www.sxdaily.com.cn/GB/216/83/526/index.html': 1301484,  # 陕西传媒网 教育-资讯

    }
    rules = (
        #http://www.sxdaily.com.cn/n/2019/0624/c526-6500628.html
        Rule(LinkExtractor(allow=(r'sxdaily.com.cn/n/%s\d{2}/c\d{3}-\d+.html' % datetime.today().strftime('%Y/%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='container title']/h1/text()").extract_first()
            content_div = xp("//div[@class='content']")[0]
            pubtime = xp("//div[@class='container title']/div/p[1]").re(r'\d{2,4}年\d{1,2}月\d{1,2}日')[0]
            
            
            origin_name = xp("//div[@class='container title']/div/p[2]/text()").extract_first('')
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

    #http://www.sxdaily.com.cn/n/2019/0621/c508-6500226.html
    def parse_item_2(self, response):
        
        xp = response.xpath
        try:
            title = xp("//div[@class='text width1000 clearfix']/h1/text()").extract_first()
            content_div = xp("//div[@class='text width1000 clearfix']")[0]
            pubtime = xp("//div[@class='text width1000 clearfix']/h3").re(r'\d{2,4}年\d{1,2}月\d{1,2}日')[0]
            

            
            origin_name = xp("//div[@class='text width1000 clearfix']/h3/text()").extract_first('')
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

