# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


class Csrccma_allSpider(NewsRCSpider):
    """中国证券监督管理委员会&中国气象网"""
    name = 'csrccma'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        'http://www.cma.gov.cn/2011xwzx/2011xqxxw/2011xzytq/': 7630,  # 中国气象局
        'http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/': 7631,  # 中国证券监督管理委员会
    }
    rules = (
        # http://www.cma.gov.cn/2011xwzx/2011xqxxw/2011xzytq/201906/t20190627_528356.html
        # http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/201906/t20190625_357873.html
        
        Rule(LinkExtractor(allow=(r'(?:cma|csrc).gov.cn.*?/%s/t\d+_\d+.html' % datetime.today().strftime('%Y%m'),),
                           ), callback='parse_item',
             follow=False, process_request=js_meta),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='news_text']/h1/text()").extract_first()
            # source = xp("//div[@class='pageHead']/h3")[0]
            content_div = xp("//div[@class='TRS_Editor']")[0]
            pubtime = xp("//div[@class='news_textspan']/div[1]/span[2]").re(r'\d{2,4}年\d{1,2}月\d{1,2}日')[0]
            origin_name = xp("//div[@class='news_textspan']/div[1]/span[1]/text()").extract_first('')
        except:
            return self.parse_item_2(response)

        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_2(self, response):
        
        xp = response.xpath
        try:
            title = xp("//div[@class='title']/text()").extract_first()
            # source = xp("//div[@class='pageHead']/h3")[0]
            content_div = xp("//div[@class='Custom_UnionStyle']")[0]
            pubtime = xp("//div[@class='time']/span[2]").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//div[@class='time']/span[1]/text()").extract_first('')
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
