#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/27 17:35
# @Author  : wjq
# @File    : rmltapp_video.py

import json
import requests
from jsonpath import jsonpath
from scrapy import Request
from scrapy.conf import settings
from news_all.spider_models import NewsRSpider
from news_all.tools.html_clean import get_query_map

# 详情页的headers不加也行
detail_headers = """Host: dangjian.edangjian.com
Connection: keep-alive
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Linux; Android 9.0; PCGM00 Build/PKQ1.190101.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Crosswalk/19.49.514.5 Mobile Safari/537.36 DajiaWebView/6.5.2(Build 1252) dajia/{"app":"dajia","buildVersion":"1252","cID":"491668263070467690416591","customID":"4916682630704676904","pID":"guest","system":"android","version":"6.5.2"}
Accept-Encoding: gzip, deflate
Accept-Language: zh-cn
Cookie: 9a572d97987a8f51d9ed091d82148e12_9=3; 9a572d97981ab3834c725c7f25867c25_9=15; 9a572d9798d91c0d5442a801e1cfcd55_9=408; 9a572d9798586206d4d579e0ed91276a_9=32; dajiaID=6737284475251933764_1566841731665; PID=efbfdf1d68824206ba419015bcfe83d4; JSESSIONID=E14FA5CB065C0FA8AEDFB90BEB8496DD; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=zh_CN"""


class RmltVideoSpider(NewsRSpider):
    """人民论坛 app 视频"""
    name = 'rmlt_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        'https://dangjian.edangjian.com/mobileshop/findProductByPage.json': 3883,  # 视频学习
    }
    start_method = 'POST'
    start_body_map = {0: ("视频学习", ['currentPageNumber=%s&commodityTemplateType=2' % i for i in range(1, 3)]), }
    
    sleep_time = 2*60*60
    start_headers = {
        "Host": "dangjian.edangjian.com",
        "Content-Type": "application/x-www-form-urlencoded",  # 必要
        # "Referer": "https://dangjian.edangjian.com/mobileshop/configPageShopProductList.action?shopConfigID=11CN0O3DQL010028&fromCommunityMobilePortalMark=mark",
    }
    
    # http://mpv.videocc.net/9a572d9798/5/9a572d9798d91c0d5442a801e1cfcd55_2.mp4
    video_api = 'http://mpv.videocc.net/9a572d9798/{}/9a572d9798{}_2.mp4'
    
    # 'https://dangjian.edangjian.com//mobileproduct/findProductIndex.action?productId=8305804836171956554'
    news_api = 'https://dangjian.edangjian.com//mobileproduct/findProductIndex.action?productId={}'
    
    def parse(self, response):
        rj = json.loads(response.text)
        
        for j in rj.get("productList", []):
            title = j.get("title")
            
            news_url = self.news_api.format(j.get('productId'))
            pubtime = j.get("updateTime")
            
            yield Request(
                url=news_url,
                callback=self.parse_item,
                meta={'pubtime': pubtime, 'title': title,
                      'source_id': response.meta['source_id'],
                      'start_url_time': response.meta.get('start_url_time'),
                      'schedule_time': response.meta.get('schedule_time')})
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            jstext = xp('//script[@id="productInfoJson"]/text()').extract()[0]
            rj = json.loads(jstext)
            videoUrl = jsonpath(rj, '$..videoUrl')[0]
            
            # 可行http://my.polyv.net/front/video/preview?vid=9a572d9798d91c0d5442a801e1cfcd55_9
            # 不行https://p.bokecc.com/player?vid=15776EC171FE93AE9C33DC5901307461&siteid=7667003FAE3EFB28&autoStart=false&width=600&height=490&playerid=26F3C8DA4DE6A369&playertype=1
            
            qq = get_query_map(videoUrl)
            if qq['netloc'] != 'my.polyv.net':
                return
            vid = qq['query']['vid'].split('_')[0].lstrip('9a572d9798')
            video_url = self.video_api.format(vid[-1], vid)
            if requests.get(video_url).status_code != 200:
                # http://mpv.videocc.net/9a572d9798/d/9a572d9798cd86332e58d422acfdd_2.mp4
                return
            # print(videoUrl, response.meta.get('title'))
        except:
            return self.produce_debugitem(response, 'xpath error')
        
        return self.produce_item(
            response=response,
            title=response.meta.get('title'),
            pubtime=response.meta.get('pubtime'),
            content='<div>#{{1}}#</div>',
            media={},
            videos={'1': {'src': video_url}},
            srcLink=video_url
        )
