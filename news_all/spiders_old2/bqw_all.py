# -*- coding: utf-8 -*-

from scrapy.conf import settings
from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider
from news_all.tools.time_translater import Pubtime


class Bqw_allSpider(NewsRCSpider):
    """北青网"""
    name = 'bqw'
    mystart_urls = {
        'http://ent.ynet.com/list/1143t1257.html': 1301344,  # 北青网 演唱文-列表及右侧头条
        'http://ent.ynet.com/list/1092t1257.html': 1301343,  # 北青网 电影-电影头条及右侧头条
        'http://ent.ynet.com/list/1107t1257.html': 1301342,  # 北青网 电视
        'http://ent.ynet.com/list/1110t1257.html': 1301346,  # 北青网 综艺
        'http://ent.ynet.com/list/1128t1257.html': 1301345,  # 北青网 音乐
        'http://ent.ynet.com/list/1074t1257.html': 1301133,  # 北青网-红人-左侧列表右侧头条
        'http://ent.ynet.com/list/1155t1257.html': 1301132,  # 北青网娱乐-滚动-全部采集
    }
    rules = (
        # http://ent.ynet.com/2019/06/13/1880983t1254.html
        # http://ent.ynet.com/2019/06/13/1880944t1254.html
        # http://ent.ynet.com/2019/07/26/1970725t1254.html
        Rule(LinkExtractor(allow=(r'ent.ynet.com/%s/\d{2}/\d+t\d+.html' % datetime.today().strftime('%Y/%m'),),
                           ), callback='parse_item',
             follow=False),
    )
    
    custom_settings = {
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    # todo xpath error 'http://ent.ynet.com/2019/07/25/1968034t1254.html'
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='articleTitle']/h1/text()").extract_first() or self.get_page_title(
                response).replace('_YNET.com北青网', '')
            content_div = xp("//div[@id='articleAll']")[0]
            pubtime = Pubtime(xp("//div[@id='msgBox']/p[@class='sourceBox']")[0].extract())
            origin_name = xp('//div[@id="msgBox"]/p[@class="sourceBox"]/span[@class="sourceMsg"]/text()').extract_first(
                '')
        except:
            return self.produce_debugitem(response, "xpath error")
        # next_a = xp('//ul[contains(@class, "pageBox")]/li/a[contains(text(),"下一页")]')
        # http://ent.ynet.com/2019/07/26/1970815t1254.html     # following-sibling 同级之后的节点
        next_a = xp('//ul[contains(@class, "pageBox")]/li[@class="active"]/following-sibling::li/a')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')})
        
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
            cvs = xp("//div[@id='articleAll']") or xp("//ul[@class='article_content']")
            content_div = cvs[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()
        
        next_a = xp('//ul[contains(@class, "pageBox")]/li[@class="active"]/following-sibling::li/a') or xp(
            '//li[@id="ff"]/a/*[text()="下一页"]/parent::a') or xp('//li[@id="ff"]/a[text()="下一页"]')
        if next_a:
            next_url = next_a.xpath('@href').extract_first()
            if 'http://h5.news.ynet.com/h5' not in next_url:
                return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
        
        content, media, videos, video_cover = self.content_clean(meta_new['content'],
                                                                 kill_xpaths=['//ul[contains(@class, "pageBox")]',
                                                                              '//span[@class="authors"]',
                                                                              '//p[@class="editor"]/following::*',
                                                                              '//li[@class="img_content"]//h3'
                                                                              ])
        
        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),
            content=content,
            media=media
        )
    
    def parse_item_2(self, response):
        # http://ent.ynet.com/2019/07/26/1970725t1254.html
        
        xp = response.xpath
        try:
            title = xp("//div[@id='nr']/h1/text()").extract_first() or self.get_page_title(
                response).replace('_YNET.com北青网', '')
            content_div = xp("//ul[@class='article_content']")[0]
            pubtime = Pubtime(xp("//div[@id='nr']/h2").extract_first())
        except:
            return self.produce_debugitem(response, "xpath error")
        next_a = xp('//li[@id="ff"]/a/*[text()="下一页"]/parent::a') or xp('//li[@id="ff"]/a[text()="下一页"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')})
        
        content, media, _, _ = self.content_clean(content_div, kill_xpaths=['//p[@class="editor"]/following::*',
                                                                            '//li[@class="img_content"]//h3'])
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media
        )
    
    # def parse_page_2(self, response):
    #     xp = response.xpath
    #     meta_new = deepcopy(response.meta)
    #     try:
    #
    #     except:
    #         return self.produce_debugitem(response, 'xpath error')
    #     meta_new['content'] += content_div.extract()
    #
    #     next_a = xp('//li[@id="ff"]/a/*[text()="下一页"]/parent::a') or xp('//li[@id="ff"]/a[text()="下一页"]')
    #     if next_a:
    #         return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
    #
    #     content, media, videos, video_cover = self.content_clean(meta_new['content'],
    #                                                              kill_xpaths=['//p[@class="editor"]/following::*',
    #                                                                           '//p[@class="editor"]',
    #                                                                           '//li[@class="img_content"]//h3'])
    #
    #     return self.produce_item(
    #         response=response,
    #         title=meta_new.get('title'),
    #         pubtime=meta_new.get('pubtime'),
    #         content=content,
    #         media=media
    #     )
