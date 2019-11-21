# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class OceanolAllSpider(NewsRCSpider):
    """中国海洋在线"""
    name = 'oceanol_all'
    mystart_urls = {

        'http://www.oceanol.com/col11.html': 2053, 'http://www.oceanol.com/col12.html': 2054,
        'http://www.oceanol.com/fangzai/col484.html': 2055, 'http://www.oceanol.com/guoji/col520.html': 2056,
        'http://www.oceanol.com/jidi/col495.html': 2057, 'http://www.oceanol.com/jidi/col496.html': 2058,
        'http://www.oceanol.com/jidi/col498.html': 2059, 'http://www.oceanol.com/jingji/col39.html': 2060,
        'http://www.oceanol.com/jingji/col40.html': 2061, 'http://www.oceanol.com/jingji/col41.html': 2062,
        'http://www.oceanol.com/jingji/col42.html': 2063, 'http://www.oceanol.com/jingji/col44.html': 2064,
        'http://www.oceanol.com/jingji/col46.html': 2065, 'http://www.oceanol.com/keji/col516.html': 2066,
        'http://www.oceanol.com/wenhua/col83.html': 2067, 'http://www.oceanol.com/zhifa/col64.html': 2068

    }

    # http://www.oceanol.com/content/201904/16/c86335.html
    rules = (
        Rule(LinkExtractor(allow=(r'oceanol.com/content/%s.*?\d+.html'%datetime.today().year), ),
                           callback='parse_item', follow=False),
    )
    
    def parse_item(self, response):
        # http://www.oceanol.com/content/201904/16/c86335.html
        
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="main-content"]')[0]
            source_div = news_div.xpath('./div[@class="main-content-box1"]')[0]
            content_div = news_div.xpath('./div[@class="main-content-box2"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}')
            pubtime = time_re[0] if time_re else ''
        except:
            return self.produce_debugitem(response, "xpath error")

        title = ''.join(i.strip() for i in news_div.xpath('./h1/text()').extract())
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media
        )
