# -*- coding: utf-8 -*-

import json
from scrapy import Request
from news_all.spider_models import NewsRCSpider


class JiaodongSpider(NewsRCSpider):
    # 胶东头条
    name = 'jiaodong_all'

    mystart_urls = {

        'http://api.jiaodong.net/jiaodongtop/V10/News/getNews?channelid=2021000000000000&related=false&news_type=0&page_count=20': 1302046,
    # 胶东头条
        'http://api.jiaodong.net/jiaodongtop/V10/News/getNews?channelid=2004000000000000&related=false&news_type=0&page_count=20': 1302047,
    # 胶东头条
        'http://api.jiaodong.net/jiaodongtop/V10/News/getNews?channelid=2011000000000000&related=false&news_type=0&page_count=20': 1302042,
    # 胶东头条
        'http://api.jiaodong.net/jiaodongtop/V10/News/getNews?channelid=2006000000000000&related=false&news_type=0&page_count=20': 1302043,
    # 胶东头条
        'http://api.jiaodong.net/jiaodongtop/V10/News/getNews?channelid=2019000000000000&related=false&news_type=0&page_count=20': 1302044,
    # 胶东头条
        'http://api.jiaodong.net/jiaodongtop/V10/News/getNews?channelid=2005000000000000&related=false&news_type=0&page_count=20': 1302048,
    # 胶东头条
        'http://api.jiaodong.net/jiaodongtop/V10/News/getNews?channelid=2007000000000000&related=false&news_type=0&page_count=20': 1302040,
    # 胶东头条
        'http://api.jiaodong.net/jiaodongtop/V10/News/getNews?channelid=2003000000000000&related=false&news_type=0&page_count=20': 1302041,
    # 胶东头条
        'http://api.jiaodong.net/jiaodongtop/V10/News/getNews?channelid=2009000000000000&related=false&news_type=0&page_count=20': 1302045,
    # 胶东头条

    }

    def parse(self, response):
        rj = json.loads(response.text)
        data= rj.get("data")
        for i in data:
            news_url = i.get("linkUrl")

            title = i.get("title")
            pubtime = i.get("pubDate")
            origin_name = i.get("origin_name")

            yield Request(
                url=news_url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title,'pubtime':pubtime,'origin_name':origin_name,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )

    def parse_item(self, response):
        try:
            content_div = response.xpath('//div[@class="content"]')[0]
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            content=content,
            media=media,
            videos=videos,
        )

