# -*- coding: utf-8 -*-

import re
import json
from scrapy import Request
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider


class DbwAllSpider(NewsRCSpider):
    """学习强国"""
    name = 'xuexi_all'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}

    mystart_urls = {
        'https://www.xuexi.cn/lgdata/index.json?_st=26005365': 7650
    }

    start_headers = {
        'Host': 'www.xuexi.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    }

    def parse(self, response):
        # https://www.xuexi.cn/lgpage/detail/index.html?id=11891749402835707327
        title_urls = re.findall(r'\"link\":\"https://www.xuexi.cn/lgpage/detail/index.html\?id=\d+\"', response.text)
        # "https://boot-source.xuexi.cn/data/app/3493463650618488237.js?callback=callback&_st=1560395879456"   详情页真实地址
        for i in title_urls:
            # url1= re.findall('https://www.xuexi.cn/lgpage/detail/index.html\?id=\d+', i)
            id = re.findall('\d+', i)
            url = "https://boot-source.xuexi.cn/data/app/"+id[0]+".js?callback=callback"
            yield Request(
                url=url,
                callback=self.parse_item,
                meta={
                      'source_id': response.meta['source_id'],
                      'start_url_time': response.meta['start_url_time'],
                      'schedule_time': response.meta['schedule_time'],
                }
            )

    def parse_item(self, response):
        # https://www.xuexi.cn/lgpage/detail/index.html?id=11891749402835707327
        text = response.text
        result = text.replace("callback(","").replace(")","")
        rs = json.loads(result)
        try:
            title = rs.get('title')
            img_urls = rs.get('image')
            # img_list = img_urls.get('url')
            content = rs.get('content')
            source = rs.get('source', '').replace('yres-article-manual_', '')
            pubtime = rs.get('publish_time')
            media = {}
            if img_urls is None:
                print("无图新闻")
            else:
                if len(img_urls):
                    count = len(img_urls)
                    x = list(range(0, count))
                    for (i, j) in zip(img_urls, x):
                        content = content.replace("<!--{img:" + str(j) + "}-->", "<img src='" + i.get("url") + "' /><br>")
            content, media, videos, video_cover = self.content_clean(content, need_video=True)
        except:
            return self.produce_debugitem(response, "json error")

        return self.produce_item(response=response,
                                 title=title,
                                 pubtime=pubtime,
                                 origin_name=source,
                                 content=content,
                                 media=media,
                                 videos=videos
        )