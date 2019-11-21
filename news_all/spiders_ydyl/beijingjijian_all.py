# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


class Bjjj_allSpider(NewsRCSpider):
    """北京纪检监察网"""
    name = 'bjjj'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        'http://www.bjsupervision.gov.cn/ywyl/': 7648,  # 中共北京市纪律检查委员会
        'http://www.bjsupervision.gov.cn/ttxw/': 7649,  # 中共北京市纪律检查委员会
    }
    rules = (
        # http://www.bjsupervision.gov.cn/ywyl/201906/t20190626_64957.html
        # http://www.bjsupervision.gov.cn/ttxw/201906/t20190626_64950.html
        Rule(LinkExtractor(allow=(r'bjsupervision.gov.cn.*?/\d{6}/t\d+_\d+.html'),
                           ), callback='parse_item',
             follow=False, process_request=js_meta),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='detail']/h1/text()").extract_first()
            source = xp("//span[@class='detail-span']")[0]
            content_div = xp("//div[@class='TRS_Editor']")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//span[@class='detail-span']/text()").extract_first().split('|')[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
