#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 16:36
# @Author  : wjq
# @File    : guancha_all.py


from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class YueduwenAllSpider(NewsRCSpider):
    chinese_name = """悦读文"""
    name = 'yueduwen_all'
    mystart_urls = {
        'https://www.yueduwen.com/a/tupian/':2144,
        'https://www.yueduwen.com/a/lizhiwenzhang/':2146,
        'https://www.yueduwen.com/a/qgwz/':2313,
        # 'https://www.yueduwen.com/a/jingdianwenzhang/':2314,
        # 'https://www.yueduwen.com/a/yuju/':2315,
        # 'https://www.yueduwen.com/a/shige/':2317,
        # 'https://www.yueduwen.com/a/sanwen/':2369,
        'https://www.yueduwen.com/a/jingdianwenzhang/':2371,
        'https://www.yueduwen.com/a/sanwen/':2372,
        'https://www.yueduwen.com/a/shige/':2384,
        'https://www.yueduwen.com/a/gushi/':2386,
        'https://www.yueduwen.com/a/riji/':2388,
        'https://www.yueduwen.com/a/yuju/':2389,
        'https://www.yueduwen.com/a/zhufuyu/':2390,
        'https://www.yueduwen.com/xiaohua/':2391,
        'https://www.yueduwen.com/xiaohua/list_5_1.html':2392,
        'https://www.yueduwen.com/xiaohua/lingxiaohua/':2393,
        'https://www.yueduwen.com/xiaohua/youmo/':2394,
        'https://www.yueduwen.com/xiaohua/qutu/':2395,
        # 'https://www.yueduwen.com/a/tupian/':2397,
        'https://www.yueduwen.com/new.html':2399,
        'https://www.yueduwen.com/a/renshengganwu/':2404,
        'https://www.yueduwen.com/a/aiqing/':2406,
        'https://www.yueduwen.com/a/qinqing/':2409,
        'https://www.yueduwen.com/a/youqing/':2411,
        'https://www.yueduwen.com/a/shangganwenzhang/':2412,
        'https://www.yueduwen.com/a/aiqingmeiwen/':2413,
    }

    #https://www.yueduwen.com/a/yijing/2017091211428.html
    #https://www.yueduwen.com/a/lizhiwenzhang/2019022117047.html
    #https://www.yueduwen.com/a/tonghuagushi/201604082201.html

    #https://www.yueduwen.com/xiaohua/zonghe/2019062317469.html
    #https://www.yueduwen.com/xiaohua/jingdian/201603021365.html

    rules = (
        Rule(LinkExtractor(allow=(r'yueduwen.com/.*?/\d+.html'),),
             callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='title']/h2/text()").extract_first() or self.get_page_title(response).split('_')[0]
            # pubtime = xp('//div[@class="info"]').re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            #
            #     self.log('out of LimitatedDaysHoursMinutes: %s' % response.url, logging.DEBUG)
            #
            #
            # origin_name = xp('//div[@class="viewbox"]/div[@class="info"]/text()').extract()[2]
            content_div = xp('//div[@class="viewbox"]/div[@class="content"]')[0]

        except:
            return self.parse_item2(response)

        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=datetime.now(),
            content=content,
            media=media
        )

    def parse_item2(self, response):
        
        xp = response.xpath
        try:
            title = xp("//h1[@class='article-title']/text()").extract_first() or self.get_page_title(response).split('_')[0]

            origin_name = xp('//div[@class="article-source"]/text()').extract_first('')
            content_div = xp('//div[@class="article-text"]')[0]

        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=datetime.now(),
            origin_name=origin_name,
            content=content,
            media=media
        )
