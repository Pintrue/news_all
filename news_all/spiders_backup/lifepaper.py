# -*- coding: utf-8 -*-
import json
from scrapy import Request
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings


class LifePaperSpider(NewsRSpider):
    # 生命时报
    name = 'life_paper'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        'http://interfacev5.vivame.cn/x1-interface-v5/json/newdatalist.json?uid=15385469&type=1&id=167072': 411,  # 首页
        'http://interfacev5.vivame.cn/x1-interface-v5/json/newdatalist.json?uid=15385469&type=1&id=563058': 412,  # 海外
        'http://interfacev5.vivame.cn/x1-interface-v5/json/newdatalist.json?uid=15385469&type=1&id=734767': 413,  # 生活
        'http://interfacev5.vivame.cn/x1-interface-v5/json/newdatalist.json?uid=15385469&type=1&id=149358': 414,  # 养老
    }

    def parse(self, response):
        rs = json.loads(response.text)
        if str(rs.get('code')) != 0:
            return self.produce_debugitem(response, 'json error')

        data = rs.get('data')
        banner = data.get('banner')
        banner_items = banner.get('items')
        feedlist_items = []

        for i in data.get('feedlist'):
            feedlist_items.extend(i.get('items'))

        for i in banner_items+feedlist_items:
            news_url = i.get('fileurl')
            pubtime = i.get('time')

            title = i.get('title')
            yield Request(
                url=news_url,
                callback=self.parse_item,
                meta={'source_id':response.meta['source_id'], 'title':title, 'pubtime':pubtime,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )

    def parse_item(self, response):
        try:
            content_div = response.xpath("//div[@id='aMain']/div[@class='text']")[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name='生命时报',
            content=content,
            media=media,
            videos=videos
        )