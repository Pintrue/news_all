# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class QgdminfoSpider(NewsRCSpider):
    '''全国党媒信息公共平台-财经'''
    name = 'qgdminfo'
    mystart_urls = {
        'https://original.hubpd.com/': 1000002,  # 全国党媒信息公共平台-财经
    }
    rules = (
        # https://original.hubpd.com/c/2019-06-11/813171.shtml
        Rule(LinkExtractor(allow=(r'original.hubpd.com/c/%s-\d{2}/\d+.s?html' % datetime.today().strftime('%Y-%m'),),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//h3[@class="bold mainTit one text-black"]/text()').extract_first()
            content_div = xp('//div[@class="m-lg art_txt_con"]')[0]

            pubtime = xp('//div[@class="pull-left art_time"]/text()').extract_first()
            
                
            origin_name = xp('//div[@class="pull-left art_Source"][1]/text()').extract_first()
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )
