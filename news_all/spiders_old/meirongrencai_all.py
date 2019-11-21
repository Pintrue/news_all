# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Meirongrencai_allSpider(NewsRCSpider):
    """美容人才网"""
    name = 'mrrcw'
    mystart_urls = {
        'http://www.138job.com/shtml/Article/?from=shtml_Article': 2946,  # 美容人才网-职场
    }
    rules = (
        #http://www.138job.com/shtml/SPbeauticians/18906/111067.shtml
        Rule(LinkExtractor(allow=(r'138job.com/shtml.*?/\d{5}/\d+.shtml'),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='news_header']/h2/text()").extract_first()
            content_div = xp("//div[@class='news_content']")[0]
            pubtime = xp("//div[@class='news_header']/h5/em[1]").re(r'\d{2,4}\.\d{1,2}\.\d{1,2}')[0]
            origin_name = xp("//div[@class='news_header']/h5/em[2]/text()").extract_first('')
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
