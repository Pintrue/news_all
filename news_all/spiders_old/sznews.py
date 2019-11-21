# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class SznewsSpider(NewsRCSpider):
    '''深圳新闻网'''
    # http://www.sznews.com/photo/content/2019-06/22/content_22198271.htm 图集多页没写
    name = 'sznews'
    mystart_urls = {
        'http://news.sznews.com/node_150127.htm': 19109,  # 深圳新闻网-焦点-国内
        'http://news.sznews.com/node_150128.htm': 19110,  # 深圳新闻网-焦点-国际-左下列表
        'http://news.sznews.com/node_134907.htm': 19111,  # 深圳新闻网-焦点-港澳台-左侧列表
        'http://news.sznews.com/node_31220.htm': 19112,  # 深圳新闻网-焦点-财经-左侧列表
        'http://news.sznews.com/node_18236.htm': 19100,  # 深圳新闻网-社会焦点-左侧列表
    }
    rules = (
        # http://news.sznews.com/content/2019-06/25/content_22203825.htm
        Rule(LinkExtractor(allow=(r'sznews.com/content/\d{4}-\d{2}/\d{2}/content_\d+\.htm'),
                           deny=(r'http://news.sznews.com/content/2019-06/25/content_22203028.htm',# 图集多页
                                 )
                           ), callback='parse_item',
             follow=False),
    )
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='h1-news']/text()").extract_first()
            content_div = xp("//div[@class='article-content cf new_txt']")[0]
            pubtime = xp("//div[@class='fs18 share-date l']/text()").extract_first().strip()
            
            
            origin_name = xp("//div[@class='fs18 share-date l']/span/text()").extract_first()
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
            title = xp("//h1[@class='h1-news']/text()").extract_first()
            content_div = xp("//div[@class='article-content cf new_txt']")[0]
            pubtime = xp("//div[@class='fs18 r share-date']/text()").extract_first().strip()
            
            
            origin_name = xp("//div[@class='fs18 r share-date']/span/text()").extract_first()
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
