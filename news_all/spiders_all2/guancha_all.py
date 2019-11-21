#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 16:36
# @Author  : wjq
# @File    : guancha_all.py


from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class GuanchaAllSpider(NewsRCSpider):
    chinese_name = """观察者网站"""
    name = 'guancha_all'
    mystart_urls = {
        'https://www.guancha.cn/military-affairs?s=dhjunshi': 2585,
        'https://www.guancha.cn/economy?s=dhcaijing': 2586,
        'https://www.guancha.cn/gongye%C2%B7keji?s=dhgongye%C2%B7keji': 2587,
        'https://www.guancha.cn/JunShi/list_1.shtml': 2684,
        'https://www.guancha.cn/GuoJi%C2%B7ZhanLue/list_1.shtml': 2685,
}
    # https://www.guancha.cn/military-affairs/2019_05_23_502830.shtml
    rules = (
        Rule(LinkExtractor(allow=(r'guancha.cn/.*?/%s_\d{2}_\d+.s?htm' % datetime.today().strftime('%Y_%m')), ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'guancha.cn.*?\d+.s?htm'), deny=(r'/201[0-8]', r'/2019_0[1-4]', r'list_\d+.s?htm')),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            pubtime = xp('//div[@class="time fix"]/span[1]/text()')[0].extract()
            origin_name = xp('//div[@class="time fix"]/span[3]/text()').extract_first('')
            content_div = xp('//div[@class="content all-txt"]')[0]
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=self.get_page_title(response),
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )