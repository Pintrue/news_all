# -*- coding: utf-8 -*-

import json
from scrapy import Request
from news_all.spider_models import NewsRSpider


class TtkbWapSpider(NewsRSpider):
    """天天快报客户端"""
    name = 'ttkb_wap'

    mystart_urls = {
        'http://op.inews.qq.com/mcms/h5/info/channel_data?refer=100000208&app_key=cace364d707a49496b18b132099fd072&channel_code=kb_news_sex&start=0&size=10': 200130,
    # 天天快报-情感
        'http://op.inews.qq.com/mcms/h5/info/channel_data?refer=100000208&app_key=cace364d707a49496b18b132099fd072&channel_code=kb_news_tea&start=0&size=10': 200214,
    # 天天快报-茶道
        'http://op.inews.qq.com/mcms/h5/info/channel_data?refer=100000208&app_key=cace364d707a49496b18b132099fd072&channel_code=kb_news_fishing&start=0&size=10': 200211,
    # 天天快报-钓鱼

    }

    def parse(self, response):
        rj = json.loads(response.text)
        data = rj.get('data')
        result = data.get('list')
        # result = r.get('content')

        for i in result:
            content = i.get('content')
            url = content.get("url")
            title = content.get("title")
            origin_name = content.get("src")
            pubtime = content.get("timestamp")

            yield Request(
                url=url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,"origin_name":origin_name,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )

    def parse_item(self, response):
        try:
            content_div = response.xpath('//div[@class="textDec"]')
            content_div[0]
        except:
            return self.produce_debugitem(response, "xpath error")

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

