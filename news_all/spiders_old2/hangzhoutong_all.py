# -*- coding: utf-8 -*-

import json
from scrapy import Request
from news_all.spider_models import NewsRCSpider


class HangZhouTongAllSpider(NewsRCSpider):
    """杭州通"""
    name = 'hangzhoutong_all'

    mystart_urls = {
        'http://app.hangzhou.com.cn/api3.php?&page=1&class_id=99': 1301917,  # 杭州通 热点
        'http://app.hangzhou.com.cn/api3.php?&page=1&class_id=6': 1301920,  # 杭州通-便民
        'http://app.hangzhou.com.cn/api3.php?&page=1&class_id=4': 1301918,  # 杭州通-时政
        'http://app.hangzhou.com.cn/api3.php?&page=1&class_id=5': 1301921,  # 杭州通-本塘
        'http://app.hangzhou.com.cn/api3.php?&page=1&class_id=8': 1301919,  # 杭州通-财经

    }

    def parse(self, response):
        rj = json.loads(response.text)
        data = rj.get("data")
        for i in data:
            url = i.get("shareurl")
            title = i.get("title")
            pubtime = i.get("add_time")
            yield Request(
                url=url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title,'pubtime':pubtime,
                      
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )

    # https://appm.hangzhou.com.cn/article_pc.php?id=273779
    def parse_item(self, response):
        try:
            content_div = response.xpath('//div[@class="articleCont"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            content=content,
            media=media,
            videos=videos,
        )