#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/1
# @Author  : wjq


from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from copy import deepcopy
from news_all.spider_models import NewsRCSpider, otherurl_meta


class CfejAllSpider(NewsRCSpider):
    """中国环境新闻网"""
    name = 'cfej_all'
    
    mystart_urls = {
        'http://www.cfej.net/about/rd/': 202,  # 1054,
        'http://www.cfej.net/fcl/': 224,  # 1055,
        'http://www.cfej.net/hbrw/': 155,  # 1059,
        'http://www.cfej.net/bwzl/jxdt/': 157,  # 1060,
        'http://www.cfej.net/rdsl/': 179,  # 1061,
        'http://www.cfej.net/lvse/hqy/': 180,  # 1062,
        'http://www.cfej.net/jizhe/jzsl/': 181,  # 1063,
        'http://www.cfej.net/hbyq/yqjc/': 184,  # 1064,
        'http://www.cfej.net/news/sp/': 185,  # 1065,
        # 'http://hunan.cfej.net/hbyq/': 1067, 'http://hunan.cfej.net/guonei/': 1068   # 删除 不更新
    }
    
    rules = (
        # http://www.cfej.net/about/rd/201904/t20190403_698371.shtml
        # http://www.cfej.net/fcl/201903/t20190315_695998.shtml
        Rule(LinkExtractor(allow=(r'cfej.net.*?/%s/t\d{8}_\d{5,}.shtml' % datetime.today().strftime('%Y%m'),),
                           ),
             callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=(r'cfej.net.*?\w{5,}.s?htm',), deny=(r'/201[0-8]', r'/2019/0[1-9]')
                           ),
             process_request=otherurl_meta, follow=False),
    )
    
    custom_settings = {
        # 'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            content_div = xp('.//div[@class="article"]/div[(@class="text")]')[0]
            source_div = xp('.//div[@class="fushu"]')[0]
            pubtime = source_div.xpath('./span[1]/text()')[0].extract().strip()
            origin_name = source_div.xpath('./span[2]/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")
        

            
        title = xp('.//h1/text()').extract_first('') or self.get_page_title(response).split('_')[0]
        content, media, videos, video_cover = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )
