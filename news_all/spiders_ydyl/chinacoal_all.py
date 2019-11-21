# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Chinacoal_allSpider(NewsRCSpider):
    """国家煤矿安全监察局"""
    name = 'chinacoal'
    mystart_urls = {
        'http://www.chinacoal-safety.gov.cn/xw/mkaqjcxw/': 7637,  # 国家煤矿安全监察局
    }
    rules = (
        # http://www.chinacoal-safety.gov.cn/xw/mkaqjcxw/201906/t20190626_311105.shtml
        
        Rule(LinkExtractor(allow=(r'chinacoal-safety.gov.cn.*?/\d{6}/t\d+_\d+.shtml'),
                           ), callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            content_div = xp("//div[@class='TRS_Editor']")[0]
            pubtime = xp("//span[@class='tdate']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//span[@class='source']/text()").extract_first('')

            title = xp('.//p[@class="MsoNormal"][1]/b[1]/span/text()').extract_first('').strip()
            sub_title = xp('.//p[@class="MsoNormal"][2]/b[1]/span/text()').extract_first('').strip()
            title = join_titles(title, sub_title)
        
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )


def join_titles(title, sub_title):
    if sub_title:
        if sub_title.startswith("——"):
            title += sub_title
        else:
            title += "——" + sub_title
    return title
