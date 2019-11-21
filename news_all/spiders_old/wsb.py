# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class WsbSpider(NewsRCSpider):
    '''卫生部网站'''
    # http://www.gov.cn/zhengce/content/2019-06/04/content_5397350.htm
    # 此类型网站未解析
    name = 'wsb'
    mystart_urls = {
        # 'http://www.moh.gov.cn/zhuz/mtbd/list.shtml': 1301508,  # 卫生部网站 媒体报道
        # 'http://www.moh.gov.cn/zhuz/xwfb/list.shtml': 1301258,  # 卫生部网站-新闻发布
        'http://www.gov.cn/pushinfo/v150203/index.htm': 1301256,  # 卫生部网站-时政要闻
        # 'http://www.moh.gov.cn/zhuz/ldzs/list.shtml': 1301257,  # 卫生部网站-领导之声
    }
    rules = (
        # http://www.gov.cn/zhengce/content/2019-06/19/content_5401568.htm
        # http://www.gov.cn/premier/2019-06/17/content_5400996.htm
        Rule(LinkExtractor(allow=(r'gov.cn/.*?/\d{4}-\d{2}/\d{2}/content_\d+\.htm',),
                           ), callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//div[@class="article oneColumn pub_border"]/h1/text()').extract_first().strip()
            content_div = xp('//div[@id="UCAP-CONTENT"]')[0]

            pubtime = xp('//div[@class="pages-date"]/text()').extract_first().strip()

            
            
            origin_name = xp('//div[@class="pages-date"]/span/text()').extract_first()

        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )
