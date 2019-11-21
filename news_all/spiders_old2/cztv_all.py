# -*- coding: utf-8 -*-

from copy import deepcopy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider


class CztvAllSpider(NewsRCSpider):
    """新蓝网"""
    name = 'cztv_all'

    mystart_urls = {
        'http://n.cztv.com/sport/': 1301529,  # 新蓝网-体育-左侧列表
        'http://n.cztv.com/national/': 1301531,  # 新蓝网-国内-左下列表
        'http://n.cztv.com/world/': 1301530,  # 新蓝网-国际-左下列表
        'http://n.cztv.com/wy/': 1301532,  # 新蓝网-文娱-左下列表
        'http://n.cztv.com/zhejiang/': 1301528,  # 新蓝网-浙江

    }

    # http://n.cztv.com/news/13218473.html    http://n.cztv.com/news/13215981.html
    rules = (
        Rule(LinkExtractor(allow=r'cztv.com/news/\d+.html',
                           deny='video', ), callback='parse_item',
             follow=False),
    )

    custom_settings = {
        # 'DEPTH_LIMIT': 3,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
            
    # http://n.cztv.com/news/13215981.html
    def parse_item(self, response):
        xp = response.xpath
        if xp('//div[contains(@class, "video_box")]'):
            return self.produce_debugitem(response, 'video filter')
        try:
            title = xp('//h1/text()').extract()[0]
            content_div = xp('//div[@id="zoom"]')[0]
            source_div = xp('//div[@class="publish"]')[0]
            pubtime = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}')[0]
            origin_name = source_div.xpath('.//ul/li[1]/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,
        )