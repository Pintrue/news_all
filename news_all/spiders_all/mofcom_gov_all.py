# -*- coding: utf-8 -*-

from datetime import datetime
import execjs
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class MofcomAllSpider(NewsRCSpider):
    """商务部网站"""
    name = 'mofcom_gov_all'
    mystart_urls = {
        'http://www.mofcom.gov.cn/article/ae/ldhd/': 2090, 'http://www.mofcom.gov.cn/article/ae/ai/': 2091,
        'http://www.mofcom.gov.cn/article/ae/sjjd/': 2092, 'http://www.mofcom.gov.cn/article/b/c/': 2093,
        'http://www.mofcom.gov.cn/article/b/fwzl/': 2094, 'http://www.mofcom.gov.cn/article/b/d/': 2095,
        'http://www.mofcom.gov.cn/article/b/e/': 2096, 'http://www.mofcom.gov.cn/article/b/f/': 2097,
        'http://www.mofcom.gov.cn/article/b/xxfb/': 2098, 'http://www.mofcom.gov.cn/article/h/redht/': 2099,
        'http://www.mofcom.gov.cn/article/h/jinckxx/': 2100, 'http://www.mofcom.gov.cn/article/h/xinxidongtai/': 2101,
        'http://www.mofcom.gov.cn/article/h/zongzhi/': 2102, 'http://www.mofcom.gov.cn/article/jiguanzx/': 2103,
        'http://www.mofcom.gov.cn/article/resume/responsibily/': 2104,
        'http://www.mofcom.gov.cn/article/resume/dybg/': 2105, 'http://www.mofcom.gov.cn/article/i/jyjl/j/': 2106,
        'http://www.mofcom.gov.cn/article/i/jyjl/k/': 2107, 'http://www.mofcom.gov.cn/article/i/jyjl/e/': 2108,
        'http://www.mofcom.gov.cn/article/i/jyjl/m/': 2109, 'http://www.mofcom.gov.cn/article/i/jyjl/l/': 2110,
        'http://www.mofcom.gov.cn/article/i/jshz/new/': 2111, 'http://www.mofcom.gov.cn/article/i/jshz/rlzykf/': 2112,
        'http://www.mofcom.gov.cn/article/i/jshz/zn/': 2113, 'http://www.mofcom.gov.cn/article/i/jshz/xm/': 2114,
        'http://www.mofcom.gov.cn/article/i/dxfw/cj/': 2115, 'http://www.mofcom.gov.cn/article/i/dxfw/gzzd/': 2116,
        'http://www.mofcom.gov.cn/article/i/dxfw/ae/': 2117, 'http://www.mofcom.gov.cn/article/i/dxfw/jlyd/': 2118,
        'http://www.mofcom.gov.cn/article/i/dxfw/nbgz/': 2119, 'http://www.mofcom.gov.cn/article/shangwubangzhu/': 2120,
        'http://www.mofcom.gov.cn/article/huiyuan/': 2121, 'http://www.mofcom.gov.cn/article/ztxx/xmlh/xmg/': 2122,
        'http://www.mofcom.gov.cn/article/ztxx/xmlh/xmf/': 2123, 'http://www.mofcom.gov.cn/article/ztxx/gwyxx/': 2124,
        'http://www.mofcom.gov.cn/article/zhengcejd/bj/': 2125, 'http://www.mofcom.gov.cn/article/zhengcejd/bl/': 2126,
    }
    # http://www.mofcom.gov.cn/article/jiguanzx/201904/20190402851412.shtml
    # http://www.mofcom.gov.cn/article/difang/201904/20190402851711.shtml
    # http://www.mofcom.gov.cn/article/ae/ai/201904/20190402850224.shtml
    rules = (
        Rule(LinkExtractor(allow=r'mofcom.gov.cn/article/.*?/%s/\d{8,}.shtml' % datetime.today().strftime('%Y%m'),
                           ),
             callback='parse_item',
             follow=False),
    )

    from scrapy.conf import settings
    from copy import deepcopy
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    def parse_item(self, response):
        xp = response.xpath
        try:
            js1 = xp('/html/body/script[1]/text()').extract_first('')
            if not js1:
                return self.produce_debugitem(response, "xpath error")

            ect1 = execjs.compile(js1)
            title = ect1.eval('atitle') or xp('//h1/text()')[0].extract().strip()
            origin_name = ect1.eval('source')
            pubtime = ect1.eval('tm')

            cv = xp('//div[@id="zoom" or @class="artCon"]')[0]
            content, media, video, cover = self.content_clean(cv)

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