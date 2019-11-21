#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 16:36
# @Author  : wjq
# @File    : guancha_all.py


from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


class WzydAllSpider(NewsRCSpider):
    chinese_name = """文章阅读"""
    name = 'wzyd_all'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                              {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        'http://www.duwenzhang.com/':2415,
        'http://www.duwenzhang.com/wenzhang/aiqingwenzhang/':2416,
        'http://www.duwenzhang.com/wenzhang/qinqingwenzhang/':2417,
        'http://www.duwenzhang.com/wenzhang/youqingwenzhang/':2418,
        'http://www.duwenzhang.com/wenzhang/shenghuosuibi/':2419,
        'http://www.duwenzhang.com/wenzhang/xiaoyuanwenzhang/':2420,
        'http://www.duwenzhang.com/wenzhang/jingdianwenzhang/':2421,
        'http://www.duwenzhang.com/wenzhang/renshengzheli/':2422,
        'http://www.duwenzhang.com/wenzhang/lizhiwenzhang/':2423,
        'http://www.duwenzhang.com/wenzhang/gaoxiaowenzhang/':2424,
        'http://www.duwenzhang.com/wenzhang/xinqingriji/':2425,
    }

    #http://www.duwenzhang.com/wenzhang/aiqingwenzhang/shanggan/20190604/403685.html
    rules = (
        Rule(LinkExtractor(allow=(r'duwenzhang.com/.*?/%s\d{2}/\d+.html' % datetime.today().strftime('%Y%m')),),
             callback='parse_item', follow=False,process_request=js_meta),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1/text()").extract()[0]
            content_div = xp('//tr[1]/td[@class="article 0"]/div[@id="wenzhangziti"]')[0]
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
             return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=datetime.now(),
            content=content,
            media=media
        )
