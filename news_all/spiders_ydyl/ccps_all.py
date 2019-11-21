# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


class Ccps_allSpider(NewsRCSpider):
    """党校声音"""
    name = 'ccps'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        'http://www.ccps.gov.cn/dxsy/': 7632,  # 中共中央党校
    }
    rules = (
        # http://www.ccps.gov.cn/dxsy/201906/t20190627_132601.shtml
        
        Rule(LinkExtractor(allow=(r'ccps.gov.cn.*?/%s/t\d+_\d+.shtml') % datetime.today().strftime("%Y%m"),
                           ), callback='parse_item',
             follow=False, process_request=js_meta),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h2[@class='xlTitle xtitle-center']/text()").extract_first()
            # source = xp("//div[@class='pageHead']/h3")[0]
            content_div = xp("//div[@class='TRS_Editor']")[0]
            pubtime = xp("//div[@class='xlCenterL']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//div[@class='xlLy']/text()").extract_first()
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
