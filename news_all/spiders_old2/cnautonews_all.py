# -*- coding: utf-8 -*-

import json
from datetime import datetime
from scrapy import Request
from news_all.spider_models import NewsRCSpider



class CnautonewsAllSpider(NewsRCSpider):
    name = 'cnautonews_all'
    
    mystart_urls = {
        'http://www.cnautonews.com/xrw/doc_3070.json?timestamp=1531791573609': 1301069,  # 中国汽车报-人物
        'http://www.cnautonews.com/tj/doc_3070.json?timestamp=1531741240210': 1301067,  # 中国汽车报-推荐
        'http://www.cnautonews.com/gd/doc_3070.json?timestamp=1531791294058': 1301068,  # 中国汽车报-观点
    }
    
    def parse(self, response):
        rj = json.loads(response.text)
        result = rj.get('lists')
        for i in result:
            url = i.get("link")
            title = i.get("title")
            origin_name = i.get("source")
            pubtime = i.get("date")
            yield Request(
                url=url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                      "origin_name": origin_name,
                      
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )
    
    def parse_item(self, response):
        try:
            content_div = response.xpath('.//div[@class="news-d-main"]/div[@class="TRS_Editor"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        
        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            
            content=content,
            media=media,
            videos=videos,
        )
