# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class DfwSpider(NewsRCSpider):
    """东方网"""
    name = 'dfw'
    mystart_urls = {
        'http://history.eastday.com/h/index.html': 18656,  # 东方网-历史
        'http://news.eastday.com/': 18655,  # 东方网-新闻-需要确定采集区域
        'http://lysh.eastday.com/lyj/Scenic_A/zxzx/index.html': 18663,  # 东方网-旅游
        'http://news.eastday.com/gd2008/finance/index.html': 18658,  # 东方网-财经
    }
    rules = (
        # http://history.eastday.com/h/20190610/u1a14892941.html
        # http://news.eastday.com/c/n1178706/u1a14917200.html
        Rule(LinkExtractor(allow=(r'eastday.com/[a-z]+/[a-z]*\d+/.*?\d+\.html'),
                           # deny=(r'http://www.eastday.com/')
                           ), callback='parse_item',
             follow=False),
        # http://lysh.eastday.com/lyj/Scenic_A/zxzx/u1ai275707.html
        # http://lysh.eastday.com/lyj/Scenic_A/zxzx/index19.html
        # http://news.eastday.com/eastday/13news/auto/news/enjoy/index_K49.html
        Rule(LinkExtractor(allow=(r'eastday.com/.*?[a-z]+_.*?\d+\.html'),
                           deny=(r'eastday.com/.*?[a-z]+_.*?/index\d+\.html',
                                 r'eastday.com/.*?/13news/.*?/index.*?\.html',
                                 # r'http://www.eastday.com/'
                                 )
                           ), callback='parse_item',
             follow=False),
        # http://photo.eastday.com/2018slideshow/20190620_3/index1.html
        Rule(LinkExtractor(allow=(r'eastday.com/\d{4}slideshow/\d{8}_\d{1}/index\d*\.html'),
                           # deny=(r'http://www.eastday.com/')
                           ), callback='parse_item',
             follow=False),
        # https://sports.eastday.com/a/190620025809905000000.html
        Rule(LinkExtractor(allow=(r'eastday.com/[a-z]+/\d+\.html'),
                           # deny=(r'http://www.eastday.com/')
                           ), callback='parse_item_sports',
             follow=False),
    )
            
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@id='biaoti']/text()")[0].extract()
            content_div = xp('//div[@id="zw"]')[0]
            pubtime = xp('//span[@id="pubtime_baidu"]/text()').extract_first()
            origin_name = xp("//div[@class='time grey12a fc lh22']/p[2]/a/text()").extract_first() or \
                          xp("//div[@class='time grey12a fc lh22']/p[2]/text()[1]").extract_first()
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item_2(self,response):
        xp = response.xpath
        try:
            title = xp("//div[@class='title tc']/text()")[0].extract()
            content_div = xp('//div[@id="zw"]')[0]
            pubtime = xp("//div[@class='grey18 lh28 tc']/text()").re(r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}')[0]
            origin_name = xp("//div[@class='grey18 lh28 tc']/text()").extract_first()
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item_sports(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='tit']/text()")[0].extract()
            content_div = xp("//div[@class='txt mt15']")[0]
            pubtime = xp("//div[@class='time']/p[@class='fl']/text()").extract_first().strip()
            origin_name = xp("//div[@class='time']/p[@class='fl']/span/text()").extract_first()
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )