# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class AqscAllSpider(NewsRCSpider):
    """中国安全生产网"""
    name = 'aqsc_all'
    mystart_urls = {
        'http://www.aqsc.cn/chanye/index.html': 2000, 'http://www.aqsc.cn/news/ataw.html': 2001,
        'http://www.aqsc.cn/news/shizheng.html': 2002, 'http://www.aqsc.cn/news/zonghe.html': 2003,
        'http://www.aqsc.cn/pinglun/yuanchuang.html': 2004, 'http://www.aqsc.cn/qiye/guanli.html': 2005,
        'http://www.aqsc.cn/news/yujing.html': 2073,
        
        # 老爬虫的
        'http://www.aqsc.cn/yaowen.html': 1301585,  # 中国安全生产报-首页-今日要闻-左侧列表
    }

    # http://www.aqsc.cn/news/201903/01/c100702.html

    rules = (
        Rule(LinkExtractor(allow=(r'aqsc.cn.*?/%s/\d{2}/c\d+.html' % datetime.today().strftime('%Y%m')), ),
                           callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'aqsc.cn.*?\w+.html'), deny=(r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/')),
                           process_request=otherurl_meta, follow=False),
    )
   
    # http://www.aqsc.cn/news/201903/01/c100702.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            source_div = xp('.//div[@class="article-details"]')[0]
            content_div = xp('.//div[@class="conbox mb30"]/p').extract()
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
        except:
            return self.parse_item2(response)
        
        origin_name = source_div.xpath('./div[@class="article-details"]/span[@class="source"]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('_')[0],
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media
        )

    def parse_item2(self, response):
        # http://www.aqsc.cn/wpy/201903/29/c103026.html
        
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="container"]')[0]
            source_div = news_div.xpath('.//table//div[1]')[0]
            content_div = news_div.xpath('.//table//div[3]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('_')[0],
            pubtime=pubtime,
            content=content,
            media=media
        )