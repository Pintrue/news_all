# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class ZgjtbSpider(NewsRCSpider):
    '''中国交通报'''
    name = 'zgjtb'
    mystart_urls = {'http://www.zgjtb.com/node_142.htm': 1301604,   #  中国交通报-要闻-左侧列表
    }

    # http://www.zgjtb.com/2019-06/10/content_222077.htm
    # http://www.zgjtb.com/2019-06/05/content_222032.htm
    rules = (
        Rule(LinkExtractor(allow=(r'zgjtb.com/%s/\d{2}/[a-z]+_\d+.htm' % datetime.today().strftime('%Y-%m'),),
                           ), callback='parse_item',
             follow=False),
    )
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='details-left']/h1/text()").extract_first()
            content_div = xp('//div[@class="article-main"]')[0]
            pubtime = xp('//div[@class="source"]/i[1]/text()').extract_first()
            
            
            origin_name = xp("//div[@class='source']/i[2]/a/text()").extract_first()

        except:
            return self.produce_debugitem(response, "xpath error")
            # return self.parse_item_2(response)
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
