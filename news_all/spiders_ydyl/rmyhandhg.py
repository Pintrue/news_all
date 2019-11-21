# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider
from news_all.tools.time_translater import Pubtime


class RmyhandhgSpider(NewsRCSpider):
    '''中国人民银行
    中华人民共和国海关总署'''
    name = 'rmyhandhg'
    mystart_urls = {
        "http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html": 7619,
        "http://www.customs.gov.cn/customs/302249/302425/index.html": 7621,
    }
    rules = (
        # http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/3849737/index.html
        # http://www.customs.gov.cn/customs/302249/302425/2467833/index.html
        Rule(LinkExtractor(allow=(r'gov.cn/[a-z]+/\d+/\d+/\d+/index\.html',),
                           deny=(r'http://www.customs.gov.cn/customs/302249/302266/302267/index.html',
                                 r'http://www.customs.gov.cn/customs/302249/302334/302335/index.html',
                                 r'http://www.customs.gov.cn/customs/302249/302306/302307/index.html',
                                 r'http://www.customs.gov.cn/customs/302249/302303/302304/index.html',
                                 r'http://www.customs.gov.cn/customs/302249/302330/302331/index.html',
                                 r'http://www.customs.gov.cn/customs/302249/302274/302275/index.html',
                                 r'http://www.customs.gov.cn/customs/302249/302270/302272/index.html',),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("/html/head/title/text()").extract_first()
            content_div = xp("//div[@id='zoom']")[0]
            pubtime = xp("//td[@class='hui12'][3]/text()").extract_first().strip()
            origin_name = xp("//span[@id='laiyuan']/text()").extract_first()
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )

    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='easysite-news-title']/h2/text()").extract_first()
            content_div = xp("//div[@id='easysiteText']")[0]
            pubtime = Pubtime(xp("//p[@class='easysite-news-describe']/text()")[0].extract())
            origin_name = xp("//span[@id='laiyuan']/text()").extract_first()
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
