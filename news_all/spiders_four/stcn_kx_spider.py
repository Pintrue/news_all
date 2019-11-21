# -*- coding: utf-8 -*-
# @Time   : 2019/3/4 下午4:25
# @Author : NewmanZhou
# @Project : news_all
# @FileName: stcn_kx_spider.py

import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, isStartUrl_meta


class StcnKXSpipder(NewsRCSpider):
    name = 'stcn_kx_spider'

    # 证券时报 ==》 首页 ==》 快讯
    mystart_urls = {
        'http://kuaixun.stcn.com/index.shtml': 495,  # '快讯列表'
    }

    rules = (Rule(LinkExtractor(allow=r'kuaixun.stcn.com/.*?\d+.s?htm', deny=('video', 'audio'),
                                restrict_xpaths='//ul[@id="news_list2"]'),
                  callback='parse_item', follow=False),
             # http://kuaixun.stcn.com/index_2.shtml
             # 线上只需要24小时的新闻
             Rule(LinkExtractor(allow=r'kuaixun.stcn.com/index_\d+.s?htm', deny=('video', 'audio'),
                                restrict_xpaths='//div[@class="pagelist1"]//a[@class="next"]'),
                  follow=True, process_request=isStartUrl_meta)
             )
    custom_settings = {'DEPTH_LIMIT': 3}

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='intal_tit']/h2/text()").extract()[0]
            pubtimeStr = xp("//div[@class='intal_tit']/div/text()").extract_first('')
            pubtime = re.findall(r'\d{2,4}.\d{1,2}.\d{1,2}.\d{1,2}:\d{1,2}|\d{2,4}.\d{1,2}.\d{1,2}', pubtimeStr)[0]
            origin_name = xp("//div[@class='intal_tit']/div/span/text()").extract_first('')
            cv = xp('//div[@id="ctrlfscont"]').extract_first()
            content, media, videos, cover = self.content_clean(cv, need_video=True)
        except BaseException:
            return self.parse_item2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )

    def parse_item2(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='box_r']/h2/text()").extract()[0]
            pubtime = xp("//div[@class='box_r']/h2/span/text()").extract_first('')
            origin_name = xp("//div[@class='intal_tit']/div/span/text()").extract_first('')
            cv = xp('//div[@class="left_txt"]').extract_first()
            content, media, videos, cover = self.content_clean(cv, need_video=True)
        except BaseException:
            return self.parse_item3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )

    def parse_item3(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='xiangxi']/h2/text()").extract()[0]
            pubtimeStr = xp("//div[@class='xiangxi']/h2/span/text()").extract_first('')
            pubtime = re.findall(r'\d{2,4}.\d{1,2}.\d{1,2}.\d{1,2}:\d{1,2}', pubtimeStr)[0]
            origin_name = re.findall('来源：(.+)?', pubtimeStr)[0].strip()
            cv = xp('//div[@id="ctrlfscont"]').extract_first()
            content, media, videos, cover = self.content_clean(cv, need_video=True)
        except BaseException:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )

