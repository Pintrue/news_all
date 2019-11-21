# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class YjglbSpider(NewsRCSpider):
    '''应急管理部'''
    name = 'yjglb'
    mystart_urls = {
        "http://www.chinasafety.gov.cn/xw/bndt/": 7618,
    }
    rules = (
        # http://www.mem.gov.cn/xw/bndt/201906/t20190627_311114.shtml
        # http://www.mem.gov.cn/xw/bndt/201906/t20190625_311069.shtml
        Rule(LinkExtractor(allow=(r'mem.gov.cn/xw/bndt/\d{6}/t\d{8}_\d+\.s?html',),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='zhenwen']/h2/text()").extract_first() or \
                    xp("/html/head/title/text()").extract_first()
            content_div = xp("//div[@class='TRS_Editor']")[0]
            pubtime = xp("//div[@class='time_laiy']/span[1]/text()").extract_first().strip()
            
            
            origin_name = xp("//div[@class='time_laiy']/span[2]/text()").extract_first()
        except:
            return self.produce_debugitem(response, "xpath error")
            # return self.parse_item_2(response)
        # 过滤视频


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
