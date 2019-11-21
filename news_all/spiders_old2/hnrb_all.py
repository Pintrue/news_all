# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Hnrb_allSpider(NewsRCSpider):
    """河南日报"""
    name = 'hnrb'
    mystart_urls = {
        'https://www.henandaily.cn/content/szheng/index.html': 1301186,  # 河南日报-时政-左侧列表采集
        'https://www.henandaily.cn/content/sh/index.html': 1301185,  # 河南日报-社会-左侧列表

    }
    rules = (
        #https://www.henandaily.cn/content/2019/0620/171682.html
        Rule(LinkExtractor(allow=(r'henandaily.cn/content/%s\d{2}/\d+.html' % datetime.today().strftime('%Y/%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='content-title']/text()").extract_first()
            content_div = xp("//div[@class='content-content']")[0]
            pubtime = xp("//span[@class='content-time']").re(r'\d{2,4}\.\d{1,2}\.\d{1,2}')[0]
            origin_name = xp("//span[@class='content-source']/text()").extract_first('')
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
