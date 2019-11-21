# -*- coding: utf-8 -*-

from scrapy import Request
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings
import json


class ZgyjWapSpider(NewsRSpider):
    '''中国应急管理报 app'''
    name = 'zgyjglb_app'
    
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        'http://203.187.176.75:8080/app_if/getArticles?columnId=332&version=0&lastFileId=0&page=0&adv=1&columnStyle=201': 3072,
        'http://203.187.176.75:8080/app_if/getArticles?columnId=340&version=0&lastFileId=0&page=1&adv=1&columnStyle=203': 3073,
        'http://203.187.176.75:8080/app_if/getArticles?columnId=813&version=0&lastFileId=0&page=0&adv=1&columnStyle=201': 3074,
        'http://203.187.176.75:8080/app_if/getArticles?columnId=337&version=0&lastFileId=0&page=0&adv=1&columnStyle=201': 3075,
        'http://203.187.176.75:8080/app_if/getArticles?columnId=339&version=0&lastFileId=0&page=0&adv=1&columnStyle=201': 3076,
        'http://203.187.176.75:8080/app_if/getArticles?columnId=722&version=0&lastFileId=0&page=0&adv=1&columnStyle=201': 3077,
        'http://203.187.176.75:8080/app_if/getArticles?columnId=338&version=0&lastFileId=0&page=0&adv=1&columnStyle=201': 3078,
        'http://203.187.176.75:8080/app_if/getArticles?columnId=343&version=0&lastFileId=0&page=1&adv=1&columnStyle=201': 3079,
    }
    
    def parse(self, response):
        res = response.text
        resJson = json.loads(res)
        items = resJson['list']
        for i in items:
            # url = i.get('shareUrl')  # https://mp.weixin.qq.com/s/sR6SKrYyTEoC4Py82oziQw
            url = i.get('contentUrl') or i.get('shareUrl')
            #  http://www.aqsc.cn:8080/app_if/getArticleContent?articleId=111688&colID=332

            title = i.get('title')
            pubtime = i.get('publishtime')

            yield Request(
                url=url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')
                      }
            )
    
    def parse_item(self, response):
        try:
            rj = json.loads(response.text)
            content_div = rj['content']
            origin_name = rj['source']
        except:
            try:
                xp = response.xpath
                origin_name = xp("//div[@class='content-details']/span[@class='source']/text()").extract_first()
                content_div = xp('//div[@class="content-main"]')[0]
            except:
                return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content_div, need_video=True)
        return self.produce_item(
            response=response,
            title=response.meta.get("title"),
            pubtime=response.meta.get("pubtime"),
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )
