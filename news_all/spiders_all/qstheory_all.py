# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider
from datetime import datetime


class QstheorySpipder(NewsRCSpider):
    name = 'qstheory_all'

    # 求是网
    mystart_urls = {
            'http://www.qstheory.cn/economy/jjgc.htm': 2673,   #  经济观察
            'http://www.qstheory.cn/zt2019/llxjj/index.htm': 2641,   #
            'http://www.qstheory.cn/qslgxd/index.htm': 2642,   #  原创
            'http://www.qstheory.cn/defense/index.htm': 2643,   #  国防
            'http://www.qstheory.cn/science/index.htm': 2644,   #  科教
            'http://www.qstheory.cn/international/index.htm': 2645,   #  国际
            'http://www.qstheory.cn/zoology/index.htm': 2647,   #  生态
            'http://www.qstheory.cn/qszq/llqk/index.htm': 2649,   #
            'http://www.qstheory.cn/society/index.htm': 2650,   #  社会
            'http://www.qstheory.cn/economy/index.htm': 2651,   #  经济
            'http://www.qstheory.cn/qszq/llwx/index.htm': 2659,   #  理论文选
            'http://www.qstheory.cn/qsyw/index.htm': 2660,   #  资讯
            'http://www.qstheory.cn/qswp.htm': 2662,   #  网评
            'http://www.qstheory.cn/books/rdsp.htm': 2664,   #  热点书评
            'http://www.qstheory.cn/zoology/nyzy.htm': 2667,   #  能源资源
            'http://www.qstheory.cn/zoology/stwm.htm': 2668,   #  生态文明
            'http://www.qstheory.cn/science/jysd.htm': 2669,   #  教育视点
            'http://www.qstheory.cn/science/kjgc.htm': 2670,   #  科技观察
            'http://www.qstheory.cn/economy/xrsd.htm': 2672,   #  新锐视点
            'http://www.qstheory.cn/economy/ggfz.htm': 2674,   #  改革发展
            'http://www.qstheory.cn/economy/hqsy.htm': 2675,   #  环球视野
            'http://www.qstheory.cn/economy/jj_fazhan.htm': 2677,   #  改革发展
            'http://www.qstheory.cn/books/ts_zhongdian.htm': 2682,   #  重点图书
    }

    # http://www.qstheory.cn/llwx/2019-03/25/c_1124276847.htm   http://www.qstheory.cn/zoology/2019-03/21/c_1124264538.htm
    rules = (Rule(LinkExtractor(allow=r'qstheory.cn/.*?/%s.*?/c_\d+.htm'%datetime.today().year,  #restrict_xpaths="//div[@class='column mar-t-10'][2]"   之前有的  线上最新的3.14
                                ),
                  callback='parse_item', follow=False),
             )

    # http://www.qstheory.cn/zoology/2019-03/21/c_1124264538.htm
    def parse_item(self, response):
        try:
            head_div = response.xpath('.//div[@class="headtitle"]')[0]
            content_div = response.xpath('.//div[@class="content"]/div[@class="highlight"]')[0]
            pubtime = head_div.xpath('.//span/text()').extract_first('').strip()
            title = ''.join(i.strip() for i in head_div.xpath('.//h1/text()').extract())
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.parse_item2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media
        )

    # http://www.qstheory.cn/yaowen/2019-01/02/c_1123937637.htm
    def parse_item2(self, response):
        try:
            news_div = response.xpath('.//div[@class="content"]/div[@class="inner"]')[0]
            content_div = response.xpath('.//div[@class="text"]/div[@class="clipboard_text"]/div[@class="highlight"]')[0]
            pubtime = news_div.xpath('.//span[@class="pubtime"]/text()').extract_first('').strip()
            title = ''.join(i.strip() for i in news_div.xpath('.//h1/text()').extract())
            origin_name = news_div.xpath('./span[@class="appellation"]/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.parse_item3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

        # http://www.qstheory.cn/wp/2019-03/14/c_1124235349.htm
    def parse_item3(self, response):
        try:
            news_div = response.xpath('.//div[@class="content"]/div[@class="inner"]')[0]
            head_div = news_div.xpath('.//span[@class="pubtime"]')[0]
            time_re = head_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = response.xpath('.//div[@class="text"]/p')
            title = ''.join(i.strip() for i in news_div.xpath('.//h1/text()').extract())
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media
        )