#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 18:54
# @Author  : wjq
# @File    : jiemian_all.py

from copy import deepcopy
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class JiemianAllSpider(NewsRCSpider):
    chinese_name = """界面网站"""
    name = 'jiemian_all'
    mystart_urls = {
        'https://www.jiemian.com/lists/84.html': 2597,
        'https://www.jiemian.com/lists/6.html': 2598,
        'https://www.jiemian.com/lists/66.html': 2599,
    }
    
    # https://www.jiemian.com/article/3159662.html
    rules = (
        Rule(LinkExtractor(allow=(r'jiemian.com/article/\d+.htm'),
                           # restrict_xpaths=r'//*[@id="news_ul"]'),
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'jiemian.com.*?\d+.htm'), deny=(r'/201[0-8]', r'/20190[1-9]/', r'/lists/\d+.html'),
                           # restrict_xpaths=r'//*[@id="news_ul"]'),
                           ),
             process_request=otherurl_meta, follow=False),
    )
    
    dd = deepcopy(settings.getdict('APP_DOWN'))
    dd['news_all.middlewares.ProxyRdMiddleware'] = 100   # 备用 使用隧道代理
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': dd, }
    
    # https://www.jiemian.com/article/3159662.html
    def parse_item(self, response):
        xp = response.xpath
        try:  # 2019/05/27 14:20
            ps = xp('//div[@class="article-info"]').re(r'\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}')  # 2019/05/26 10:50收藏(0) 3.5W
            pubtime = ps[0]
            og = xp('//div[@class="article-info"]').re(r'来源：\w{2+}')
            if og:  # ['   ']
                og = og[0].split()
            origin_name = og[0].split()[0] if og else '界面新闻'
            content_div = xp('//div[@class="article-content"]')[0]
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('|')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
