# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Jingchu_allSpider(NewsRCSpider):
    """荆楚网"""
    name = 'jcw'
    mystart_urls = {
        'http://news.cnhubei.com/xw/gn/': 1301456,  # 荆楚网-国内
        'http://news.cnhubei.com/xw/gj//': 1301455,  # 荆楚网-国际
        'http://news.cnhubei.com/xw/yl/': 1301457,  # 荆楚网-娱乐新闻
        'http://news.cnhubei.com/xw/sh/': 1301454,  # 荆楚网-社会列表

    }
    rules = (
        #http://news.cnhubei.com/xw/gn/201901/t4209364.shtml
        #http://news.cnhubei.com/xw/gj//201901/t4209648.shtml
        Rule(LinkExtractor(allow=(r'news.cnhubei.com.*?/%s/t\d+.shtml' % datetime.today().strftime('%Y%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='title']/text()").extract_first()
            content_div = xp("//div[@class='TRS_Editor']")[0]
            pubtime = xp("//div[@class='jcwsy_mini_content']/span[1]").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//a[@id='source_url']/text()").extract_first('')
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
