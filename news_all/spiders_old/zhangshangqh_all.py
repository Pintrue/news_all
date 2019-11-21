# -*- coding: utf-8 -*-

import json
from datetime import datetime
from scrapy import Request
from news_all.spider_models import NewsRCSpider


class Zhangshangqh_allSpider(NewsRCSpider):
    # 掌上青海
    name = 'zsqh'
    
    mystart_urls = {
        # 'http://cmswebv3.aheading.com/api/Article/List?ClassifyIdx=8566&ClassifyType=4&IsFound=0&NewspaperIdx=8905&PageIndex=1&PageSize=15&Type=0': 1302089,
        # 掌上青海  #pass 得到的并非最终url
        'http://cmswebv3.aheading.com/api/Article/List?ClassifyIdx=0&ClassifyType=4&IsFound=0&NewspaperIdx=8905&PageIndex=1&PageSize=15&Type=0': 1302088,
        # 掌上青海
        
    }
    
    def parse(self, response):
        rj = json.loads(response.text)
        result1 = rj.get('TopArticle')
        result2 = rj.get("ArticleList")
        print(result1)
        print(result2)
        for i in result1:
            url = i.get("Url")

            title = i.get("Title")
            origin_name = ""
            pubtime = ""
            yield Request(
                url=url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                      "origin_name": origin_name,
                      
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )
        for j in result2:
            url = j.get("Url")
            title = j.get("Title")
            origin_name = j.get("SourceUrl")
            pubtime = j.get("PostDateTimeFormat")
            yield Request(
                url=url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                      "origin_name": origin_name,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )
    
    def parse_item(self, response):
        try:
            content_div = response.xpath('//div[@id="imgChange"]')[0]
            pubtime = response.request.meta['pubtime'] or \
                      response.xpath("//h2/span[@class='fl']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            
                
            origin_name = response.xpath("//h2/span[@class='fl fl-margin']/text()").extract_first()
        except:
            return self.parse_item_2(response)
        
        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=pubtime,
            origin_name=response.request.meta['origin_name'],
            
            content=content,
            media=media,
            videos=videos,
        )
    
    def parse_item_2(self, response):
        # https://mp.weixin.qq.com/s/jMLjWObI1rUhkWPfGu2_mg
        try:
            content_div = response.xpath('//h2[@id="activity-name"]')[0]
            pubtime = response.request.meta['pubtime'] or response.xpath(
                "//em[@id='publish_time']/text()").extract_first()
            
                
            origin_name = response.xpath("//span[@id='profileBt']/a[@id='js_name']/text()").extract_first()
        except:
            return self.produce_debugitem(response, "xpath error")
        
        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=pubtime,
            origin_name=response.request.meta['origin_name'],
            
            content=content,
            media=media,
            videos=videos,
        )
