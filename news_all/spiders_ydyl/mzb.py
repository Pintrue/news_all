# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


class MzbSpider(NewsRCSpider):
    '''民政部'''
    name = 'mzb'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        "http://www.mca.gov.cn/article/xw/mzyw/?": 7610,
    }
    rules = (
        # http://www.mca.gov.cn/article/xw/mzyw/201906/20190600017982.shtml
        Rule(LinkExtractor(allow=(r'gov.cn/article/xw/mzyw/\d{6}/\d+\.s?html',),
                           deny=(r'http://www.mca.gov.cn/article/xw/mzyw/201906/20190600018032.shtml'),
                           ), callback='parse_item',
             follow=False,process_request=js_meta),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title_total = xp("//h3[@class='mtitle']/text()").extract()
            title = ''
            for i in range(len(title_total)):
                title = title + title_total[i]
            content_div = xp("//div[@id='zoom']")[0]
            pubtime = xp("//div[@class='source']/center/text()[2]").re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')[0].strip()
            origin_name = xp("//div[@class='source']/center/text()[3]").extract_first()
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
