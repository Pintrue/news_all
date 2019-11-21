# -*- coding: utf-8 -*-

import json
from scrapy import Request
from news_all.spider_models import NewsRSpider


class LnrbxmtSpider(NewsRSpider):
    """辽宁日报"""
    name = 'lnrbxmt_all'

    mystart_urls = {
        'http://api.lnrbxmt.com/index.php/news/get_list?menu_id=1&page=1&num=15&last_id=0&token=75804d4e8eda216c26d509800921b7b9': 1301815,
    # 辽宁日报-头条

    }

    def parse(self, response):
        rj = json.loads(response.text)
        list = rj.get("list")
        for i in list:
            id = i.get("id")
            news_url = 'http://api.lnrbxmt.com/index.php/news/get_content?id=' + id

            title = i.get("title")
            origin_name = i.get("source")
            pubtime = i.get('release_datetime')
            
            yield Request(
                url=news_url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title, 'origin_name': origin_name,'pubtime':pubtime,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )

    def parse_item(self, response):
        rj = json.loads(response.text)
        result = rj.get("info")
        content_div = result.get("content")
        if content_div is None:
            return self.produce_debugitem(response, 'json error')
        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            content=content,
            media=media,
            videos=videos,
        )
