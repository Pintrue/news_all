# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Cnipagov_allSpider(NewsRCSpider):
    """中央人民政府&国家知识产权局"""
    name = 'zyrmzf'
    mystart_urls = {
        'http://www.gov.cn/guowuyuan/xinwen.htm': 7628,  # 中华人们共和国中央人民政府
        'http://www.gov.cn/xinwen/yaowen.htm': 7629,  # 中华人们共和国中央人民政府
        'http://www.cnipa.gov.cn/szywn/index.htm': 7640,  # 国家知识产权局
        'http://www.gov.cn/xinwen/gundong.htm': 7641,  # 中华人民共和国中央人民政府
    }
    rules = (
        # http://www.gov.cn/xinwen/2019-06/25/content_5402999.htm
        # http://www.gov.cn/xinwen/2019-06/26/content_5403411.htm
        # http://www.gov.cn/xinwen/2019-06/25/content_5403066.htm
        
        Rule(LinkExtractor(allow=(r'gov.cn/xinwen.*?/\d{2}/content_\d+.htm'),
                           ), callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='article oneColumn pub_border']/h1/text()").extract_first()
            source = xp("//div[@class='pages-date']")[0]
            content_div = xp("//div[@id='UCAP-CONTENT']")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//span[@class='font']/text()").extract_first('')
            content, media, _, _ = self.content_clean(content_div)
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
