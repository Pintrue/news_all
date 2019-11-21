#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/3 17:23
# @Author  : wjq
# @File    : cctv5_wap.py

import json
from scrapy import Request
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings
import jsonpath


class CCTV5WapSpider(NewsRSpider):
    chinese_name = """央视体育app"""
    name = 'cctv5_app'
    mystart_urls = {
        'https://api.5club.cctv.cn/mobileinf/rest/oly/cardgroups': [2986, 2987, 2988, 2989, 2990, 2991, 2992, 2993,
                                                                    2994, 2995, 2996, 2997, 2998, 2999, 3000, 3001,
                                                                    3002, 3003, 3004, 3005, 3006, 3007, 3009, 3010,
                                                                    3011, 3012, 3013, 3014, 3015, 3016]}
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    start_method = 'POST'
    
    start_body_map = {2986: ('推荐',
                             'json={"cardgroups":"SPORTSINDEX","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      2987: ('女足世界杯',
                             'json={"cardgroups":"Page1558426653616740","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      2988: ('足球',
                             'json={"cardgroups":"Page1499225103795157","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      2989: ('篮球',
                             'json={"cardgroups":"Page1499224144980143","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      2990: ('综合体育',
                             'json={"cardgroups":"Page1499224770434152","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      2991: ('排球',
                             'json={"cardgroups":"Page1499224684160147","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      2992: ('温网',
                             'json={"cardgroups":"Page1499224886118154","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      2993: ('冰雪',
                             'json={"cardgroups":"Page1499224560054147","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      2994: ('4k专区',
                             'json={"cardgroups":"Page1550569195596877","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      2995: ('发现-天下足球',
                             'json={"cardgroups":"Page1499223636641134","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      2996: ('发现-足球之夜',
                             'json={"cardgroups":"Page1499223700358135","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      2997: ('发现-冠军欧洲',
                             'json={"cardgroups":"Page1499223432887135","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      2998: ('发现-篮球公园',
                             'json={"cardgroups":"Page1499223505032136","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      2999: ('发现-NBA最前线',
                             'json={"cardgroups":"Page1499223332537130","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3000: ('发现-体育咖吧',
                             'json={"cardgroups":"Page1499223584198137","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3001: ('发现-砥砺',
                             'json={"cardgroups":"Page1561003490895111","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3002: ('发现-风云会',
                             'json={"cardgroups":"Page1499223403839134","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3003: ('发现-田径杂志',
                             'json={"cardgroups":"Page1557487664295964","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3004: ('发现-健身动起来',
                             'json={"cardgroups":"Page1499224634425148","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3005: ('发现-NHL一周进球集锦',
                             'json={"cardgroups":"Page1544319124988660","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3006: ('发现-冰球冰球',
                             'json={"cardgroups":"Page1499224430726143","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3007: ('发现-ATP周刊',
                             'json={"cardgroups":"Page1544319084188535","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3009: ('发现-马术世界',
                             'json={"cardgroups":"Page1544318757329646","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3010: ('发现-约战果岭',
                             'json={"cardgroups":"Page1544318984264651","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3011: ('发现-奔跑中国',
                             'json={"cardgroups":"Page1499223381229133","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3012: ('发现-冰雪天地',
                             'json={"cardgroups":"Page1547396435021766","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3013: ('发现-体育人间',
                             'json={"cardgroups":"Page1527770899890607","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3014: ('发现-奇谭十一人',
                             'json={"cardgroups":"Page1528817015422213","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3015: ('发现-一起说奥运',
                             'json={"cardgroups":"Page1500615897063841","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}'),
                      3016: ('发现-体坛风云人物',
                             'json={"cardgroups":"Page1513646107359502","paging":{"page_size":10,"last_id":"","page_no":1},"version":"2.8.9"}&appcommon={"adid":"865685026456493","ap":"androidphone","an":"央视体育","av":"2.8.9"}')}
    
    video_base = 'https://vod.cctv.cn/cctv/cctvsportsshare/video/video.html?id={id}&link=app://{id}'
    article_base = 'https://vod.cctv.cn/cctv/cctvsportsshare/article/article.html?id={id}&link=app://{id}'
    
    def parse(self, response):
        rs = json.loads(response.text)
        # paged = rs.get("paged")  #  <class 'dict'>: {'more': 1, 'count': 10}
        cards = jsonpath.jsonpath(rs, '$..cards.*')
        if not isinstance(cards, list):
            return self.produce_debugitem(response, 'json error')
        
        for i in cards:
            # 网页 https://vod.cctv.cn/cctv/cctvsportsshare/video/video.html?id=VIDE1562102005515469&link=app://VIDE1562102005515469
            # 网页 https://vod.cctv.cn/cctv/cctvsportsshare/article/article.html?id=ARTI1562194500272856&link=app://ARTI1562194500272856
            # 接口 https://api.5club.cctv.cn/mobileinf/rest/cardgroups/share?json=%7B%27cardgroups%27:%27ARTI1562194500272856%27%7D&cb=jQuery172031397928368506545_1563769491274&_=1563769491302
            link = i.get('link')
            if not link or link[:9] == "videolive":  # "videolive://OlyL20190709204500000CH00000889"
                continue
            origin_name = i.get('source')
            title = i.get('title')
            pubtime = i.get('date')
            if link[6:10] == 'VIDE':
                yield self.produce_item(
                    response=response,
                    title=title,
                    pubtime=pubtime,
                    origin_name=origin_name,
                    content='<div>#{{1}}#</div>',
                    media={},
                    videos={'1': {'src': i['video']['url_cd']}},  # i['video']['url_hd'] or i['video']['url']
                    srcLink=i['video']['url_cd']
                )
            elif link[6:10] == 'ARTI':
                # news_url = 'https://vod.cctv.cn/cctv/cctvsportsshare/article/article.html?id={}&link={}'.format(link.replace('app://', ''), link)
                news_url = "https://api.5club.cctv.cn/mobileinf/rest/cardgroups/share?json={{'cardgroups':'{}'}}".format(
                    link.replace('app://', ''), link)
                yield Request(
                    url=news_url,
                    callback=self.parse_item,
                    headers={"clientversion": "Android/v8.4.2"},
                    meta={'title': title, 'pubtime': pubtime, 'origin_name': origin_name,
                          'source_id': response.meta['source_id'],
                          'start_url_time': response.meta.get('start_url_time'),
                          'schedule_time': response.meta.get('schedule_time')}
                )
            else:
                self.log(link)
    
    def parse_item(self, response):
        rs = json.loads(response.text)
        try:
            cardgroups = rs.get('cardgroups')
            content_div = cardgroups[0]['cards'][0]['content']
            # 放弃cardgroups[1]有其他新闻详情url
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, 'json error')
        
        return self.produce_item(
            response=response,
            title=response.meta.get('title'),
            pubtime=response.meta.get('pubtime'),
            origin_name=response.request.meta['origin_name'],
            content=content,
            media=media,
        )
