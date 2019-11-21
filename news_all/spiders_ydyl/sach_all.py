# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


class Sach_allSpider(NewsRCSpider):
    """国家文物局"""
    name = 'sach'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        'http://www.sach.gov.cn/col/col722/index.html': 7636,  # 国家文物局
    }
    rules = (
        # http://www.sach.gov.cn/art/2019/6/26/art_722_155787.html
        # sach.gov.cn.*?/\d{4}/\d{1,2}/\d{2}/art_\d+_\d+.html
        
        Rule(LinkExtractor(allow=(r'sach.gov.cn.*?/\d{4}/\d{1,2}/\d{2}/art_\d+_\d+.html'),
                           ), callback='parse_item',
             follow=False, process_request=js_meta),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title_total = xp("//table[3]/tbody/tr[1]/td/text()").extract()
            title = ''
            for i in range(len(title_total)):
                title = title + title_total[i]

            # source = xp("//div[@class='pageHead']/h3")[0]
            content_div = xp("//div[@id='zoom']")[0]
            pubtime = xp("//td[@class='art_top'][2]/span").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="",
            content=content,
            media=media
        )
