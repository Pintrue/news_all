# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class GjlySpider(NewsRCSpider):
    '''国际旅游岛商报'''
    # 椰网
    name = 'gjly'
    mystart_urls = {
        'https://www.hndnews.com/': 1301178,  # 国际旅游岛商报-焦点
    }
    rules = (
        # https://www.hndnews.com/p/280383.html
        Rule(LinkExtractor(allow=(r'hndnews.com/p/\d+\.html',),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//h1[@class="title"]').extract_first()
            content_div = xp('//div[@id="detail_file"]')[0]
            pubtime = xp('//div[@class="desc"]').re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')[0]
            origin_name = xp('//div[@class="desc"]/a/text()').extract_first() \
                          or xp('//span[@class="source"]/text()').extract_first()
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
