# -*- coding: utf-8 -*-
import json
from scrapy import Request
from news_all.spider_models import NewsRSpider


class YongpiSpider(NewsRSpider):
    name = 'yongpi'
    mystart_urls = {
        'http://pi.cnnb.com.cn/yongpai_api/yh/get_news_list?lastModify=0&pageNo=1&pageSize=20&channelid=32': 1301915,
    # 甬派-教育
        'http://pi.cnnb.com.cn/yongpai_api/yh/get_news_list?lastModify=1533262689373&pageNo=1&pageSize=20&channelid=0': 1301914,
    # 甬派-焦点
    }
    
    def parse(self, response):
        rj = json.loads(response.text)
        data = rj.get('data', [])
        if not data:
            return self.produce_debugitem(response, 'json error')
        
        for item in data:
            url = item.get("url")
            try:
                title = item.get("title")
                origin_name = item.get("name")
                pubtime = item.get("updatetime")

                yield Request(
                    url=url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,"origin_name":origin_name,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )
            except:
                yield self.produce_debugitem(response, 'json error')
 
    def parse_item(self, response):
        xp = response.xpath
        try:
            content_div = xp("//div[@id='content']")[0] \
                          # or xp('//div[@class="cnt_bd"]')[0] \
                          # or xp('//div[@class="main-text-container"]/section')[0]
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
