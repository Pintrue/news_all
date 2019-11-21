# -*- coding: utf-8 -*-
# @Time   : 2019/3/1 下午5:59
# @Author : NewmanZhou
# @Project : news_all
# @FileName: people_gdyw_spider.py


from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import isStartUrl_meta
from news_all.spiders.people import PeopleSpider
import re


class PeopleGDYWSpipder(PeopleSpider):
    name = 'people_gdyw_spider'
    
    # 人民健康网
    mystart_urls = {
        'http://health.people.com.cn/GB/415859/index.html': 222,  # '今日要闻（滚动新闻）'--'滚动新闻'
        'http://health.people.com.cn/GB/408572/index.html': 415,  # '养生'
        'http://health.people.com.cn/GB/408575/index.html': 416,  # '美容'
        'http://health.people.com.cn/GB/408571/index.html': 417,  # '健身'

        'http://health.people.com.cn/GB/408567/index.html': 419,  # '医学前沿'
        'http://health.people.com.cn/GB/408564/index.html': 424,  # '政策声音'
        'http://health.people.com.cn/GB/408565/index.html': 425,  # '行业热点'
    }
    
    # http://health.people.com.cn/n1/2019/0301/c14739-30953006.html
    rules = (Rule(
        LinkExtractor(allow=r'health.people.com.cn/.*?/%s\d{2}/c\d+-\d+.html' % datetime.today().strftime('%Y/%m'),
                      deny=('video', 'audio'),
                      restrict_xpaths="//div[@class='columWrap']"),
        callback='parse_item', follow=False),
             Rule(LinkExtractor(allow=r'health.people.com.cn/GB/415859/index\d+.html',
                                restrict_xpaths='//div[@class="pageNum"]/a[text()="下一页"]'),
                  follow=True, process_request=isStartUrl_meta),
    )
    custom_settings = {
        'DEPTH_LIMIT': 3,  # 翻页需要设置深度为0 或者 >1
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % PeopleSpider.name,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            pubtimeStr = xp('//div[@class="artOri"]').extract()[0]
            pubtime = re.findall(r'\d{2,4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{1,2}', pubtimeStr)[0]
            cv = xp('//div[@class="articleCont"]/div[@class="artDet"]')[0]
            content, media, video, cover = self.content_clean(cv, need_video=False)
            title = xp('//div[@class="title"]/h2/text()').extract()[0]

            origin_name = xp('//div[@class="artOri"]/a/text()').extract()[0]
        except:
            return super(PeopleGDYWSpipder, self).parse_item(response)

        return self.produce_item(
            response=response,  # must
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )


class PeopleSPSYSpipder(PeopleSpider):
    name = 'people_spsy_spider'
    
    # 人民健康网==》食品
    mystart_urls = {
        'http://shipin.people.com.cn/': 426,  # '食品首页'
        'http://shipin.people.com.cn/GB/395905/index.html': 186242,  # 427,  # '行业24小时'
        'http://shipin.people.com.cn/GB/395906/index.html': 186244,  # 428,  # '吃喝百宝袋'
    }
    custom_settings = {
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % PeopleSpider.name,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    # http://shipin.people.com.cn/n1/2019/0304/c85914-30955501.html
    rules = (Rule(
        LinkExtractor(allow=r'shipin.people.com.cn/.*?/%s\d{2}/c\d+-\d+.html' % datetime.today().strftime('%Y/%m'),
                      deny=('video', 'audio'),
                      restrict_xpaths=["//div[@class='p1_content w1000']", "//div[@class='p2_left ej_left']",
                                       "//div[@class='p2_title clearfix']/ul/li[@id='p2Aa_1']"]),
        callback='parse_item', follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        
        try:
            title = xp("//div[@class='clearfix w1000_320 text_title']/h1/text()").extract()[0]
            cent = xp("//div[@class='fl text_con_left']/div[@id='rwb_zw']")[0]
            content, media, video, cover = self.content_clean(cent, need_video=False)
            pubtimeStr = xp("//div[@class='box01']/div[@class='fl']/text()").extract()[0]
            pubtime = re.findall(r'\d{2,4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{1,2}', pubtimeStr)[0]
            origin_name = xp("//div[@class='box01']/div[@class='fl']/a/text()").extract()[0]
        except:
            return self.parse_item_newman2(response)
        
        return self.produce_item(
            response=response,  # must
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )
    
    def parse_item_newman2(self, response):
        xp = response.xpath
        
        try:
            title = xp("//div[@class='title']/h2/text()").extract()[0]
            cent = xp("//div[@class='articleCont']/div[@class='artDet']")[0]
            pubtimeStr = xp("//div[@class='articleCont']/div[@class='artOri']/text()").extract()[0]
            pubtime = re.findall(r'\d{2,4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{1,2}', pubtimeStr)[0]
            origin_name = xp("//div[@class='articleCont']/div[@class='artOri']/a/text()").extract()[0]
        except:
            return super(PeopleSPSYSpipder, self).parse_item(response)
        
        content, media, video, cover = self.content_clean(cent, need_video=False)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )


class PeopleZYYSYSpipder(PeopleSPSYSpipder):
    name = 'people_zyysy_spider'
    
    # 人民健康网==》中医药
    mystart_urls = {
        'http://health.people.com.cn/GB/420321/index.html': 429,  # '中医药==》中医药首页，' todo 和430 url相同
    }
    
    # http://health.people.com.cn/n1/2018/0828/c14739-30255131.html
    rules = (Rule(
        LinkExtractor(allow=r'health.people.com.cn/.*?/%s\d{2}/c\d+-\d+.html' % datetime.today().strftime('%Y/%m'),
                      deny=('video', 'audio'),
                      restrict_xpaths="//div[@class='clearfix p1_con w1000']"),
        callback='parse_item', follow=False),
             )
    custom_settings = {
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % PeopleSpider.name,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }


# 2019年7月8日核对source_id 删重复url
# class PeopleZYYHY24HSpipder(PeopleSPSYSpipder):
#     name = 'people_zyyhy24h_spider'
#
#     # 人民健康网==》中医药
#     mystart_urls = {
#         'http://health.people.com.cn/GB/420321/index.html': 430,  # '中医药==》行业24小时，'
#     }
#
#     # http://health.people.com.cn/n1/2018/0828/c14739-30255131.html
#     rules = (Rule(
#         LinkExtractor(allow=r'health.people.com.cn/.*?/%s\d{2}/c\d+-\d+.html' % datetime.today().strftime('%Y/%m'),
#                       deny=('video', 'audio'),
#                       restrict_xpaths="//div[@class='fl headingNews_con']/div[@class='headingNews headingNews_a']"),
#         callback='parse_item', follow=False),
#              )
#     custom_settings = {
#         'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
#         'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % PeopleSpider.name,
#         'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
#     }