# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider, otherurl_meta


class CacAllSpider(NewsRCSpider):
    """中国网信网"""
    name = 'cac_all'
    mystart_urls = {
        'http://www.cac.gov.cn/xgbm.htm': 2147,
     'http://www.cac.gov.cn/xgbmfb.htm': 2148, 'http://www.cac.gov.cn/bgsfb.htm': 2149,
     'http://www.cac.gov.cn/wlcb.htm': 2150, 'http://www.cac.gov.cn/cbgz.htm': 2153,
     'http://www.cac.gov.cn/wsznl.htm': 2154, 'http://www.cac.gov.cn/gjjl.htm': 2165,
     'http://www.cac.gov.cn/hzjl.htm': 2170, 'http://www.cac.gov.cn/yjdt.htm': 2173,
     'http://www.cac.gov.cn/wlfz.htm': 2187, 'http://www.cac.gov.cn/gjkj.htm': 2194,
     'http://www.cac.gov.cn/jscx.htm': 2196, 'http://www.cac.gov.cn/wlqy.htm': 2197,
     'http://www.cac.gov.cn/yjdsj.htm': 2198, 'http://www.cac.gov.cn/llyqsy.htm': 2204,
     'http://www.cac.gov.cn/ll.htm': 2205, 'http://www.cac.gov.cn/sy.htm': 2206,
    }
    # http://www.cac.gov.cn/2019-04/13/c_1124362642.htm
    # http://www.cac.gov.cn/2019-04/15/c_1124366390.htm
    rules = (
        Rule(LinkExtractor(
            allow=r'cac.gov.cn/%s/\d{2}/c_\d{8,}.htm'%datetime.today().strftime('%Y-%m'),
                           ),
             callback='parse_item',follow=False),
        Rule(LinkExtractor(
            allow=r'cac.gov.cn.*?\w{8,}.htm', deny=(r'/201[0-8]', r'/2019-0[1-9]')
        ),
            process_request=otherurl_meta, follow=False),
    )

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp(r'//h1[@id="title"]/text()').extract_first('') or self.get_page_title(response).split('_')[0]
            pubtime = xp('//div[@class="info"]/*[@id="pubtime"]/text()')[0].extract().strip()
            
            

            cv = xp('//div[@id="content"]')[0]
            content, media, video, cover = self.content_clean(cv)
            origin_name = xp('//div[@class="info"]/*[@id="source"]/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )
