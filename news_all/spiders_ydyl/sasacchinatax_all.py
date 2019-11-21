# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


class Sasacchinatax_allSpider(NewsRCSpider):
    """国务院国有资产监督管理委员会&国家税务总局"""
    name = 'sasacchinatax'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        'http://www.sasac.gov.cn/n2588025/n2588119/index.html': 7620,  # 国务院国有资产监督管理委员会
        'http://www.chinatax.gov.cn/n810219/n810724/index.html': 7622,  # 国家税务总局
    }
    rules = (
        # http://www.sasac.gov.cn/n2588025/n2588119/c11593808/content.html
        # http://www.chinatax.gov.cn/n810219/n810724/c4453457/content.html
        
        Rule(LinkExtractor(allow=(r'(?:sasac|chinatax).gov.cn.*?/content.html'),
                           ), callback='parse_item',
             follow=False, process_request=js_meta),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='zsy_cotitle']/text()").extract_first()
            source = xp("//div[@class='zsy_cotitle']/p")[0]
            content_div = xp("//div[@class='zsy_comain']")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//div[@class='zsy_cotitle']/p/text()").extract_first('')
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    # http://www.chinatax.gov.cn/n810219/n810724/c4453457/content.html
    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp("//li[@class='sv_texth1']/text()").extract_first()
            source = xp("//div[@class='zuo1']")[0]
            content_div = xp("//li[@id='tax_content']")[0]
            pubtime = source.re(r'\d{2,4}年\d{1,2}月\d{1,2}日')[0]
            origin_name = xp("//span[@class='meitihuaxian']/a/text()").extract_first('')
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
