# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


class NyncbSpider(NewsRCSpider):
    '''农业农村部'''
    name = 'nyncb'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        "http://www.moa.gov.cn/xw/zwdt/index.htm": 7617,
    }
    rules = (
        # http://www.moa.gov.cn/xw/zwdt/201906/t20190626_6319458.htm
        # http://www.moa.gov.cn/xw/zwdt/201906/t20190626_6319484.htm
        Rule(LinkExtractor(allow=(r'moa.gov.cn/xw/zwdt/\d{6}/t\d{8}_\d+\.htm',),
                           ), callback='parse_item',
             follow=False, process_request=js_meta),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title_total = xp("//h1[@class='bjjMTitle']/text()").extract()
            title = ''
            for i in range(len(title_total)):
                title = title + title_total[i]
            content_div = xp("//div[@class='Custom_UnionStyle']")[0]
            pubtime = xp("//span[@class='dc_2'][1]/span/text()").extract_first().strip()
            origin_name = xp("//span[@class='dc_2'][3]/span/text()").extract_first()
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
            title_total = xp("//h1[@class='bjjMTitle']/span/text()").extract()
            title = ''
            for i in range(len(title_total)):
                title = title + title_total[i]
            content_div = xp("//p[@class='Custom_UnionStyle']")[0]
            pubtime = xp("//span[@class='dc_2'][1]/span/text()").extract_first().strip()
            origin_name = xp("//span[@class='dc_2'][3]/span/text()").extract_first()
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_3(response)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )

    def parse_item_3(self, response):
        xp = response.xpath
        try:
            title_total = xp("//h1[@class='bjjMTitle']/text()").extract()
            title = ''
            for i in range(len(title_total)):
                title = title + title_total[i]
            content_div = xp("//div[@class='TRS_Editor']")[0]
            pubtime = xp("//span[@class='dc_2'][1]/span/text()").extract_first().strip()
            origin_name = xp("//span[@class='dc_2'][3]/span/text()").extract_first()
        except:
            return self.produce_debugitem(response, "xpath error")
            # return self.parse_item_3(response)

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )