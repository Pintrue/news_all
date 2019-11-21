# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.conf import settings
import json
from news_all.spider_models import *
from news_all.tools.html_clean import get_query_map


class gonrenSpider(NewsRSpider):
    """工人日报 app"""
    name = 'gongren_app'
    mystart_urls = {
        'http://47.110.139.194/api/getArticles?sid=1&cid=4&lastFileID=0&rowNumber=0': 532,
        # APP端-中央媒体移动端-工人日报-首页-热点
        'http://47.110.139.194/api/getArticles?sid=1&cid=5&lastFileID=0&rowNumber=0': 534,
        # APP端-中央媒体移动端-工人日报-首页-视频
        'http://47.110.139.194/api/getArticles?sid=1&cid=6&lastFileID=0&rowNumber=0': 559,
        # APP端-中央媒体移动端-工人日报-首页-工讯
        'http://47.110.139.194/api/getArticles?sid=1&cid=7&lastFileID=0&rowNumber=0': 570,
        # APP端-中央媒体移动端-工人日报-首页-财经
        'http://47.110.139.194/api/getArticles?sid=1&cid=8&lastFileID=0&rowNumber=0': 579,
        # APP端-中央媒体移动端-工人日报-首页-锐评
        'http://47.110.139.194/api/getArticles?sid=1&cid=9&lastFileID=0&rowNumber=0': 589,
        # APP端-中央媒体移动端-工人日报-首页-图片
        'http://47.110.139.194/api/getArticles?sid=1&cid=10&lastFileID=0&rowNumber=0': 599,
        # APP端-中央媒体移动端-工人日报-首页-劳模
        'http://47.110.139.194/api/getArticles?sid=1&cid=11&lastFileID=0&rowNumber=0': 600,
        # APP端-中央媒体移动端-工人日报-首页-职场
        'http://47.110.139.194/api/getArticles?sid=1&cid=12&lastFileID=0&rowNumber=0': 616,
        # APP端-中央媒体移动端-工人日报-首页-文化
        'http://47.110.139.194/api/getArticles?sid=1&cid=13&lastFileID=0&rowNumber=0': 621,
        # APP端-中央媒体移动端-工人日报-首页-体育
        'http://47.110.139.194/api/getArticles?sid=1&cid=14&lastFileID=0&rowNumber=0': 622,
        # APP端-中央媒体移动端-工人日报-首页-休闲
        'http://47.110.139.194/api/getArticles?sid=1&cid=15&lastFileID=0&rowNumber=0': 623
        # APP端-中央媒体移动端-工人日报-首页-农民工
    }

    custom_settings = {
        'DEPTH_LIMIT': 4,  # 翻页需要设置深度为0 或者 >1
        'DEPTH_PRIORITY': 1,  # 为正值时越靠广度优先，负值则越靠深度优先，默认值为0
        'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')
    }
    
    def parse(self, response):
        rs = json.loads(response.text)
        query_map = get_query_map(response.url)
        cid = query_map['query']['cid']
        rowNumber = int(query_map['query']['rowNumber'])
        
        for i, j in enumerate(rs['list']):
            title = j['title']
            news_url = 'http://47.110.139.194/api/getArticle?sid=1&aid={}&cid={}'.format(j['fileID'], j['columnID'])
            # news_url = 'http://47.110.139.194/api/getArticle?sid=1&aid=80083&cid=4'

            pubtime = j['publishTime']

            yield Request(
                url=news_url,
                callback=self.parse_item2,
                meta={'source_id': response.meta['source_id'], 'title': title,
                      'start_url_time': response.meta.get('start_url_time'),
                      'schedule_time': response.meta.get('schedule_time'),
                      'pubtime': pubtime})
        
        if rowNumber < 80:  # 向后再翻3页
            lastFileID = rs['list'][-1]['fileID']
            rowNumber += 20
            list_url = 'http://47.110.139.194/api/getArticles?sid=1&cid={}&lastFileID={}&rowNumber={}'.format(cid,
                                                                                                              lastFileID,
                                                                                                              rowNumber)
            return Request(  # 这里用return的话就直接结束了
                url=list_url,
                callback=self.parse,
                meta={'source_id': response.meta['source_id'],
                      'start_url_time': response.meta.get('start_url_time'),
                      'schedule_time': response.meta.get('schedule_time'),
                      'isStartUrl': True},
                      dont_filter=True)

    def parse_item2(self, response):
        rs = json.loads(response.text)
        try:
            title = rs['title']
            pubtime = response.meta.get('pubtime') or rs['version']
            origin_name = rs['source']
            content, media, videos, _, = self.content_clean(rs['content'], need_video=True)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            videos=videos,
            media=media,
        )