#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 18:54
# @Author  : wjq
# @File    : kr36_all.py
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class KrAllSpider(NewsRCSpider):
    chinese_name = """36氪网站"""
    name = 'kr36_all'
    mystart_urls = {
        'https://36kr.com/information/web_recommend': 2592,
        'https://36kr.com/information/contact': 2593,
        'https://36kr.com/information/technology': 2594,
    }
    
    # https://36kr.com/p/5209064
    rules = (
        Rule(LinkExtractor(allow=(r'36kr.com/p/\d+',),
                           # restrict_xpaths=r''
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'36kr.com'), deny=(r'/201[0-8]', r'/20190[1-9]/',),
                           # restrict_xpaths=r''
                           ),
             process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        if '本文来自36氪付费栏目' in response.text:  # https://36kr.com/p/5210723  本文来自36氪付费栏目《36氪每日商业精选》
            return self.produce_debugitem(response, '本文来自36氪付费栏目')
        
        xp = response.xpath
        
        try:
            ss = xp('//script[contains(text(), "window.initialState")]/text()')[0].extract()
            start = ss.index('{"articleDetail":')
            
            rj = json.loads(ss[start:]).get('articleDetail').get('articleDetailData').get('data')
            pubtime = rj.get('published_at')
            
            
            title = rj.get('title')
            content_div = rj.get('content')
            # <p>我是36氪记者陈绍元，关注物联网、AI、科技，交流或寻求报道(不收费)加微信:963757163，请注明公司、职位、姓名。</p>
            content, media, _, _ = self.content_clean(content_div, kill_xpaths=[r'//address', r'//*[text()="——————"]',
                                                                                r'//p[starts-with(text(),"我是36氪")]'])
        except:
            return self.produce_debugitem(response, "xpath error")
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="36氪",
            content=content,
            media=media
        )
