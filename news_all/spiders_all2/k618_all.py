# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class K618AllSpider(NewsRCSpider):
    """未来网"""
    name = 'k618_all'
    mystart_urls = {

        'http://politics.k618.cn/rd/': 1923,
        'http://politics.k618.cn/yw/': 1924,
        'http://politics.k618.cn/sp/': 1925,
        'http://news.k618.cn/roll/': 1926,
        'http://edu.news.k618.cn/yc/': 1927,
        'http://college.k618.cn/gxdt/': 1928,
        'http://college.k618.cn/jxky/': 1929,
        'http://news.k618.cn/society/': 1930,
        'http://news.k618.cn/jhtj/': 1931,
        'http://news.k618.cn/world/': 1932,
        'http://news.k618.cn/travel/guonei/': 1933,
        'http://news.k618.cn/travel/world/': 1934,
        'http://news.k618.cn/travel/ltqw/': 1935,
        'http://tech.k618.cn/': 1936,
        'http://view.k618.cn/rmpl/': 1937,
        'http://edu.news.k618.cn/': 1938,
        'http://news.k618.cn/finance/': 1939,
        'http://news.k618.cn/finance/xjj/': 1940,
        'http://news.k618.cn/finance/hg/': 1941,
        'http://news.k618.cn/finance/money/': 1942,
        'http://news.k618.cn/finance/pl/': 1943,
        'http://news.k618.cn/finance/tscj/': 1944,
        'http://edu.k618.cn/zxzx/': 1945,
        'http://kids.k618.cn/jinrht/': 1946,
        'http://xiao.k618.cn/xwzt/': 1947
    }

    # http://news.k618.cn/shizheng/rd/201904/t20190415_17337753.html    http://news.k618.cn/shizheng/rd/201904/t20190415_17337716.html
    rules = (
        Rule(LinkExtractor(allow=(r'k618.cn/.*?/%s/td+_\d+.shtml'%datetime.today().strftime('%Y%m')),
                           deny=r'v.k618.cn/vlist/'),  # 排除视频
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'k618.cn/.*?\d+.html'), deny=(r'/201[0-8]', r'/20190[1-9]/', r'v.k618.cn/vlist/', r'index_\d+')),
             callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="news_conetnt"]/div[@class="news_content_left"]')[0]
            source_div = news_div.xpath('./div[@class="news_time_source"]')[0]
            # pubtime = source_div.xpath('./div[@class="ly"]/span[@id="time_tex"]/text()').extract_first('').strip()
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            cvs = xp('.//div[@class="news_main"]/div[@class="TRS_Editor"]') or xp('.//div[@class="news_main"]')
            content_div = cvs[0]
        except:
            return self.parse_item2(response)

        title = ''.join(i.strip() for i in news_div.xpath('./h1/text()').extract())
        origin_name = source_div.xpath('./span/text()').extract_first('').replace('来源:', '').strip()
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    #  http://edu.k618.cn/jnpx/201903/t20190314_17263164.html
    def parse_item2(self, response):
        
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="inn"]/div[@class="s3"]/div[@class="d nrP"]')[0]
            source_div = news_div.xpath('./div[@class="hd"]/p[@class="fcH"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = news_div.xpath('./div[@class="bd"]/div[@class="TRS_Editor"]')[0]
        except:
            return self.parse_item3(response)

        title = ''.join(i.strip() for i in news_div.xpath('.//*/h1/text()').extract())
        # origin_name = source_div.xpath('./span/text()').extract_first('').replace('来源:', '').strip()
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media
        )

    #  http://kids.k618.cn/jinrht/201904/t20190411_17328638.html
    def parse_item3(self, response):
        
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="nr"]/div[@class="lb-l"]/div[@class="lblnr"]')[0]
            source_div = news_div.xpath('./div[@class="yxzhzwtt01 text-666 fs12"]')[0]
            # pubtime = source_div.xpath('./div[@class="ly"]/span[@id="time_tex"]/text()').extract_first('').strip()
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = news_div.xpath('.//div[@class="TRS_Editor"]')[0]
        except:
            return self.parse_item4(response)
        
        title = ''.join(i.strip() for i in news_div.xpath('./div[@class="yxzhzwtt fm01 fs22 text-333"]/text()').extract())
        origin_name = source_div.xpath('./font[@id="source_baidu"]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://news.k618.cn/pic/yctp/201904/t20190403_17309593.html
    def parse_item4(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@id="replayBtn"]/div[@class="inn"]')[0]
            source_div = news_div.xpath('.//*/div[@class="fl"]/p[@class="p_info"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = news_div.xpath('./div[@class="s1"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        title = ''.join(i.strip() for i in news_div.xpath('.//*/h1/text()').extract())
        origin_name = source_div.xpath('./span[2]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )