# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class SfbSpider(NewsRCSpider):
    '''司法部'''
    name = 'sfb'
    mystart_urls = {
        "http://www.moj.gov.cn/news/node_zfyw.html": 7611,
    }
    rules = (
        # http://www.moj.gov.cn/news/content/2019-06/22/zfyw_3226423.html
        Rule(LinkExtractor(allow=(r'gov.cn/news/content/\d{4}-\d{2}/\d{2}/zfyw_\d+\.html',),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title_total = xp("//div[@class='con_bt']/text()").extract()
            title = ''
            for i in range(len(title_total)):
                title = title + title_total[i]
            content_div = xp("//div[@id='content']")[0]
            pubtime = xp("//div[@class='con_time']/span[1]/text()").extract_first().strip()
            origin_name = xp("//div[@class='con_time']/span[2]/text()").extract_first()
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media
        )
