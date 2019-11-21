#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 9:16
# @Author  : wjq
# @File    : yicai_wap.py


import json
from scrapy import Request
from scrapy.conf import settings
from news_all.spider_models import NewsRSpider


class YicaiWapSpider(NewsRSpider):
    chinese_name = """第一财经app"""
    name = 'yicai_wap'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}

    mystart_urls = {
    'https://appcdn.yicai.com/handler/app/GetNewsListByChannelId.ashx?cid=537&pagesize=25&page=1&check=b2095dccc78037e41d4cc0349e929e05': 1302076,
    # 第一财经-中国时间
    'https://appcdn.yicai.com/handler/app/GetNewsListByChannelId.ashx?cid=65&pagesize=25&page=1&check=c61a4b5268e573a477c87ef1c4dccc7d': 1302074,
    # 第一财经-今日股市
    'https://appcdn.yicai.com/handler/app/GetNewsListByChannelId.ashx?cid=57&pagesize=25&page=1&check=fd1be75966a9da6b90cbbd71a3f66e1f': 1302072,
    # 第一财经-公司
    'https://appcdn.yicai.com/handler/app/GetNewsListByChannelId.ashx?cid=296&pagesize=25&page=1&check=e6c2c4f6c81c20d54e0b9d2cb87bc3ed': 1302075,
    # 第一财经-公司与行业
    'https://appcdn.yicai.com/handler/app/GetNewsListByChannelId.ashx?cid=49&pagesize=25&page=1&check=25552d812146c45d791d8f67bb7dfc4a': 1302070,
    # 第一财经-宏观
    'https://appcdn.yicai.com/handler/app/GetNewsListByChannelId.ashx?cid=524&pagesize=25&page=1&check=f05be51e93af1f13aa152b98dd1ca29d': 1302077,
    # 第一财经-第一时尚
    'https://appcdn.yicai.com/handler/app/GetNewsListByChannelId.ashx?cid=54&pagesize=25&page=1&check=ec15c793c5d29e848355267092c138ef': 1302068,
    # 第一财经-要闻
    'https://appcdn.yicai.com/handler/app/GetNewsListByChannelId.ashx?cid=64&pagesize=25&page=1&check=9f27f0ed66c6377675da23a178bac6d0': 1302073,
    # 第一财经-谈股论金
    'https://appcdn.yicai.com/handler/app/GetNewsListByChannelId.ashx?cid=53&pagesize=25&page=1&check=0571f11d6151de90a2139d34aab9d6de': 1302071,
    # 第一财经-金融
}

    def parse(self, response):
        rs = json.loads(response.text)
        if not isinstance(rs, list):
            return self.produce_debugitem(response, 'json error')
    
        for i in rs:
            news_id = i.get('NewsID')
            news_url = 'https://www.yicai.com/news/{}.html'.format(news_id)
            pubtime = i.get('LastDate')
            title = i.get('NewsTitle')

            origin_name = i.get('NewsSource')
            yield Request(
                url=news_url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                      'origin_name': origin_name,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )

    def parse_item(self, response):
        xp = response.xpath
        try:
            content_div = xp('//div[@class="m-txt"]/p')
            content, media, _, _ = self.content_clean(content_div, kill_xpaths=r'//div[@class="news-edit-info"]')
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            content=content,
            media=media
        )
