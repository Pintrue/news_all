# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Guanchazhe_allSpider(NewsRCSpider):
    """观察者网"""
    name = 'gczw'
    mystart_urls = {
        'http://www.guancha.cn/GuoJi%C2%B7ZhanLue/list_1.shtml': 1200953,  # 观察者网-国际资讯
        'http://www.guancha.cn/politics': 1200952,  # 观察者网-政治-全部抓取
        'http://www.guancha.cn/': 13120,  # 观察者网-除头条外左侧评论及卡片区域全部

    }
    rules = (
        #https://www.guancha.cn/internation/2019_06_24_506771.shtml
        #https://www.guancha.cn/politics/2019_06_24_506774.shtml
        #https://www.guancha.cn/FaLiDe-ZhaKaLiYa/2019_06_23_506710.shtml
        Rule(LinkExtractor(allow=(r'guancha.cn.*?/%s_\d{2}_\d+.shtml' % datetime.today().strftime('%Y_%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//li[@class='left left-main']/h3/text()").extract_first()
            content_div = xp("//div[@class='content all-txt']")[0]
            pubtime = xp("//div[@class='time fix']/span[1]").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//div[@class='time fix']/span[3]/text()").extract_first('')
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
