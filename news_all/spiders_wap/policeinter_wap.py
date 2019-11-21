# -*- coding: utf-8 -*-

from news_all.spider_models import NewsRSpider
from scrapy.conf import settings
import json
from scrapy import Request


class PoliceinterAppSipder(NewsRSpider):
    """人民公安报 app"""
    name = 'policeinter_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    sleep_time = 60000
    mystart_urls = {
            'http://gabapp.cn/Policeinterface/user!findNewsListByColumuId.action?page=1&rows=10&columuId=26': 3456,   #  APP端-中央媒体移动端-人民公安报-头条
            'http://gabapp.cn/Policeinterface/user!findNewsListByColumuId.action?page=1&rows=10&columuId=27': 3457,   #  APP端-中央媒体移动端-人民公安报-热点
            'http://gabapp.cn/Policeinterface/user!findNewsListByColumuId.action?page=1&rows=10&columuId=28': 3458,   #  APP端-中央媒体移动端-人民公安报-微说
            'http://gabapp.cn/Policeinterface/user!findNewsListByColumuId.action?page=1&rows=10&columuId=39': 3459,   #  APP端-中央媒体移动端-人民公安报-警事
            'http://gabapp.cn/Policeinterface/user!findNewsListByColumuId.action?page=1&rows=10&columuId=228': 3460,   #  APP端-中央媒体移动端-人民公安报-奇案
    }

    def parse(self, response):
        rs = json.loads(response.body)
        rows = rs.get("rows")
        for j in rows:
            try:
                title = j.get("title")
                origin_name = j.get("source")
                newsId = j.get("newsId")
                detail_url = 'http://gabapp.cn/Policeinterface/user!loadNewsContentHtml.action?newsId=' + str(newsId)
                pubtime = j.get("publishTime")
            except:
                return self.produce_debugitem(response, "json error")
            yield Request(
                url=detail_url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'],'title':title,'origin_name':origin_name,'pubtime':pubtime,
                      
                      'start_url_time': response.meta.get('start_url_time'),
                      'schedule_time': response.meta.get('schedule_time')}
            )

    def parse_item(self, response):
        try:
            content_div = response.xpath('.//body')[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        content, media, videos, video_cover = self.content_clean(content_div,kill_xpaths=['//body/div', ])
        return self.produce_item(response=response,  # 一定要写response=response, 不能是response
                                 title=response.meta.get('title'),
                                 pubtime=response.meta.get('pubtime'),
                                 origin_name=response.meta.get('origin_name'),
                                 content=content,
                                 media=media,
                                 )
