# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class CcoalnewsAllSpider(NewsRCSpider):
    """中国煤炭网"""
    name = 'ccoalnews_all'
    mystart_urls = {
        
        'http://www.ccoalnews.com/dujia.html': 2012,
        'http://www.ccoalnews.com/jingji.html': 2013,
        # 'http://www.ccoalnews.com/news/qiye.html': 2014,  # 4月30日说暂停抓取
        'http://www.ccoalnews.com/news/yaowen.html': 2015, 'http://www.ccoalnews.com/zhengce.html': 2016,
        
    }
    
    # http://www.ccoalnews.com/news/201904/15/c103916.html
    #  http://www.ccoalnews.com/201905/10/c105787.html
    rules = (
        Rule(LinkExtractor(allow=(r'ccoalnews.com.*?/%s/\d{2}/c\d+.html' % datetime.today().strftime('%Y%m')), ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'ccoalnews.com/.*?\w+.html', deny=(r'/201[0-8]', r'/2019/0[1-9]', r'/2019/0[1-9]'),
                           ),
             process_request=otherurl_meta,
             follow=False),
    )
    
    # http://www.ccoalnews.com/news/201904/15/c103916.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="text-article"]')[0]
            source_div = news_div.xpath('./div[@class="article-details"]')[0]
            content_div = news_div.xpath('./div[@class="content"]')[0]
            # pubtime = source_div.xpath('./div[@class="ly"]/span[@id="time_tex"]/text()').extract_first('').strip()
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
            
            
        except:
            return self.produce_debugitem(response, "xpath error")
        

        
        title = ''.join(i.strip() for i in news_div.xpath('.//h1/text()').extract())
        origin_name = source_div.xpath('./span[@class="source"]/text()').extract_first('').strip()
        content, media, videos, video_cover = self.content_clean(content_div,
                                                                 kill_xpaths=["//div[@class='content']//span",
                                                                              "//div[@class='content']/div[@class='share']"])
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media
        )
