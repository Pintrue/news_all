# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Kkxw_allSpider(NewsRCSpider):
    """看看新闻"""
    name = 'kkxw'
    mystart_urls = {
        'http://www.kankanews.com/list/xinwen/511': 1301211,  # 看看新闻-上海
        'http://www.kankanews.com/xinwen/': 1301218,  # 看看新闻-中国-下方列表采集
        'http://www.kankanews.com/list/xinwen/508': 1301210,  # 看看新闻-全球
        'http://www.kankanews.com/list/kandian/744': 1301213,  # 看看新闻-实讯-下方列表采集
        'http://www.kankanews.com/list/xinwen/519': 1301215,  # 看看新闻-文娱
        'http://www.kankanews.com/list/kandian/747': 1301217,  # 看看新闻-正能量-下方列表采集
        'http://www.kankanews.com/list/xinwen/517': 1301207,  # 看看新闻-港澳台-左侧列表
        'http://www.kankanews.com/list/kandian/749': 1301208,  # 看看新闻-看现场
        'http://www.kankanews.com/list/xinwen/513': 1301212,  # 看看新闻-社会
        'http://www.kankanews.com/list/kandian/773': 1301209,  # 看看新闻-酷科技
        'http://www.kankanews.com/list/kandian/775': 1301214,  # 看看新闻-食药安办

    }
    rules = (
        #http://www.kankanews.com/a/2019-06-13/0038885672.shtml?appid=508813
        #http://www.kankanews.com/a/2019-06-13/0038885692.shtml?appid=508826
        Rule(LinkExtractor(allow=(r'kankanews.com/a/%s-\d{2}/\d+.s?htm.*?' % datetime.today().strftime('%Y-%m'),),
                           ), callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            # title = xp("//div[@class='nrHeader']/text()").extract_first()
            title = xp("//h1/text()").extract_first()
            content_div = xp("//div[@class='textBody']")[0]
            pubtime = xp("//div[@class='infor']/p[@class='time']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp('//div[@class="infor"]/p[@class="resource"]/text()').extract_first('')
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
