# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Chongqing_allSpider(NewsRCSpider):
    """重庆日报"""
    name = 'cqrb'
    mystart_urls = {
        'http://www.cqrb.cn/node/node_123.htm': 1301644,  # 重庆日报-重庆
    }
    rules = (
        #https://www.cqrb.cn/content/2019-06/25/content_198641.htm
        #https://www.cqcb.com/topics/shaiwenhuashaifengjingdaxingwenlv/zuixinzixun/2019-06-24/1702388.html
        Rule(LinkExtractor(allow=(r'cqrb.cn.*?/%s/\d{2}/content_\d+.htm' % datetime.today().strftime('%Y-%m'), ),
                           ), callback='parse_item',
             follow=False),

        Rule(LinkExtractor(allow=(r'cqcb.com.*?/%s-\d{2}/\d+.html' % datetime.today().strftime('%Y-%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    #https://www.cqrb.cn/content/2019-06/25/content_198641.htm
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='dbt']/text()").extract_first()
            content_div = xp("//div[@class='contents']")[0]
            pubtime = xp("//div[@class='edit']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//div[@class='from']/text()").extract_first('')
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    #https://www.cqcb.com/topics/shaiwenhuashaifengjingdaxingwenlv/zuixinzixun/2019-06-24/1702388.html
    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='ftop_biaoti']/h1/text()").extract_first()
            content_div = xp("//div[@class='farticle_text']")[0]
            pubtime = xp("//div[@class='ftop_biaoti']/h2/span[1]").re(r'\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//div[@class='ftop_biaoti']/h2/span[3]/text()").extract_first('')
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
