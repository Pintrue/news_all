# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Zgzxw_allSpider(NewsRCSpider):
    """中国政协网"""
    name = 'zgzxw'
    mystart_urls = {
        'http://www.cppcc.gov.cn/zxww/newcppcc/zxyw/index.shtml': 7642,  # 中国人民政治协商会议全国委员会
    }
    rules = (
        # http://www.cppcc.gov.cn/zxww/2019/06/25/ARTI1561421709036136.shtml
        
        Rule(LinkExtractor(allow=(r'cppcc.gov.cn.*?/\d{4}/\d{2}/\d{2}/\w+\d+.shtml'),
                           ), callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='cnt_box']/h3/text()").extract_first()
            content_div = xp("//div[@class='cnt_box']/div[@class='con']")[0]
            pubtime = xp("//span[@class='info']/i").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]

            origin_name = xp("//span[@class='info']/em/text()[2]").extract_first()
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
