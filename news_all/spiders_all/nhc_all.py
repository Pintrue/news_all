# -*- coding: utf-8 -*-

import re
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class NhcAllSpider(NewsRCSpider):
    """卫生部网站"""
    name = 'nhc_all'
    mystart_urls = {
        'http://www.nhc.gov.cn/wjw/xwdt/list.shtml': 2085,
     'http://www.nhc.gov.cn/wjw/mtbd/list.shtml': 2086, 'http://www.nhc.gov.cn/wjw/gfxwjj/list.shtml': 2087,
     'http://www.nhc.gov.cn/wjw/zcjd/list.shtml': 2088, 'http://www.nhc.gov.cn/wjw/rdts/list.shtml': 2089,
    }
    # http://www.nhc.gov.cn/yjb/s7860/201904/f4841378e85c41f39ffa2911aaa5bb02.shtml
    rules = (
        Rule(LinkExtractor(allow=r'nhc.gov.cn.*?/%s/\w{6,}.shtml'%datetime.today().strftime('%Y%m'),
                           # restrict_xpaths=r'//div[@class="list"]/ul/li/span[contains(text(), "%s")]/parent::li/a' % datetime.today().strftime(
                           #     '%Y-%m'),
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
            title = xp('//div[@class="list"]/div[@class="tit"]/text()')[0].extract().strip()
            pubtime = xp('//div[@class="list"]//*[contains(text(), "发布时间：")]/text()')[0].extract().replace("发布时间：", "").strip()
            
                
            cv = xp('//div[@id="xw_box"]')[0]
            content, media, video, cover = self.content_clean(cv, kill_xpaths=r'//div[@class="fx fr"]')

            og = xp('//div[@class="list"]//*[contains(text(), "来源")]/text()').extract_first('')
            if og:
                origin_name = re.sub(r'来源[:：]', '', og).strip()
            else:
                og = xp('//div[@class="list"]').re(r"来源[:：]([.\u4E00-\u9FA5]{2,})", re.S)
                origin_name = og[0].strip() if og else ""

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
