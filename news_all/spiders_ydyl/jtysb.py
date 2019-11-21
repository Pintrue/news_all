# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class JtysbSpider(NewsRCSpider):
    '''交通运输部'''
    name = 'jtysb'
    mystart_urls = {
        "http://www.mot.gov.cn/jiaotongyaowen/": 7615,
        "http://www.mot.gov.cn/zhengcejiedu/": 7616,
    }
    rules = (
        # http://www.mot.gov.cn/jiaotongyaowen/201906/t20190627_3217724.html
        Rule(LinkExtractor(allow=(r'mot.gov.cn/[a-z]+/\d{6}/t\d{8}_\d+\.html',),
                           deny=(r'http://www.mot.gov.cn/wangzhanguanli/201510/t20151018_1912374.html',
                                 r'http://www.mot.gov.cn/wangzhanguanli/201511/t20151126_1938922.html',
                                 r'http://www.mot.gov.cn/wangzhanguanli/201510/t20151018_1912376.html'),
                           ), callback='parse_item',
             follow=False),
        # http://www.mot.gov.cn/zhengcejiedu/jtysxxhbztx/
        # http://www.mot.gov.cn/zhengcejiedu/feizhibl_13/
        Rule(LinkExtractor(allow=(r'mot.gov.cn/zhengcejiedu/.+?',),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='row xq_main180625']/h1/text()").extract_first()
            content_div = xp("//div[@class='Custom_UnionStyle']")[0]
            pubtime = xp("//div[@class='row xq_main180625']/h3/font/text()").re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')[0]
            origin_name = xp("//div[@class='row xq_main180625']/h3/font/text()").extract_first().split("\xa0\xa0\xa0\xa0")[0].replace('来源：','')
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

    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='row xq_main180625']/h1/text()").extract_first()
            content_div = xp("//div[@class='TRS_Editor']")[0]
            pubtime = xp("//div[@class='row xq_main180625']/h4/text()").re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')[0]
            origin_name = xp("//div[@class='row xq_main180625']/h4/text()").extract_first().split("\xa0\xa0\xa0\xa0")[0].replace('来源：','')
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