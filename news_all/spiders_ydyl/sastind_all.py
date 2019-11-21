# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Sastind_allSpider(NewsRCSpider):
    """国家国防科技工业局"""
    name = 'sastind'
    mystart_urls = {
        'http://www.sastind.gov.cn/n112/n117/index.html': 7634,  # 国家国防科技工业局
    }
    rules = (
        # http://www.sastind.gov.cn/n112/n117/c6806646/content.html
        
        Rule(LinkExtractor(allow=(r'sastind.gov.cn.*?/content.html'),
                           ), callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//td/div[@id='con_title']/text()").extract_first()
            # source = xp("//div[@class='pageHead']/h3")[0]
            content_div = xp("//td[@class='black14_30']")[0]
            pubtime = xp("//span[@id='con_time']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//td[@class='sv_brown']/text()").extract_first().split(']\u3000  \r\n')[0].replace(
                '[ 信息来源：', '').strip()
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
