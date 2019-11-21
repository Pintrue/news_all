# -*- coding: utf-8 -*-
from datetime import datetime
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class JwviewSpider(NewsRCSpider):
    """中新经纬"""
    name = 'jwview'
    mystart_urls = {'http://www.jwview.com/hg.html': 196,  # '宏观',
                  'http://www.jwview.com/jr.html': 197,  # '金融',
                  'http://www.jwview.com/zq.html': 198,  # '股市',

                    # 来自spiders_all
                    'http://www.jwview.com/34/2017/0831/18.html': 655,  # 中新经纬-杨德龙
                    'http://www.jwview.com/34/2017/0913/16.html': 656,  # 中新经纬-董希淼
                    'http://www.jwview.com/html/34/2018/1213/43.html': 657,  # 中新经纬-点石成金
                    'http://www.jwview.com/html/34/2019/0307/47.html': 658,  # 中新经纬-明明
                    'http://www.jwview.com/34/2017/0918/30.html': 659,  # 中新经纬-李大霄
                    'http://www.jwview.com/html/34/2019/0307/45.html': 660,  # 中新经纬-万喆
                    'http://www.jwview.com/html/34/2019/0226/44.html': 661,  # 中新经纬-华商影响力
                    'http://www.jwview.com/html/34/2017/1212/13.html': 662,  # 中新经纬-盛松成
                    'http://www.jwview.com/html/34/2019/0314/48.html': 663,  # 中新经纬-管涛
                    'http://www.jwview.com/renwen.html': 666,  # 中新经纬-人文
                    'http://www.jwview.com/wc.html': 668,  # 中新经纬-外参
                    'http://www.jwview.com/rw.html': 669,  # 中新经纬-财人
                    'http://www.jwview.com/jwmj.html': 670,  # 中新经纬-专栏
                    'http://www.jwview.com/': 671,  # 中新经纬-精英的财经资讯
                    'http://www.jwview.com/lc.html': 672,  # 中新经纬-理财
                    'http://www.jwview.com/sj.html': 673,  # 中新经纬-视界
                    'http://www.jwview.com/kj.html': 674,  # 中新经纬-科技
                    'http://www.jwview.com/qc.html': 675,  # 中新经纬-汽车
                    'http://www.jwview.com/znh.html': 676,  # 中新经纬-高层
                    'http://www.jwview.com/original.html': 677,  # 中新经纬-原创
                    'http://www.jwview.com/fc.html': 678,  # 中新经纬-房产
                    'http://www.jwview.com/sc.html': 679,  # 中新经纬-产经
                    'http://www.jwview.com/ztlm/37/2019/0218/270.html': 682,  # 中新经纬-深度解读
                    'http://www.jwview.com/ztlm/37/2019/0218/269.html': 683,  # 中新经纬-热点聚焦
                    }
    # http://www.jwview.com/jingwei/html/01-20/209084.shtml
    rules = (
        Rule(LinkExtractor(allow=(r'jwview\.com/jingwei/.*?/%s-\d{2}/\d+\.shtml'%datetime.today().strftime('%m'),),
                           deny=r'jingwei/zb/'),  # 排除直播
                  callback='parse_item', follow=False),
             )
             
    def parse_item(self, response):
        try:
            news_div = response.xpath('.//div[contains(@class,"contentleft")]/div[contains(@class,"content_zw")]')[0]
            head_div = news_div.xpath('./div[@class="title"]')[0]
            # content_divs = news_div.xpath('.//*[not(contains(@class,"title" or "time"))]')  # 由多个标签构成正文
            border_divs = response.xpath('.//div[@class="info borderee"]')
            source_text = head_div.xpath('./div[@class="time"]/text()').extract_first('').strip()
            pubtime = re.search(r'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}\:\d{1,2})', source_text).group(1)
        except:
            return self.parse_item_2(response)
        title = ''.join(i.strip() for i in head_div.xpath('./h1/text()').extract())
        origin_name = source_text.replace(pubtime, '').strip()

        content_text = news_div.extract().replace(head_div.extract(), "")
        for i in border_divs:
            content_text = content_text.replace(i.extract(), "")
        content, media, videos, video_cover = self.content_clean(content_text)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_2(self, response):
        # article http://www.jwview.com/jingwei/01-18/208965.shtml
        try:
            head_div = response.xpath('.//header')[0]
            content_div = response.xpath('.//article')[0]
            pubtime = head_div.xpath('./div/time/em/text()')[0].extract().strip()
        except:
            return self.produce_debugitem(response, "xpath error")

        title = ''.join(i.strip() for i in head_div.xpath('./h1/text()').extract())
        origin_name = head_div.xpath('./div/time/p/text()').extract_first('').strip()
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
