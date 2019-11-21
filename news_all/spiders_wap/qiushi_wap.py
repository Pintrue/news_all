# -*- coding:utf-8 -*-
# @Time    : 2019/7/10 17:29
# @Author  : zxy
# @File    : qiushi_wap.py

import json
from scrapy import Request
from scrapy.conf import settings
from news_all.spider_models import NewsRSpider


class QiushiSpider(NewsRSpider):
    chinese_name = """求是新闻app"""
    name = 'qiushi_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        "http://da.wa.news.cn/nodeart/page?nid=1181546&orderby=1&pgnum=1&cnt=10": 3654,  # 要闻
        "http://da.wa.news.cn/nodeart/page?nid=1184334&orderby=1&pgnum=1&cnt=10": 3084,
        "http://da.wa.news.cn/nodeart/page?nid=1181602&orderby=1&pgnum=1&cnt=10": 3085,
        "http://da.wa.news.cn/nodeart/page?nid=1181603&orderby=1&pgnum=1&cnt=10": 3086,
        "http://da.wa.news.cn/nodeart/page?nid=1184412&orderby=1&pgnum=1&cnt=10": 3087,
        "http://da.wa.news.cn/nodeart/page?nid=1195041&orderby=1&pgnum=1&cnt=10": 3090,
        "http://da.wa.news.cn/nodeart/page?nid=1184340&orderby=1&pgnum=1&cnt=10": 3092,
        "http://da.wa.news.cn/nodeart/page?nid=1181640&orderby=1&pgnum=1&cnt=10": 3093,
        "http://da.wa.news.cn/nodeart/page?nid=1181614&orderby=1&pgnum=1&cnt=10": 3094,
        "http://da.wa.news.cn/nodeart/page?nid=1181632&orderby=1&pgnum=1&cnt=10": 3099,
        "http://da.wa.news.cn/nodeart/page?nid=1181648&orderby=1&pgnum=1&cnt=10": 3100,
        "http://da.wa.news.cn/nodeart/page?nid=1181665&orderby=1&pgnum=1&cnt=10": 3101,
        "http://da.wa.news.cn/nodeart/page?nid=1181708&orderby=1&pgnum=1&cnt=10": 3102,
        "http://da.wa.news.cn/nodeart/page?nid=1181686&orderby=1&pgnum=1&cnt=10": 3103,
    }
    base_api = 'http://da.wa.news.cn/nodeart/detail/{}'

    def parse(self, response):
        rs = json.loads(response.text)
        data = rs.get('data', None)
        if str(rs.get('status')) != '0' or not isinstance(data, dict):
            return self.produce_debugitem(response, 'json error')
        for art_data in data.get('list', []):
            doc_id = art_data.get('DocID')
            if not doc_id:
                print('have not doc_id')
                continue
            news_url = self.base_api.format(doc_id)

            title = art_data.get('Title')
            pubtime = art_data.get('PubTime')

            origin_name = art_data.get("SourceName")
            meta = {'source_id': response.meta['source_id'],
                    'title': title,
                    'pubtime': pubtime,
                    'origin_name': origin_name,
                    'start_url_time': response.meta.get('start_url_time'),
                    'schedule_time': response.meta.get('schedule_time')}

            yield Request(
                url=news_url,
                headers=self.start_headers,
                callback=self.parse_item,
                meta=meta)

    def parse_item(self, response):
        articel_data = json.loads(response.text)
        pubtime = response.request.meta['pubtime']
        if not pubtime:
            pubtime = articel_data.get('CreateTime')

        content_raw = articel_data.get('Content')
        if not content_raw:
            return
        content, media, _, _ = self.content_clean(content_raw)

        return self.produce_item(
            response=response,
            title=response.meta['title'],
            pubtime=pubtime,
            # origin_name=response.meta["origin_name"],   # 杂质'《求是》2019/18'  '《红旗文稿》2019/18'
            summary=articel_data.get('summary'),
            content=content,
            media=media)
