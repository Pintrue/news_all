# -*- coding: utf-8 -*-

import json
from scrapy import Request
from news_all.spider_models import NewsRSpider


class M2peopleAllSpider(NewsRSpider):
    name = 'peoplem2'
    
    mystart_urls = {
        'http://m2.people.cn/apps/zixun/json.php?page={}&size=40'.format(i): 1000154 for i in range(1, 4)  # 手机人民网m2
    }

    def parse(self, response):
        rj = json.loads(response.text)
        data = rj.get('articles', [])
        if not data:
            return self.produce_debugitem(response, 'json error')
        for i in data:
            content = i.get('content')
            title = i.get("title")
            origin_name = i.get("media")
            pubtime = i.get("time")
            newsUrl = i.get("newsUrl")
            try:
                content, media, videos, video_cover = self.content_clean(content, need_video=True)
                yield self.produce_item(
                    response=response,
                    title=title,
                    pubtime=pubtime,
                    origin_name=origin_name,
                    content=content,
                    media=media,
                    videos=videos,
                    srcLink=newsUrl
                )
            except BaseException:
                # news_url = 'http://m2.people.cn/r/MV8wXzEzMzIyNjExXzE2MDFfMTU3MTg5Njk5OA=='
                # 防止重复报警
                yield Request(
                    url=newsUrl,
                    callback=self.parse_item,
                    meta={
                        'source_id': response.meta.get('source_id'),
                        'start_url_time': response.meta.get('start_url_time'),
                        'schedule_time': response.meta.get('schedule_time')
                    }
                )

    def parse_item(self, response):
        return self.produce_debugitem(response, 'json error')
