# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


class sppgov_allSpider(NewsRCSpider):
    """中华人民共和国最高人民检察院"""
    name = 'sppgov'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        'http://www.spp.gov.cn/spp/qwfb/index.shtml': 7643,  # 中华人民共和国最高人民检察院
        'http://www.spp.gov.cn/spp/zdgz/index.shtml': 7644,  # 中华人民共和国最高人民检察院
        'http://www.spp.gov.cn/spp/tt/index.shtml': 7645,  # 中华人民共和国最高人民检察院
    }
    rules = (
        # http://www.spp.gov.cn/spp/zdgz/201906/t20190626_423039.shtml
        # http://www.spp.gov.cn/spp/qwfb/201906/t20190625_422948.shtml
        
        Rule(LinkExtractor(allow=(r'spp.gov.cn.*?/t\d+_\d+.shtml'),
                           ), callback='parse_item',
             follow=False, process_request=js_meta),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='detail_tit']/text()").extract_first()
            source = xp("//div[@class='detail_extend1 fl']")[0]
            content_div = xp("//div[@id='fontzoom']")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//div[@class='detail_extend1 fl']").re('来源：(\w{2,})')[0]
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
