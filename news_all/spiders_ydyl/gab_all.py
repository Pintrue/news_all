# -*- coding: utf-8 -*-


from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


# 中华人民共和国公安部
class GabAllSpider(NewsRCSpider):
    name = 'gab_all'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        'http://www.mps.gov.cn/n2254098/n4904352/index.html': 7609,  # 中华人民共和国公安部 工作动态
    }

    # http://www.mps.gov.cn/n2254098/n4904352/c6526781/content.html    http://www.mps.gov.cn/n2254098/n4904352/c6550367/content.html
    rules = (
        Rule(LinkExtractor(allow=r'mps.gov.cn/.*?/content.html',
                           deny='video', ), callback='parse_item',
             follow=False,process_request=js_meta),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('/html/head/title/text()').extract()[0]
            content_div = xp('//div[@id="ztdx"]')[0]
            source_div = xp('//div[@class="arcTool relative"]')[0]
            pubtime = source_div.re(r'\d{2,4}年\d{1,2}月\d{1,2}日')[0]
        except:
            return self.parse_item_2(response)

        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            # origin_name=origin_name,
            
            content=content,
            media=media,
            videos=videos,
        )
    
    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='cnt_nav']/h3/text()").extract()[0]
            content_div = xp("//div[@class='cnt_bd']")[0]
            pubtime = xp("//p[@class='info']/text()").re(r'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}')[0]
            origin_name = xp("//p[@class='info']/i/text()").extract_first()
        except:
            return self.produce_debugitem(response, 'xpath error')
        
        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media,
            videos=videos,
        )