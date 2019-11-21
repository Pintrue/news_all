# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta
from news_all.tools.time_translater import Pubtime


class TwentyOneSpider(NewsRCSpider):
    """21cn"""
    name = '21CN'

    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        'http://www.21cn.com/': 683,
    }
    # http://dangjian.21cn.com/redian/a/2019/1031/11/33720151.shtml
    rules = (
        Rule(LinkExtractor(allow=(r'dangjian.21cn.com/.*?/%s.*?/\d+.shtml' % datetime.today().strftime('%Y/%m')),
                           ),
             callback='parse_item', follow=False, process_request=js_meta),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@id="article_text"]')[0]
            head_div = xp('.//div[@class="info fl"]')[0]
            origin_name = head_div.xpath('.//*/a/text()').extract_first('').strip()
            title = xp('.//h1/text()').extract()[0]
            pubtime = Pubtime(xp("//span[@class='pubTime']/text()").extract_first())
            # pubtime = head_div.re(r'\d{2,4}年\d{1,2}月\d{1,2}日 \d{1,2}:\d{1,2}')[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        content, media, videos, video_cover = self.content_clean(news_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
