# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class CntheoryAllSpider(NewsRCSpider):
    """理论网"""
    name = 'cntheory_all'
    mystart_urls = {
        'http://www.cntheory.com/zydx/ddjs/index.html': 2017,
        'http://www.cntheory.com/zydx/jjjs/index.html': 2018,
        'http://www.cntheory.com/zydx/jszl/index.html': 2019,
        'http://www.cntheory.com/zydx/shjs/index.html': 2020,
        'http://www.cntheory.com/zydx/stwmjs/index.html': 2021,
        'http://www.cntheory.com/zydx/whjs/index.html': 2022,
        'http://www.cntheory.com/zydx/wj/index.html': 2023, 'http://www.cntheory.com/zydx/zl/index.html': 2024,
        'http://www.cntheory.com/zydx/zzjs/index.html': 2025
    }

    # http://www.cntheory.com/zydx/2019-04/ccps190416O7PS.html
    rules = (
        Rule(LinkExtractor(allow=(r'cntheory.com.*?/%s/\w+.html'%datetime.today().strftime('%Y-%m')), ),
                           callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'cntheory.com.*?\w+.html'), deny=(r'/201[0-8]', r'/2019-0[1-8]/', r'/index_\d+.html')),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('.//div[@class="font_36"]/text()')[0].extract()
            source_div = xp('.//table[@class="ke-zeroborder"][2]/tbody/tr/td/table')[0]
            content_div = xp('.//div[@class="font_16"]')[0]
            # pubtime = source_div.xpath('./div[@class="ly"]/span[@id="time_tex"]/text()').extract_first('').strip()
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media
        )
