#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 15:42
# @Author  : wjq
# @File    : haiwainet_video.py
from datetime import datetime

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
import re

base_api = 'http://m.haiwainet.cn/middle/{channelid}/{date}/content_{contentid}_1.html'


def change_url(x):
    #  网站   http://v.haiwainet.cn/n/2019/0816/c3543236-31612075.html
    #  wap站  http://m.haiwainet.cn/middle/3543236/2019/0816/content_31612075_1.html
    res = re.search(r'haiwainet.cn/n/(\d{4}/\d{4})/c(\d+)-(\d+)\.htm', x.url)
    url_2 = base_api.format(channelid=res.group(2), date=res.group(1), contentid=res.group(3))
    kwargs = {}
    for i in ['method', 'headers', 'body', 'cookies', 'meta', 'flags',
              'encoding', 'priority', 'dont_filter', 'callback', 'errback']:
        kwargs.setdefault(i, getattr(x, i))
    r = Request(url_2, **kwargs)
    return r


class HaiwainetVSpider(NewsRCSpider):
    """海外网 视频"""
    name = 'haiwainet_video'
    mystart_urls = {
            "http://v.haiwainet.cn/HWWhaikeshipin/": 3758,
            "http://v.haiwainet.cn/news/": 3766,
            "http://v.haiwainet.cn/jintai/": 3767,
            "http://v.haiwainet.cn/chinavison/": 3768,
            "http://v.haiwainet.cn/hello/": 3769,
            "http://v.haiwainet.cn/": 3770,
            "http://v.haiwainet.cn/news/2018_qnmlg-2018/": 3771,
            "http://v.haiwainet.cn/jintai/2016cshd/": 3772,
            "http://v.haiwainet.cn/2016wyxf/":  3773,
    }
    # LimitatedDaysHoursMinutes = (10, 0, 0)
    
    rules = (
        Rule(LinkExtractor(allow=r'v.haiwainet.cn/n/%s\d{2}/c\d+-\d+.htm'% datetime.today().strftime('%Y/%m'),  # 视频少不限制月份
                           ),
             callback='parse_item', process_request=change_url,
             follow=False),
        Rule(LinkExtractor(allow=r'haiwainet.cn.*?\d{5,}.htm', deny=(r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/'),
                           ),
             process_request=otherurl_meta,
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            pubtime = xp('//meta[@name="publishdate"]/@content').extract_first('')
            video_url = xp("//div[@class='videoBox']/@data-video-src")[0].extract()
            content_div = xp("//div[@class='con']/p")
            origin_name = xp('//meta[@name="source"]/@content').extract_first('')
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")
        
        return self.produce_item(
            response=response,
            title=self.get_page_title(response),
            pubtime=pubtime,
            origin_name=origin_name,
            content='<div>#{{1}}#</div>' + content,
            media=media,
            videos={'1': {'src': video_url}}
        )
