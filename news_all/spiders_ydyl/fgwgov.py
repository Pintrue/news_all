# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


class FgwgovSpider(NewsRCSpider):
    '''中华人民共和国国家发展和改革委员会
    国务院发展研究中心'''
    name = 'fgwgov'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        "http://www.ndrc.gov.cn/jjxsfx/index.html": 7605,
        "http://www.drc.gov.cn/xsyzcfx/": 7606,
        "http://www.drc.gov.cn/xsyzcfx/c4-l460.htm":7607,
    }
    rules = (
        # http://www.ndrc.gov.cn/jjxsfx/201905/t20190531_938106.html
        # http://www.drc.gov.cn/xsyzcfx/20190624/4-4-2898817.htm
        # http://www.drc.gov.cn/xsyzcfx/20190701/4-459-2898855.htm
        Rule(LinkExtractor(allow=(r'gov.cn/[a-z]+/\d{4,8}/.*?\.htm',),
                           ), callback='parse_item',
             follow=False,process_request=js_meta),

    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='txt_title1 tleft']/text()").extract_first()
            content_div = xp("//div[@class='TRS_Editor']")[0]
            pubtime = xp("//div[@class='txt_subtitle1 tleft']/text()").extract_first().strip()
            origin_name = xp("//span[@id='dSourceText']/a/text()").extract_first()
        except:
            return self.parse_item_2(response)

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

    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@id='MainContent_docSubject']/text()").extract_first()
            content_div = xp("//div[@id='MainContent_docContent']")[0]
            pubtime = xp("//div[@id='MainContent_docAuthor']/text()").extract_first().strip()
            origin_name = xp("//div[@id='MainContent_docSource']/text()[2]").extract_first().split('2019')[0]
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )