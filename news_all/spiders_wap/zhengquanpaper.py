# -*- coding: utf-8 -*-

import json
from datetime import datetime
from scrapy import Request
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings

# todo
""" 
快讯 在要闻分页中
POST http://www.stcn.com/common/mobile/api/v2/flash/list_1.json HTTP/1.1
Content-Length: 0
Host: www.stcn.com
Connection: Keep-Alive
User-Agent: Apache-HttpClient/UNAVAILABLE (java 1.4)
"""


class ZhengQuanPaperSpider(NewsRSpider):
    """证券时报 app"""
    name = 'zhengquan_paper_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    # todo  根据新闻时间决定要不要发下一page list_2/3/4 request
    mystart_urls = {
        'http://www.stcn.com/common/mobile/api/v2/news/list_1.json' : 398,   #  要闻
        'http://www.stcn.com/common/mobile/api/v2/market/list_1.json' : 399,   #  股市
        'http://www.stcn.com/common/mobile/api/v2/depth/list_1.json' : 400,   #  深度
        'http://www.stcn.com/common/mobile/api/v2/comment/list_1.json' : 401,   #  评论
        'http://www.stcn.com/common/mobile/api/v2/watch/list_1.json' : 402,   #  观察
        'http://www.stcn.com/common/mobile/api/v2/country/list_1.json' : 403,   #  国内
        'http://www.stcn.com/common/mobile/api/v2/world/list_1.json' : 404,   #  海外
        'http://www.stcn.com/common/mobile/api/v2/venture/list_1.json' : 405,   #  创投
        'http://www.stcn.com/common/mobile/api/v2/people/list_1.json' : 406,   #  人物
    }
    # LimitatedDaysHoursMinutes = 10

    def parse(self, response):
        rs = json.loads(response.text)
        slides = rs.get('slide', [])
        if isinstance(slides, str):
            slides = json.loads(slides)

        news_reqs = []

        for i in rs.get('list') + slides:
            pubtime = i.get("publishStr", "") or i.get("sorttime", "")
            title = i.get('title')
            news_url = i.get('shareurl')

            r = Request(news_url, callback=self.parse_item, meta={'pubtime':pubtime, 'title':title,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')})
            news_reqs.append(r)

        for r in news_reqs:
            r.meta['source_id'] = response.meta['source_id']
            r.meta['start_url_time'] = response.meta.get('start_url_time')
            r.meta['schedule_time'] = response.meta.get('schedule_time')
            yield r

    def parse_item(self, response):
        origin_name = response.xpath("//div[@class='title']/span/em[2]/text()").extract_first('')
        try:
            content_div = response.xpath("//div[@class='con_txt']")[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )