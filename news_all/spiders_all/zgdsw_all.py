# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class ZgdswAllSpider(NewsRCSpider):
    """中国共产党历史网"""
    name = 'zgdsw_all'
    mystart_urls = {
        'http://www.zgdsw.org.cn/GB/219002/index.html': 2069,
        'http://www.zgdsw.org.cn/GB/244522/index.html': 2070,
        'http://www.zgdsw.org.cn/GB/244523/index.html': 2071,
        'http://www.zgdsw.org.cn/GB/349473/index.html': 2072
    }

    # http://www.zgdsw.org.cn/n1/2019/0416/c422509-31032473.html

    rules = (
        Rule(LinkExtractor(allow=(r'zgdsw.org.cn/.*?/%s.*?\d+.html'%datetime.today().year), ),
        # Rule(LinkExtractor(allow=(r'zgdsw.org.cn/.*?/%s.*?\d+.html' % datetime.today().year), ),
    )
             )
    
    # http://www.zgdsw.org.cn/n1/2019/0416/c422509-31032473.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="p2_right wb_right fr"]')[0]
            source_div = news_div.xpath('./h5[@class="one"]')[0]
            content_div = news_div.xpath('./p').extract()
            # pubtime = source_div.xpath('./div[@class="ly"]/span[@id="time_tex"]/text()').extract_first('').strip()
            time_re = source_div.re(r'\d{2,4}年\d{1,2}月\d{1,2}日\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
        except:
            return self.parse_item2(response)

        title = ''.join(i.strip() for i in news_div.xpath('./h1/text()').extract())
        origin_name = source_div.xpath('./a/text()').extract_first('').strip()
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
        # http://www.zgdsw.org.cn/n1/2019/0108/c244522-30509725.html
        
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="fr"]')[0]
            source_div = news_div.xpath('./p[@class="orgin"]')[0]
            content_div = news_div.xpath('./div[@class="box_con"]')[0]
            # pubtime = source_div.xpath('./div[@class="ly"]/span[@id="time_tex"]/text()').extract_first('').strip()
            time_re = source_div.re(r'\d{2,4}年\d{1,2}月\d{1,2}日\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
        except:
            return self.produce_debugitem(response, "xpath error")

        title = ''.join(i.strip() for i in news_div.xpath('./h1/text()').extract())
        origin_name = source_div.xpath('./a/text()').extract_first('').strip()
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
