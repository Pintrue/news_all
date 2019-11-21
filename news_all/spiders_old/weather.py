#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 17:25
# @Author  : wjq
# @File    : weather.py

from copy import deepcopy
from datetime import datetime
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta, otherurl_meta
from news_all.tools.time_translater import Pubtime


class WeatherSpider(NewsRCSpider):
    """中国天气网"""
    name = 'weather'
    mystart_urls = {
        'http://www.weather.com.cn/index/jqzdtqsj/index.shtml': 1302262,  # 中国天气网
    }
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    rules = (
        # http://p.weather.com.cn/2019/06/3205336.shtml
        Rule(LinkExtractor(
            allow=(
                r'p.weather.com.cn/%s/\d+.s?htm' % datetime.today().strftime('%Y/%m'),),
            # deny=(r'',)
        ),
            callback='parse_images', follow=False),
        # http://www.weather.com.cn/index/2019/06/3200897.shtml
        # http://www.weather.com.cn/video/2019/06/3206360.shtml
        # http://news.weather.com.cn/2019/06/3206451.shtml
        Rule(LinkExtractor(
            allow=(r'weather.com.cn.*?/%s/\d+.shtml' % datetime.today().strftime('%Y/%m')),
            deny=(r'/video/', r'/zt/tqzt/', r'/weather_error_404')
            # <200 http://www.weather.com.cn/other/weather_error_404.html?r=www.weather.com.cn/mtqtj/zrds/2019/06/3205522.shtml>
        ),
            callback='parse_item', follow=False),
        
        Rule(LinkExtractor(
            # allow=(r'weather.com.cn/alarm/newalarmcontent.shtml\?file=\d+-%s\d+-\d+.html' % datetime.today().strftime('%Y%m'),
            allow=(r'weather.com.cn/alarm/newalarmcontent.shtml',),
            deny=(r'/video/', r'/zt/tqzt/', r'/weather_error_404')
            # <200 http://www.weather.com.cn/other/weather_error_404.html?r=www.weather.com.cn/mtqtj/zrds/2019/06/3205522.shtml>
        ),
            callback='parse_item', follow=False),
        # /html/body/div[2]/div/span[8]
        
        Rule(LinkExtractor(
            allow=(r'weather.com.cn.*?\d+.s?htm',),
            deny=(r'/201[0-8]', r'/2019/0[1-9]', r'/2019-0[1-9]', r'/2019_0[1-9]', r'/20190[1-9]', '/index.htm',
                  r'/weather1d/\d+.shtml', r'/index_\d+.s?htm', r'/zt/tqzt/')
        ),
            process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            ps = xp('//div[@class="articleInfo"]/span[1]/text()') or xp(
                '//div[@class="articleTimeSizeleft"]/span[1]/text()') or xp(
                '//ul[@class="lunboinfoUl"]/li[1]/text()') or xp('//div[@class="xyn-cont-time"]')
            pubtime = Pubtime(ps[0].extract())
            cvs = xp('//div[@class="articleBody"]') or xp('//div[@class="xyn-cont-left"]/div[@class="xyn-text"]')
            content_div = cvs[0]
            title = xp('//div[@class="xyn-cont-left"]/h2/text()').extract_first("") or \
                    self.get_page_title(response).split('-')[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        
        content, media, _, _ = self.content_clean(content_div, kill_xpaths='//div[@class="shoucang"]')
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="中国天气网",
            content=content,
            media=media
        )
    
    def parse_images(self, response):
        
        xp = response.xpath
        try:
            ps = xp('//div[@class="articleInfo"]/span[1]/text()') or xp('//ul[@class="lunboinfoUl"]/li[1]/text()')
            pubtime = Pubtime(ps[0].extract())
            content_div = xp('//div[@class="carousel carousel-stage"]/ul')
            if content_div:
                content, media, _, _ = self.content_clean(content_div, kill_xpaths='//div[@class="shoucang"]')
            else:
                content_div = xp('//div[@class="container"]/div//li[@class="child"]/a/img')
                content, media = self.make_img_cont(content_div)
            title = xp('//div[@class="title"]/text()').extract_first("") or self.get_page_title(response).split('-')[0]
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="中国天气网",
            content=content,
            media=media
        )
    
    def make_img_cont(self, content_div):
        """
       <img class="lunboimgages xh-highlight" src="http://..jpg" imgtitle="图为..">
        """
        media = {'images': {}}
        content = ''
        for i, j in enumerate(content_div):
            content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
            media['images'][str(i + 1)] = {'src': j.xpath('@src').extract_first()}
            content += '<p>' + j.xpath('@imgtitle').extract_first() + '</p>'
        return content, media


class WeatherJsSpider(NewsRCSpider):
    """中国天气网js"""
    name = 'weather_js'
    mystart_urls = {
        'http://www.weather.com.cn/alarm/warninglist1.shtml': 1302261,  # 中国天气网  # todo 浏览器按下一页
    }
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':
            {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
             'news_all.middlewares.UserAgentMiddleware': 20,
             'news_all.middlewares.PhantomJSMiddleware': 540,
             'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
             }}
    start_meta = {'jstype': True}
    rules = (
        Rule(LinkExtractor(
            # allow=(r'weather.com.cn/alarm/newalarmcontent.shtml\?file=\d+-%s\d+-\d+.html' % datetime.today().strftime('%Y%m'),
            allow=(r'weather.com.cn/alarm/newalarmcontent.shtml',),
            deny=(r'/video/', r'/zt/tqzt/', r'/weather_error_404')
        ),
            callback='parse_item', follow=False, process_request=js_meta),
        
        Rule(LinkExtractor(
            allow=(r'weather.com.cn.*?\d+.s?htm',),
            deny=(r'/201[0-8]', r'/2019/0[1-9]', r'/2019-0[1-9]', r'/2019_0[1-9]', r'/20190[1-9]', '/index.htm',
                  r'/weather1d/\d+.shtml', r'/index_\d+.s?htm', r'/zt/tqzt/')
        ),
            process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            sdiv = xp('//div[@class="xyn-cont-time"]')[0]
            pubtime = sdiv.re(r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}')[0]  # 2019-06-09 07:30:29
            content_div = xp('//div[@class="xyn-cont-left"]/div[@class="xyn-text"]')[0]
            title = xp('//div[@class="xyn-cont-left"]/h2/text()').extract_first("")
            content, media, _, _ = self.content_clean(content_div, kill_xpaths='//div[@class="shoucang"]')
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="中国天气网",
            content=content,
            media=media
        )
