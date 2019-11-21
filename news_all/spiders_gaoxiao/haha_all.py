#!/usr/bin/env python 
# -*- coding:utf-8 _*-  
# Time: 2019/08/20
# Author: zcy
import re
from news_all.spider_models import *
from news_all.tools.time_translater import timestamps
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


img_pattern = re.compile(r'<img.*?(?:data-original|src)=[\',"]((?:http|https)?//(?!static\.hahamx\.cn/images/pic_none).*?)[\',"].*?>')


class HahaSpider(NewsRCSpider):
    """傲游哈哈搞笑"""
    name = 'haha_all'

    mystart_urls_base = {
        'https://www.hahamx.cn/good/day/%s':  3790,  # 推荐
        'https://www.hahamx.cn/new/%s':       3792,  # 新鲜
        'https://www.hahamx.cn/cross/%s':     3793,  # 穿越
        'https://www.hahamx.cn/pic/new/%s':   3794,  # 搞笑图-新鲜
        'https://www.hahamx.cn/pic/good/%s':  3796,  # 搞笑图-今日榜单
        'https://www.hahamx.cn/pic/rising/%s':3797,  # 搞笑图-上升快
        'https://www.hahamx.cn/pic/hot/%s':   3798,  # 搞笑图-评论多
        'https://www.hahamx.cn/comment/%s':   3799,  # 神评论
    }

    mystart_urls = {}
    for i in range(1, 11):
        for url, source_id in mystart_urls_base.items():
            mystart_urls[url % i] = source_id
    
    rules = (
        Rule(LinkExtractor(allow=(r'hahamx.cn/joke/\d+'),),
        callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = self.get_page_title(response).replace('_傲游哈哈', '')
            # pubtime = xp('//span[@class="joke-user-info-create-time"]/text()').extract_first()
            content_div = xp('//div[@class="joke-main-content clearfix"]')[0]
            content, media, _, _ = self.content_clean(content_div, img_re=img_pattern)
        except:
            self.produce_debugitem(response, 'xpath error')
        return self.produce_item(
            response=response,
            title=title,
            pubtime=timestamps(),
            content=content,
            media=media
        )
