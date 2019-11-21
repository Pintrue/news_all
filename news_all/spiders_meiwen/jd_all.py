#!/usr/bin/env python 
# -*- coding:utf-8 _*-  
# Time: 2019/07/26
# Author: zcy

import re
from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider


class ChickenSoupSpider(NewsRCSpider):
    """经典网"""
    name = 'jd_all'
    mystart_urls = {
        'https://www.ishuo.cn/': 2733,  # 经典网首页
        'https://www.ishuo.cn/yulu/': 2734,  # 经典语录
        'https://www.ishuo.cn/yulu/1': 2736,  # 经典语录-经典台词
        'https://www.ishuo.cn/yulu/2': 2740,  # 经典语录-名人名言
        'https://www.ishuo.cn/yulu/8': 2744,  # 经典语录-幽默讽刺
        'https://www.ishuo.cn/yulu/4': 2746,  # 经典语录-爱情语录
        'https://www.ishuo.cn/yulu/3': 2748,  # 经典语录-真理格言
        'https://www.ishuo.cn/yulu/9': 2751,  # 经典语录-经典短信
        'https://www.ishuo.cn/lizhi/mingyan/': 2753,  # 经典励志-励志名言
        'https://www.ishuo.cn/lizhi/gushi/': 2754,  # 经典励志-励志故事
        'https://www.ishuo.cn/lizhi/wenzhang/': 2756,  # 经典励志-励志文章
        'https://www.ishuo.cn/lizhi/dianying/': 2758,  # 经典励志-励志电影
        'https://www.ishuo.cn/lizhi/gaosan/': 2760,  # 经典励志-高三励志
        'https://www.ishuo.cn/lizhi/qingchun/': 2762,  # 经典励志-青春励志
        'https://www.ishuo.cn/lizhi/qianming/': 2764,  # 经典励志-励志签名
        'https://www.ishuo.cn/lizhi/zhichang/': 2767,  # 经典励志-职场励志
        'https://www.ishuo.cn/zuowen_index.html': 2769,  # 作文网首页
        'https://www.zuowens.com/': 2771,  # 作文大全
        'https://www.wenji8.com/home/': 2774,  # 作文网
        'https://www.ishuo.cn/rizhi/': 2775,  # 经典日志-首页
        'https://www.ishuo.cn/rizhi/shanggan/': 2778,  # 经典日志-伤感日志
        'https://www.ishuo.cn/rizhi/xinqing/': 2780,  # 经典日志-心情日志
        'https://www.ishuo.cn/rizhi/kongjian/': 2782,  # 经典日志-空间日志
        'https://www.ishuo.cn/rizhi/gaoxiao/': 2732,  # 经典日志-搞笑日志
        'https://www.ishuo.cn/rizhi/aiqing/': 2806,  # 经典日志-爱情日志
        'https://www.ishuo.cn/rizhi/feizhuliu/': 2809,  # 经典日志-非主流日志
        'https://www.ishuo.cn/rizhi/weimei/': 2811,  # 经典日志-唯美日志
        'https://www.ishuo.cn/rizhi/shuoshuo/': 2812,  # 经典日志-说说日志
        'https://www.ishuo.cn/fanwen/': 2814,  # 经典范文
    }

    rules = (
        Rule(
            LinkExtractor(allow=r'ishuo.cn/.*/.*.html', ),
            callback='parse_ishuo',
            follow=False
        ),
        Rule(
            LinkExtractor(allow=r'zuowens.com/.*/.*.html', ),
            callback='parse_zuowen',
            follow=False
        ),
        Rule(
            LinkExtractor(allow=r'wenji8.com/.*/\d+.html', ),
            callback='parse_wenji8',
            follow=False
        )
    )

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    def parse_ishuo(self, response):
        xp = response.xpath
        try:
            title = xp('//h1/text()').extract_first() or self.get_page_title(response).split('-')[0]
            # info = xp('//div[@class="info"]').extract_first()
            # pubtime = re.findall('\d{4}-\d{2}-\d{2}', info)[0]
            content = xp('//div[@class="content"]')[0]
            content, media, _, _ = self.content_clean(content)
        except:
            return self.produce_debugitem(response, 'xpath error')
            
        yield self.produce_item(
            response=response,
            title=title,
            pubtime=datetime.now(),
            content=content,
            media=media
        )

    def parse_zuowen(self, response):
        # https://www.zuowens.com/450zi/asjfff.html
        xp = response.xpath
        try:
            title = xp('//h1/text()').extract_first() or self.get_page_title(response)
            # info = xp('//div[@class="info"]/text()').extract_first()
            # pubtime = re.findall('\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}', info)[0]
            content = xp('//div[@class="content"]')[0]
            content, media, _, _ = self.content_clean(content)
        except:
            return self.produce_debugitem(response, 'xpath error')
        
        yield self.produce_item(
            response=response,
            title=title,
            pubtime=datetime.now(),
            origin_name='作文网',
            content=content,
            media=media
        )

    def parse_wenji8(self, response):
        xp = response.xpath
        try:
            title = xp('//h1/text()').extract_first() or self.get_page_title(re)
            # pubtime = xp('//div[@class="info"]/text()').extract_first().strip()
            content = xp('//div[@class="content"]')[0]
            content, media, _, _ = self.content_clean(content)
        except:
            return self.produce_debugitem(response, 'xpath error')
        yield self.produce_item(
            response=response,
            title=title,
            pubtime=datetime.now(),
            content=content,
            media=media
        )