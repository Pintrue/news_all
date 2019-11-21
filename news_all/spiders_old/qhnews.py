# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class QhnewsSpider(NewsRCSpider):
    '''青海新闻网'''
    name = 'qhnews'
    mystart_urls = {
        'http://www.qhnews.com/newscenter/yc/': 1301223,  # 青海新闻网 本网原创
        'http://www.qhnews.com/qhly/tpbd/': 1301224,  # 青海新闻网 本网原创
    }
    rules = (
        # http://www.qhnews.com/newscenter/system/2019/06/18/012906665.shtml
        # http://www.qhnews.com/qhly/system/2019/04/17/012858330.shtml
        Rule(LinkExtractor(
            allow=(r'qhnews.com/[a-z]+/system/%s/\d{2}/\d+\.s?html' % datetime.today().strftime('%Y/%m'),), ),
             callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//span[@class="zi14hei"]/text()').extract_first()
            content_div = xp('//div[@id="zoom"]')[0]
            # 过滤视频

            
            pubtime = xp('//td[@class="hui12"][2]/div/text()')[1].extract().strip()
            
                
            origin_name = xp('//td[@class="hui12"][1]/div/text()').extract_first()
        
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
            title = xp('//h1[@id="ArticleTitle"]/text()').extract_first()
            content_div = xp('//div[@id="ArticleContent"]')[0]
            # 过滤视频

            # if self.video_filter(content_div) or self.page_turn_filter(content_div):
            #     return
            pubtime = xp('//span[@id="ArticleCreatedAt"]/text()').extract_first().strip()
            
                
            origin_name = xp('//span[@id="ArticleSource"]/a/text()').extract_first().strip()
        
        except:
            return self.parse_item_3(response)
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
    
    def parse_item_3(self, response):
        
        xp = response.xpath
        try:
            title = xp('//h1[@id="title1"]/text()').extract_first()
            content_div = xp('//div[@id="zoom"]')[0]
            # 过滤视频

            
            pubtime = xp('//div[@class="abstract ta_c"]/text()')[5].extract().strip()
            
                
            origin_name = ''
        
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
