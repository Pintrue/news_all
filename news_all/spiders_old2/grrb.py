# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class GrrbSpider(NewsRCSpider):
    '''工人日报'''
    name = 'grrb'
    mystart_urls = {
        'http://ent.workercn.cn/30021/30021.shtml': 1301389,  # 工人日报-娱乐-娱乐头条-头条-左侧列表
        'http://ent.workercn.cn/30031/30031.shtml': 1301388,  # 工人日报-娱乐-娱乐头条-滚动列表
    }
    rules = (
        # http://ent.workercn.cn/30021/201906/24/190624085519498.shtml
        Rule(LinkExtractor(allow=(r'workercn.cn/\d{5}/\d{6}/\d{2}/\d+\.s?html'),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='ctitle']/text()").extract_first()
            content_div = xp("//div[@class='ccontent']")[0]
            pubtime = xp("//div[@class='signdate']/span[1]/text()").extract_first()
            origin_name = xp("//div[@class='signdate']/span[2]/text()").extract_first()
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
