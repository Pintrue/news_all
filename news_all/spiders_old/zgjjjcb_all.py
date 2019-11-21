# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Zjj_allSpider(NewsRCSpider):
    """中国纪检监察报"""
    name = 'zgjjjcb'
    mystart_urls = {
        'http://www.ccdi.gov.cn/ldhd/gcsy/': 1301597,  # 中国纪检监察报-首页-领导活动

    }
    rules = (
        Rule(LinkExtractor(allow=(r'ccdi.gov.cn.*?/%s/t\d{8}_\d+.html' % datetime.today().strftime('%Y%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h2[@class='tit']/text()").extract_first()
            source = xp("//h3[@class='daty']")[0]
            content_div = xp("//div[@class='TRS_Editor']")[0]

            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            
            

            origin_name = xp('//div[@class="daty_con"]/em[@class="e e1"]/text()').extract_first('')
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
