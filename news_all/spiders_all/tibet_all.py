# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class TaiWanAllSpider(NewsRCSpider):
    """中国西藏网"""
    name = 'tibet_all'
    # mystart_urls = {
    #     'http://www.tibet.cn/cn/politics/': 1566,
    #     'http://www.tibet.cn/cn/medicine/jbzl/': 1567,
    #     'http://www.tibet.cn/cn/medicine/sjys/': 1568,
    #     'http://www.tibet.cn/cn/theory/news/': 1569,
    #     'http://www.tibet.cn/cn/rediscovery/': 1570,
    #     'http://www.tibet.cn/cn/tech/': 1571,
    #     'http://www.tibet.cn/cn/book/': 1572,
    # }

    mystart_urls = {
        'http://www.tibet.cn/': 1,
        'http://www.tibet.cn/cn/news/yc/': 2,
        'http://www.tibet.cn/cn/news/zx/': 3,
        'http://www.tibet.cn/cn/news/zcdt/': 4,
        'http://www.tibet.cn/cn/politics/': 5,
        'http://www.tibet.cn/cn/bwsp/': 6,
        'http://www.tibet.cn/cn/culture/ms/': 7,
        'http://www.tibet.cn/cn/culture/gy/': 8,
        'http://www.tibet.cn/cn/culture/zx/': 9,
        'http://www.tibet.cn/cn/culture/wx/': 10,
        'http://www.tibet.cn/cn/aid_tibet/news/': 11,
        'http://www.tibet.cn/cn/aid_tibet/rw/': 12,
        'http://www.tibet.cn/cn/travel/': 13,
        'http://www.tibet.cn/cn/medicine/news/': 14,
        'http://www.tibet.cn/cn/medicine/jbzl/': 15,
        'http://www.tibet.cn/cn/medicine/sjys/': 16,
        'http://www.tibet.cn/cn/theory/zjcs/': 17,
        'http://www.tibet.cn/cn/theory/news/': 18,
        'http://www.tibet.cn/cn/rediscovery/': 19,
        'http://www.tibet.cn/cn/religion/': 20,
        'http://media.tibet.cn/photo/news/list.shtml': 21,
        'http://media.tibet.cn/photo/landscape/list.shtml': 22,
        'http://media.tibet.cn/photo/custom/list.shtml': 23,
        'http://media.tibet.cn/photo/special/list.shtml': 24,
        'http://www.tibet.cn/cn/tech/': 25,
        'http://www.tibet.cn/cn/book/': 26,
        'http://www.tibet.cn/cn/vg/': 27,
        'http://www.tibet.cn/cn/data/': 28,
        'http://www.tibet.cn/cn/edu/': 29,
        'http://www.tibet.cn/cn/ecology/': 30,
        'http://www.tibet.cn/cn/fp/': 31,
        'http://www.tibet.cn/cn/network/dt/': 32,
        'http://www.tibet.cn/cn/cloud/xszypk/a/': 33,
        'http://www.tibet.cn/cn/cloud/xszypk/b/': 34,
        'http://www.tibet.cn/cn/cloud/xszypk/c/': 35,
        'http://www.tibet.cn/cn/cloud/xszypk/d/': 36,
        'http://www.tibet.cn/cn/cloud/xszypk/e/': 37,
    }

    # http://www.tibet.cn/cn/news/yc/201904/t20190410_6550585.html

    rules = (
        Rule(LinkExtractor(allow=(r'tibet.cn/.*?/%s.*?\d+.html'%datetime.today().year), ),
                           callback='parse_item', follow=False),

    )

    # http://www.tibet.cn/cn/news/yc/201904/t20190410_6550585.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="content"]')[0]
            source_div = news_div.xpath('./div[@class="title_box"]/div[@class="info"]')[0]
            content_div = news_div.xpath('./div[@class="left"]/div[@id="text"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
        except:
            return self.produce_debugitem(response, "xpath error")



        title = ''.join(i.strip() for i in news_div.xpath('./div[@class="title_box"]/h2/text()').extract())
        origin_name = source_div.xpath('./div[@class="title_box"]/div[@class="info"]/span[3]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div,kill_xpaths=["//div[@class='content_banquan']"])

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
