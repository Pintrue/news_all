#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 16:36
# @Author  : wjq
# @File    : guancha_all.py

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider,js_meta


class JcmwAllSpider(NewsRCSpider):
    chinese_name = """精彩美文"""
    name = 'jcmw_all'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            },
                       'DOWNLOAD_TIMEOUT': 240}
    
    start_meta = {'jstype': True}
    mystart_urls = {
        'https://story.5article.com/aiqing/':646,
        'https://story.5article.com/zheli/':648,
        'https://story.5article.com/qinqing/':651,
        'https://story.5article.com/sex/':654,
        'https://story.5article.com/xiandai/':774,
        'https://story.5article.com/shaoer/tonghua/':856,
        'https://story.5article.com/mingren/':857,
        'https://story.5article.com/chuangye/':1018,
        'https://story.5article.com/lishi/':1054,
        'https://story.5article.com/gui/':1055,
        'https://www.5article.com/jingdian/qinggan/':1059,
        'https://www.5article.com/jingdian/zheli/':1060,
        'https://www.5article.com/jingdian/shanggan/':1061,
        'https://www.5article.com/jingdian/suibi/':1062,
        'https://www.5article.com/jingdian/ganwu/':1063,
        'https://www.5article.com/sanwen/aiqing/':1064,
        'https://www.5article.com/sanwen/shanggan/':1067,
        'https://www.5article.com/sanwen/shuqing/':1121,
        'https://www.5article.com/sanwen/xiejing/':1165,
        'https://www.5article.com/sanwen/jingdian/':1314,
        'https://www.5article.com/sanwen/youmei/':1333,
        'https://www.5article.com/wenzhang/juzi/':1335,
        'https://www.5article.com/wenzhang/yulu/':1338,
        'https://www.5article.com/wenzhang/duanxin/':1448,
        'https://www.5article.com/wenzhang/zawen/':1583,
        'https://www.5article.com/wenzhang/gexing/':1681,
        'https://www.5article.com/wenzhang/rizhi/':1683,
        'https://www.5article.com/wenzhang/wenzhang/':1685,
        'https://www.5article.com/wenzhang/sanwen/':1802,
        'https://www.5article.com/wenzhang/renshengganwu/':1856,
    }
    #https://www.5article.com/view/112871.html
    #https://story.5article.com/view/29114.html
    #https://www.5article.com/topic/150713.html

    rules = (
        Rule(LinkExtractor(allow=(r'5article.com/.*?/\d+.html'),),
             callback='parse_item', follow=False,process_request=js_meta),
    )

    #https://www.5article.com/topic/150713.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='box']/h1[@class='h1']/text()").extract_first() or self.get_page_title(response)
            # pubtime = xp('//h1[@class="h1"]/div[@class="p"]').re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{2}:\d{2}')[0]
            # 
            #     self.log('out of LimitatedDaysHoursMinutes: %s' % response.url, logging.DEBUG)
            # 
            #     
            # origin_name = xp('//dd/div[@class="con-tit"]/p/text()').extract()[0].split()[2].replace('来源:','')
            content_div = xp('//div[@id="Article"]/div[@class="content_z"]')[0]

        except:
            return self.parse_item2(response)

        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=datetime.now(),
            # origin_name=origin_name,
            content=content,
            media=media
        )

    #https://story.5article.com/view/9820.html
    def parse_item2(self, response):
        
        xp = response.xpath
        try:
            title = xp("//div[@class='content-title']/h1/text()").extract_first() or self.get_page_title(response)
            # pubtime = xp('//div[@class="writer"]/span[1]').re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{2}:\d{2}')[0]
            # 
            #     self.log('out of LimitatedDaysHoursMinutes: %s' % response.url, logging.DEBUG)
            # 
            #     
            # origin_name = xp('//dd/div[@class="con-tit"]/p/text()').extract()[0].split()[2].replace('来源:','')
            content_div = xp('//div[@class="content article"]')[0]

        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=datetime.now(),
            content=content,
            media=media
        )

