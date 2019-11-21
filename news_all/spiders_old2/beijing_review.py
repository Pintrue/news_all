#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 10:50
# @Author  : wjq
# @File    : beijing_review.py

from scrapy.conf import settings
from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class BeijingreviewSpider(NewsRCSpider):
    """北京周报"""
    name = 'beijingreview'
    # mystart_urls = {
    #     'http://www.beijingreview.com.cn/shishi/': 1301341,  # 北京周报 时事
    #     'http://www.beijingreview.com.cn/caijing/': 1301130,  # 北京周报-财经-左侧列表
    # }

    mystart_urls = {
        'http://www.beijingreview.com.cn/keji/': 1,
        'http://www.beijingreview.com.cn/tupianji/': 2,
        'http://www.beijingreview.com.cn/wenhua/': 3,
        'http://www.beijingreview.com.cn/minsheng/': 4,
        'http://www.beijingreview.com.cn/chinafrica/': 5,
        'http://www.beijingreview.com.cn/wenjian/': 6,
    }

    rules = (
        # http://www.beijingreview.com.cn/shishi/201906/t20190624_800171470.html
        # http://www.beijingreview.com.cn/caijing/201906/t20190624_800171485.html 组图
        Rule(LinkExtractor(allow=(r'beijingreview.com.cn.*?/%s/t\d+_\d+.html' % datetime.today().strftime('%Y%m'),),
                           # deny=(r'',)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'beijingreview.com.cn.*?\d+.s?htm',),
                           deny=(r'/201[0-8]',
                                 r'/2019(?:0[1-9]|10)',
                                 r'/index_\d+')
                           ),
             process_request=otherurl_meta, follow=False),
    )

    custom_settings = {
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            pubtime = xp('/html/head/meta[@name="publishdate"]/@content').extract_first()
            content_div = xp('//div[@class="TRS_Editor"]')[0]
            origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first("")
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")
        title = self.get_page_title(response)
        next_a = xp('//a[@id="pagenav_1"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         })
        
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media
        )

    def parse_page(self, response):
        xp = response.xpath
        meta_new = deepcopy(response.meta)
    
        try:
            content_div = xp('//div[@class="TRS_Editor"]')[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()
    
        next_a = xp('//div[@id="div_currpage"]//a[contains(text(), "下一页")]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
    
        content, media, videos, video_cover = self.content_clean(meta_new['content'],
                                                                 kill_xpaths='//div[@id="div_currpage"]')
    
        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),

            content=content,
            media=media
        )