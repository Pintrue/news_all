# -*- coding: utf-8 -*-

import json
from datetime import datetime
from scrapy.conf import settings
from scrapy import Request
from news_all.spider_models import NewsSpider


class ZgmtbSpider(NewsSpider):
    """中国煤炭报 app"""
    name = 'zgmtb_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    # todo check columnStyle=201 或 203 的区别
    mystart_urls = {
        'http://203.187.176.75:8080/app_if/getArticles?columnId=591&version=0&lastFileId=0&page=0&adv=1&columnStyle=201': 2953,
        # APP端-中央媒体移动端-中国煤炭报-头条
        'http://203.187.176.75:8080/app_if/getArticles?columnId=592&version=0&lastFileId=0&page=0&adv=1&columnStyle=203': 2954,
        # APP端-中央媒体移动端-中国煤炭报-视频
        'http://203.187.176.75:8080/app_if/getArticles?columnId=594&version=0&lastFileId=0&page=1&adv=1&columnStyle=201': 2955,
        # APP端-中央媒体移动端-中国煤炭报-企业
        'http://203.187.176.75:8080/app_if/getArticles?columnId=595&version=0&lastFileId=0&page=1&adv=1&columnStyle=201': 2956,
        # APP端-中央媒体移动端-中国煤炭报-政策
        'http://203.187.176.75:8080/app_if/getArticles?columnId=630&version=0&lastFileId=0&page=0&adv=1&columnStyle=201': 2957,
        # APP端-中央媒体移动端-中国煤炭报-经济
    }
    
    def parse(self, response):
        rj = json.loads(response.text)
        if isinstance(rj, list):
            print()
        result = rj.get('list')
        for i in result:
            url = i.get("shareUrl")

            title = i.get("title")
            origin_name = i.get("source")
            pubtime = i.get("publishtime")
            videoUrl = i.get("videoUrl")

            yield Request(
                url=url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title,
                      'pubtime': pubtime,
                      'videoUrl': videoUrl,
                      "origin_name": origin_name,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )
    
    def parse_item(self, response):
        videoUrl = response.meta.get("videoUrl")
        if videoUrl:
            videos = {'1': {'src': videoUrl}}
            content = '<div>#{{1}}#</div>'
            media = {}
        else:
            xp = response.xpath
            try:
                cvs = xp('//div[@class="text-article"]/div[@class="content"]') or xp('//div[@class="content-main"]')
                content_div = cvs[0]
            except:
                return self.produce_debugitem(response, "xpath error")
            content, media, videos, video_cover = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=response.meta.get("title"),
            pubtime=response.meta.get("pubtime"),
            origin_name=response.meta.get("origin_name"),
            content=content,
            media=media,
            videos=videos,
        )


class ZgmtbGSpider(ZgmtbSpider):
    """中国煤炭报 app 观察者"""
    name = 'zgmtb_wap_gcz'
    
    mystart_urls = {
        'http://203.187.176.75:8080/app_if/leaderView?start=0&count=20&siteId=2': 2958,  # APP端-中央媒体移动端-中国煤炭报-观察家
    }
    sleep_time = 60*60*24*2
    custom_settings = {'DEPTH_LIMIT': 2}
    
    list_api = 'http://203.187.176.75:8080/app_if/getArticles?columnId={}&version=0&lastFileId=0&page=0&adv=1&columnStyle=201'
    
    def parse(self, response):
        rj = json.loads(response.text)
        if not isinstance(rj, list):
            return self.produce_debugitem(response, 'json error')
        column_ids = [i['columnID'] for i in rj]
        # print(column_ids)
        # [636, 649, 634, 654, 639, 633, 652, 641, 637, 647, 646, 645, 640, 638, 642, 648, 644, 650, 651, 653]
        for c in column_ids:
            yield Request(
                url=self.list_api.format(c),
                callback=self._parse_list,
                meta={'source_id': response.meta['source_id'],
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time'),
                      'isStartUrl': True},
                dont_filter=True,
            )

    def _parse_list(self, response):
        return super(ZgmtbGSpider, self).parse(response)