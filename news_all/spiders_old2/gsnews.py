# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class GsnewsSpider(NewsRCSpider):
    '''甘肃新闻网'''
    name = 'gsnews'
    mystart_urls = {
        'http://gansu.gscn.com.cn/gsyw/': 1301167,  # 甘肃新闻网 甘肃新闻-本网原创
    }
    rules = (
        # http://gansu.gscn.com.cn/system/2019/06/25/012176563.shtml
        Rule(LinkExtractor(allow=(r'gansu.gscn.com.cn/system/\d{4}/\d{2}/\d{2}/\d+\.s?html'),
                           deny=(r'https://live.xinhuaapp.com/xcy/reportlist.html?liveId=156092565653055&from=timeline')
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='a-header']/h1/text()").extract_first()
            content_div = xp("//div[@class='a-container']")[0]
            pubtime = xp("//span[@class='m-frt']/text()").extract_first().strip()
            origin_name = xp("//div[@class='info']/span[2]/text()").extract_first()
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