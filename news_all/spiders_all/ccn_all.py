# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class CnnSpider(NewsRCSpider):
    """中国消费网"""
    name = 'cnn_all'
    mystart_urls = {
        'http://www.ccn.com.cn/html/diaocha/': 2006, 'http://www.ccn.com.cn/html/fazhijujiao/': 2007,
        'http://www.ccn.com.cn/html/news/xiaofeiyaowen/': 2008,
        'http://www.ccn.com.cn/html/shishangshenghuo/jiankang/': 2009,
        'http://www.ccn.com.cn/html/shishangshenghuo/licai/': 2010,
        'http://www.ccn.com.cn/html/xiaofeipinglun/': 2011
    }

    #  http://www.ccn.com.cn/html/news/xiaofeiyaowen/2019/0415/449323.html
    #  http://www.ccn.com.cn/html/news/xiaofeiyaowen/2019/0412/449067.html

    rules = (
        Rule(LinkExtractor(allow=(r'ccn.com.cn/.*?/%s\d{2}/\d+.html'%datetime.today().strftime('%Y/%m')), ),
                           callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'ccn.com.cn/.*?\w+.html',  deny=(r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/', r'list_\d'),
                           ),
             process_request=otherurl_meta,
             follow=False),
    )

    # http://news.cpd.com.cn/n3559/201904/t20190415_835839.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            source_div = xp('.//p[@class="fz12 z6 mt5"]')[0]
            content_div = xp('.//div[@class="ov btm content"]')[0]
            # pubtime = source_div.xpath('./div[@class="ly"]/span[@id="time_tex"]/text()').extract_first('').strip()
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            title = ''.join(i.strip() for i in response.xpath('.//h2/text()').extract())
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
