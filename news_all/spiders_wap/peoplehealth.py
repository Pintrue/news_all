# -*- coding: utf-8 -*-

import json
from scrapy import Request
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings


class PeopleHealthSpider(NewsRSpider):
    """人民健康 app"""
    name = 'people_health_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        'http://appuser.people.cn/i/content/getcontentlist.json?tagid=15&pjcode=10_2016_11_75&devicetype=2': 294,  # 389,  # 独家
        'http://appuser.people.cn/i/content/getcontentlist.json?tagid=14&pjcode=10_2016_11_75&devicetype=2': 298,  # 392,  # 热点
        'http://appuser.people.cn/i/content/getcontentlist.json?tagid=10&pjcode=10_2016_11_75&devicetype=2': 299,  # 393,  # 曝光
        'http://appuser.people.cn/i/content/getcontentlist.json?tagid=36&pjcode=10_2016_11_75&devicetype=2': 302,  # 394,  # 美食
        'http://appuser.people.cn/i/content/getcontentlist.json?tagid=37&pjcode=10_2016_11_75&devicetype=2': 303,  # 395,  # 中医
        'http://appuser.people.cn/i/content/getcontentlist.json?tagid=38&pjcode=10_2016_11_75&devicetype=2': 306,  # 396,  # 养生
        'http://appuser.people.cn/i/content/getcontentlist.json?tagid=39&pjcode=10_2016_11_75&devicetype=2': 307,  # 397,  # 健身
    }
    baseurl = 'http://appuser.people.cn/i/content/getdetail.json?itemid={}&pjcode=10_2016_11_75'

    # LimitatedDaysHoursMinutes = (3, 0, 0)

    def parse(self, response):
        rs = json.loads(response.text)
        result = rs.get('result')

        if result.get('message') != 'ok':
            return self.produce_debugitem(response, 'json error')

        for i in rs.get('data', []):
            items = i.get('items', [])
            for j in items:
                items_sub = j.get('items_sub', [])  # todo 如果需要则采"cover"图
                for x in items_sub:
                    # 获取id 拼接每条新闻的详情url 并解析
                    url = self.baseurl.format(x.get('id'))  # 构建一个每个条目的完整url
                    yield Request(url, callback=self.parse_item,
                                  meta={'source_id': response.meta['source_id'],
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')})

    def parse_item(self, response):
        rs = json.loads(response.text)
        result = rs.get('result')
        if result.get('message') != 'ok':
            return self.produce_debugitem(response, 'json error')

        data = rs.get('data')
        article = data.get('article')
        title = article.get('title')
        origin_name = article.get('source')
        pubtime = article.get('time')
        content = article.get('content')
        # 可能是广告https://hys.people-health.cn/web/downloadPage
        if not content:
            return self.produce_debugitem(response, 'content is null')
        content, media, videos, video_cover = self.content_clean(content)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,
        )
