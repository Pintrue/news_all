# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class TaiWanAllSpider(NewsRCSpider):
    """中国台湾网"""
    name = 'taiwan_all'
    mystart_urls = {
        'http://www.taiwan.cn/taiwan/today/': 1537,
        'http://www.taiwan.cn/taiwan/pu/': 1538,
        'http://www.taiwan.cn/taiwan/jsxw/': 1539,
        'http://www.taiwan.cn/plzhx/hxshp/': 1540,
        'http://www.taiwan.cn/plzhx/zhjzhl/zhjlw/': 1541,
        'http://www.taiwan.cn/plzhx/xxhla/': 1542,
        'http://www.taiwan.cn/plzhx/dlgc/': 1543,
        'http://www.taiwan.cn/plzhx/wyrt/': 1544,
        'http://www.taiwan.cn/plzhx/plyzl/': 1545,
        'http://www.taiwan.cn/lilunpindao/': 1546,
        'http://www.taiwan.cn/xwzx/la/': 1547,
        'http://y.taiwan.cn/newsqw/list.shtml': 1548,
        'http://www.taiwan.cn/31t/zxxx/': 1549,
        'http://www.taiwan.cn/31t/wh31/': 1550,
        'http://www.taiwan.cn/31t/jm31/': 1551,
        'http://www.taiwan.cn/31t/jy31/': 1552,
        'http://www.taiwan.cn/31t/qx31/': 1553,
        'http://www.taiwan.cn/31t/cy/': 1554,
        'http://www.taiwan.cn/31t/zgrz31/': 1555,
        'http://www.taiwan.cn/31t/zcfb/': 1556,
        'http://www.taiwan.cn/31t/zcjd31/': 1557,
        'http://www.taiwan.cn/31t/ys31/': 1558,
        'http://www.taiwan.cn/xwzx/': 1559,
        'http://econ.taiwan.cn/': 1560,
        'http://taishang.taiwan.cn/tszx/': 1561,
        'http://culture.taiwan.cn/': 1562,
        'http://travel.taiwan.cn/': 1563,
        'http://www.taiwan.cn/local/dfkx/': 1564,
        'http://depts.taiwan.cn/news/': 1565,
    }

    #http://www.taiwan.cn/taiwan/today/201902/t20190228_12143123.htm

    rules = (
        Rule(LinkExtractor(allow=(r'taiwan.cn/.*?/%s.*?\d+.htm'%datetime.today().year), ),
                           callback='parse_item', follow=False),
    )

    #http://www.taiwan.cn/taiwan/today/201902/t20190228_12143123.htm
    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@id="main"]')[0]
            source_div = news_div.xpath('.//div[@id="infoAFun"]')[0]
            content_div = news_div.xpath('./div[@id="contentArea"]/div[@class="TRS_Editor"]')[0]
            pubtime = source_div.xpath('./div[1]/span[1]/text()').extract_first('').strip()
        except:
            return self.parse_item2(response)

        title = ''.join(i.strip() for i in news_div.xpath('./h1/text()').extract())
        origin_name = source_div.xpath('./div[1]/span[2]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item2(self, response):
        # http://y.taiwan.cn/newsqw/2019/0410/9942164.html
        xp = response.xpath
        try:
            news_div = xp('.//div[@id="mainContent"]')[0]
            source_div = news_div.xpath('./div[@class="titleAndPanel"]')[0]
            content_div = news_div.xpath('./div[@class="leftS"]/div[@class="contentArea"]/div[@class="TRS_Editor"]')[0]
            time_re = source_div.re(r'\d{2,4}年\d{1,2}月\d{1,2}日\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            title = ''.join(i.strip() for i in news_div.xpath('./h1/text()').extract())
            origin_name = source_div.xpath('./p/span/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div)
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
