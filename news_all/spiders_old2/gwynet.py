# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class GwynetSpider(NewsRCSpider):
    '''国务院网站 国务院信息'''
    name = 'gwynet'
    mystart_urls = {
        'http://www.gov.cn/pushinfo/v150203/index.htm': 1301235,  # 国务院网站 国务院信息
    }
    rules = (
        # http://www.gov.cn/premier/2019-06/11/content_5399323.htm
        # http://www.gov.cn/premier/2019-06/06/content_5398110.htm
        Rule(LinkExtractor(allow=(r'gov.cn/premier/%s/\d{2}/content_\d+\.htm' % datetime.today().strftime('%Y-%m'),),), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//div[@class="article oneColumn pub_border"]/h1/text()').extract_first()
            content_div = xp('//div[@id="UCAP-CONTENT"]')[0]
            pubtime = xp('//div[@class="pages-date"]/text()').extract_first().strip()
            origin_name = xp('//div[@class="pages-date"]/span[@class="font"]/text()').extract_first().replace('来源：','').strip()
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
