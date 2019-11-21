# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class DangJianAllSpider(NewsRCSpider):
    """中国党网"""
    name = 'dangjian_all'
    mystart_urls = {

        'http://dangjian.com/djw2016sy/djw2016syyw/': 1573,
        'http://dangjian.com/djw2016sy/djw2016xxll/': 1574,
        'http://dangjian.com/djw2016sy/djw2016djlt/': 1575,
        'http://dangjian.com/djw2016sy/djw2016fwcl/': 1576,
        'http://dangjian.com/djw2016sy/djw2016dvgd/': 1577,
        'http://dangjian.com/djw2016sy/djw2016dsgs/': 1578,
        'http://dangjian.com/djw2016sy/djw2016whdg/': 1579,
        'http://dangjian.com/djw2016sy/djw2016gjgc/': 1580,
        'http://dangjian.com/djw2016sy/2016djwsyznlrw/': 1581,
        'http://dangjian.com/djw2016sy/djw2016wkztl/wkztl2016xihy/': 1582,
    }

    # http://dangjian.com/djw2016sy/djw2016syyw/201904/t20190415_5076589.shtml   http://dangjian.com/djw2016sy/djw2016gddj/201904/t20190415_5076642.shtml
    #  href="./201907/t20190717_5189426.shtml
    # http://dangjian.com/djw2016sy/djw2016wkztl/wkztl2016xihy/201907/t20190718_5191268.shtml
    rules = (
        Rule(LinkExtractor(allow=(r'dangjian.com/.*?/%s/t\d+_\d+.shtml'%datetime.today().strftime('%Y%m')), ),
                           callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'dangjian.com/.*?\d+.shtml'), deny=(r'/201[0-8]', r'/20190[1-9]/')),
             process_request=otherurl_meta, follow=False),
    )

    #http://dangjian.com/djw2016sy/djw2016gddj/201904/t20190415_5076642.shtml
    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="main"]/div[@class="inner"]/div[@class="main-left"]')[0]
            source_div = news_div.xpath('./div[@class="box"]')[0]
            content_div = news_div.xpath('.//*/div[@class="TRS_Editor"]')[0]

            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}')
            pubtime = time_re[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        title = ''.join(i.strip() for i in news_div.xpath('./div[@id="title_tex"]/text()').extract())
        origin_name = source_div.xpath('./div[@class="ly"]/span[@id="time_ly"]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
