# -*- coding: utf-8 -*-
import logging
from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
import time


class NmgnewsSpider(NewsRCSpider):
    """内蒙古新闻网"""
    name = 'nmgnews'
    mystart_urls = {
        'http://china.nmgnews.com.cn/': 1301468,  # 内蒙古新闻网 国内频道-全部列表采集
        'http://inews.nmgnews.com.cn/nmgxw/kjwwxw/': 1301466,  # 内蒙古新闻网 科教文卫-左侧列表
        'http://inews.nmgnews.com.cn/nmgxw/jjxw/': 1301465,  # 内蒙古新闻网 经济新闻-左侧列表
        'http://inews.nmgnews.com.cn/nmgxw/syxw/': 1301467,  # 内蒙古新闻网 综合新闻
    }
    
    rules = (
        # http://china.nmgnews.com.cn/system/2019/07/02/012736421.shtml
        # http://inews.nmgnews.com.cn/system/2019/07/05/012739043.shtml
        Rule(LinkExtractor(allow=r'nmgnews.com.cn/system/%s/\d{2}/\d+\.s?html?' % time.strftime("%Y/%m"),
                           # deny=(),
                           ),
             callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=r'nmgnews.com.cn.*?\d+\.s?html?',
                           deny=(r'/201[0-8]', r'/2019/0[1-9]')
                           ),
             process_request=otherurl_meta,
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            sdiv = xp('//div[@id="div3"]')[0]
            pubtime = sdiv.re('\d{2,}-\d{2}-\d{2} \d{2}:\d{2}')[0]  # 19-07-05 09:44
            content_div = xp('//div[@id="div_content"]')[0]
            content, media, videos, cover = self.content_clean(content_div, need_video=True)
            og = sdiv.re('来源：\w+')
            origin_name = og[0] if og else ""
        except:
            return self.produce_debugitem(response, "xpath error")
        title = self.get_page_title(response).split('-')[0]
        next_a = xp('//div[@id="news_more_page_div_id"]/a[text()="下一页"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'origin_name': origin_name,
                                         'content': content_div.extract(), 'title': title,
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         })
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,
        )

    def parse_page(self, response):
        meta_new = deepcopy(response.meta)
        xp = response.xpath
        try:
            content_div = xp('//div[@id="div_content"]')[0]
        except Exception as e:
            return self.produce_debugitem(response, 'xpath error')
    
        meta_new['content'] += content_div.extract()
    
        next_a = xp('//div[@id="news_more_page_div_id"]/a[text()="下一页"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
    
        content, media, videos, video_cover = self.content_clean(meta_new['content'],
                                                                     kill_xpaths='//div[@id="news_more_page_div_id"]')
    
        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),

            content=content,
            media=media
        )