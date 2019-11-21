#!/usr/bin/env python
# -*- coding:utf-8 _*-
# Time: 2019/07/22
# Author: zcy

from news_all.spider_models import *
from scrapy.conf import settings
import json


class ChinaNewsSipder(NewsRSpider):
    """中新网 app"""
    name = 'china_news_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}

    mystart_urls_base = {
        'https://m.chinanews.com/chinanews/getDigest?language=chs&dtp=10&isWap=yes&pageIndex=%d':2959, # 要闻
        'https://m.chinanews.com/chinanews/getVidList?language=chs&isWap=yes&pageSize=15&pageIndex=%d':2960, # 视频
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=hm&pageIndex=%d':2961, # 华媒
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=gj&pageIndex=%d':2962, # 国际
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=ty&pageIndex=%d':2963, # 体育
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=newsest&pageIndex=%d':2964, # 最新
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=ga&pageIndex=%d':2965, # 港澳
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=tw&pageIndex=%d':2966, # 两岸
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=cj&pageIndex=%d':2967, # 财经
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=yl&pageIndex=%d':2968, # 娱乐
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=sh&pageIndex=%d':2969, # 社会
        'https://m.chinanews.com/chinanews/getPicList?language=chs&isWap=yes&pageSize=15&pageIndex=%d':2970, # 图片
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=hr&pageIndex=%d':2971, # 华人
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=mil&pageIndex=%d':2972, # 军事
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=shj&pageIndex=%d':2973, # 生活
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=business&pageIndex=%d':2974, # 产经
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=estate&pageIndex=%d':2975, # 房产
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=auto&pageIndex=%d':2976, # 汽车
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=it&pageIndex=%d':2977, # IT
        'http://dw.chinanews.com/chinanews/getNewsList?pageSize=15&dtp=11&searchType=1&version_chinanews=6.6.1&deviceId_chinanews=866822032025934&platform_chinanews=android&source=chinanews&cname=tj&pageIndex=%d':2978, # 推荐
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=wine&pageIndex=%d':2979, # 葡萄酒
        'http://dw.chinanews.com/chinanews/getVidList?pageSize=20&dtp=1&pageIndex=%d&channel=dsp&language=chs&version_chinanews=6.6.0&deviceId_chinanews=865685026456493&platform_chinanews=android&source=chinanews':2980, # 短视频
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=stock&pageIndex=%d':2981, # 证券
        'https://m.chinanews.com/chinanews/getNewsList?language=chs&pageSize=15&searchType=1&dtp=6&isWap=yes&cname=fortune&pageIndex=%d':2982, # 金融
        'http://dw.chinanews.com/chinanews/getVidList?pageSize=20&dtp=1&pageIndex=%d&channel=wsj&language=chs&version_chinanews=6.6.0&deviceId_chinanews=865685026456493&platform_chinanews=android&source=chinanews':2983, # 微视界
        'http://dw.chinanews.com/chinanews/getVidList?pageSize=20&dtp=1&pageIndex=%d&channel=xsy&language=chs&version_chinanews=6.6.0&deviceId_chinanews=865685026456493&platform_chinanews=android&source=chinanews':2984, # 新视野
        'http://dw.chinanews.com/chinanews/getVidList?pageSize=20&dtp=1&pageIndex=%d&channel=zgf&language=chs&version_chinanews=6.6.0&deviceId_chinanews=865685026456493&platform_chinanews=android&source=chinanews':2985, # 中国风
    }

    mystart_urls = {}
    for page in range(1, 11):
        for i, j in mystart_urls_base.items():
            mystart_urls[i % page] = j
    # 'http://dw.chinanews.com/chinanews/content.jsp?id=8920365&classify=zw&pageSize=6&language=chs'
    base_api = 'http://dw.chinanews.com/chinanews/content.jsp?id={}'
    
    def parse(self, response):
        rs = json.loads(response.body)
        if rs['message'] == '[数据库异常]:no data.':
            return self.produce_debugitem(response, reason='[数据库异常]:no data.')
        data_list = rs['data']
        
        items = []
        for data in data_list:
            if data['classify'] == 'rddlf':
                dlfList = data['dlfList']
                for dlf in dlfList:
                    items.append(self.deal_one_article(dlf, response))

            else:
                items.append(self.deal_one_article(data, response))
        for i in items:
            if i:
                yield i
                
    def deal_one_article(self, dlf, response):
        newsid = dlf['id']
        pubtime = dlf['pubtime']
        content, media, _, _ = self.content_clean(dlf['contentForDetail'])
        video = {'1': {'src': dlf.get('video')}} if dlf.get('video') else ''
        return self.produce_item(
            response=response,
            title=dlf['title'],
            pubtime=pubtime,
            origin_name=dlf['source'],
            content='<div>#{{1}}#</div>' + content if video != '' else content,
            media=media,
            videos=video
        )
