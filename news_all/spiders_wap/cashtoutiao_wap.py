#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 9:45
# @Author  : wjq
# @File    : cashtoutiao_wap.py


import json
import random
from copy import deepcopy
from scrapy import Request
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings

UA = [
    "Mozilla/5.0 (Linux; Android 6.0; Redmi Pro Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 hsp",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)'
]


class CashtoutiaoSpider(NewsRSpider):
    """惠头条app"""
    name = 'cashtoutiao_app'
    mystart_urls = {
        'http://api.admin.cp.cashtoutiao.com/headLine/getVideoAndArticleNoCoverApi': [130, 131, 132, 133, 134, 135, 136,
                                                                                      137, 138, 139, 140, 141, 142, 143,
                                                                                      144, 145, 146, ]}
    
    sleep_time = 30
    dd = deepcopy(settings.getdict('APP_DOWN'))
    dd['news_all.middlewares.ProxyRdMiddleware'] = 100  # 备用 使用隧道代理
    custom_settings = {'DOWNLOADER_MIDDLEWARES': dd, }
    
    start_body_map = {
        130: ("娱乐",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'yule', 'page': '0'}),
        131: ("健康",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'jiankang', 'page': '0'}),
        132: ("奇趣",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'xiaohua', 'page': '0'}),
        133: ("美食",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'yinshi', 'page': '0'}),
        134: ("家居",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'jiaju', 'page': '0'}),
        135: ("财经",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'caijing', 'page': '0'}),
        136: ("科技",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'keji', 'page': '0'}),
        137: ("汽车",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'qiche', 'page': '0'}),
        138: ("三农",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'sannong', 'page': '0'}),
        139: ("故事",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'gushi', 'page': '0'}),
        140: ("星座",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'xingzuo', 'page': '0'}),
        141: ("教育",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'jiaoyu', 'page': '0'}),
        142: ("旅行",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'lvxing', 'page': '0'}),
        143: ("时尚",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'shishang', 'page': '0'}),
        144: ("体育",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'tiyu', 'page': '0'}),
        145: ("文化",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'wenhua', 'page': '0'}),
        146: ("游戏",
              {'platform': 'Android', 'versionName': '4.1.0.0', 'deviceId': '', 'appVersion': 64, 'backVersion': '1',
               'type': 'youxi', 'page': '0'})
    }
    
    start_method = 'POST'
    start_headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Host": "api.admin.cp.cashtoutiao.com",  # 可以不加Host Connection Accept-Encoding  User-Agent
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/2.7.1"
    }
    
    def parse(self, response):
        
        rs = json.loads(response.text)
        data = rs.get('data')
        if not isinstance(data, list):
            return self.produce_debugitem(response, 'json error')
        
        for i in data:
            if i.get("coverType") == "video":
                # https://api.admin.cp.cashtoutiao.com/headLine/h5Api/video?id=2531644&channelType=lvxing&contentType=1&userId=00000000&showPosition=1&showSource=feed&contentType=video&loadType=0&log_id=ef558fd4a0354e12b1c1187ac29c2332&exp_id=myselfRecommend&strategy_id=strategy&retrieve_id=retrieve
                continue
            iid = i.get('id')
            news_url = 'https://api.admin.cp.cashtoutiao.com/headLine/h5Api?id={}'.format(iid)
            pubtime = i.get('articlePublishTime')
            title = i.get('topic')
            
            yield Request(
                url=news_url,
                # 不是必要的
                headers={"User-Agent": UA[random.randint(0, len(UA) - 1)], "Origin": "https://h5.cp.cashtoutiao.com"},
                callback=self.parse_item,
                meta={'pubtime': pubtime, 'title': title,
                      'source_id': response.meta['source_id'],
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')})
    
    # https://api.admin.cp.cashtoutiao.com/headLine/h5Api?id=14794696&userId=137796479&showPosition=1&showSource=feed&relatedArticleID=&versionName=&platform=&serkey=&channelType=youxi
    # https://api.admin.cp.cashtoutiao.com/headLine/h5Api?id=14794696
    def parse_item(self, response):
        rs = json.loads(response.text)
        data = rs.get('data')
        if not isinstance(data, dict) or not data.get('content'):
            return self.produce_debugitem(response, 'json error')
        pubtime = response.request.meta['pubtime']
        title = response.request.meta['title']
        
        try:
            content_div = data['content']
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")
        
        content, media, videos, video_cover = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="",  # "source":"我爱花卉盆栽", 作为来源不合适
            content=content,
            media=media,
            videos=videos,
        )
    
    def parse_item_2(self, response):
        # 备用解析模板  必须用浏览器渲染
        # https://h5.cp.cashtoutiao.com/m/news/detail?id=14774909&channelType=lvxing&contentType=0&userId=00000000&showPosition=6&showSource=feed&isShow=0&loadType=0&log_id=6dcce65c268d4d9a874b114189f41398&exp_id=myselfRecommend&strategy_id=strategy&retrieve_id=retrieve
        
        pubtime = response.request.meta['pubtime']
        title = response.request.meta['title']
        
        try:
            content_div = response.xpath('//section[@class="view-content"]')[0]
        except IndexError:
            return self.produce_debugitem(response, "xpath error")
        
        content, media, videos, video_cover = self.content_clean(content_div,
                                                                 kill_xpaths='//div[@class="btn-show-more-area"]')
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="",
            content=content,
            media=media,
            videos=videos,
        )
