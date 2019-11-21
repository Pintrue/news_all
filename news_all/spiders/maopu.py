from copy import deepcopy
from scrapy import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.tools.time_translater import Pubtime
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from scrapy.conf import settings


class PeopleSpider(NewsRCSpider):
    name = 'maopu'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        "http://www.mop.com/": 1,
    }

    # http://mpdzh.eastday.com/a/191023135950951983422.html?region=1

    rules = (
        Rule(LinkExtractor(allow=(r'eastday.com/a/\d+\.html',)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'eastday.com/a/\d+\.html\?region=1',)
                           ),
             callback='parse_item', follow=False),
        # # Rule(LinkExtractor(allow=(r'mop.com/.*',)
        # #                    ),
        # #      callback='parse_item', follow=False),
        # Rule(LinkExtractor(allow=(r'eastday.com/.*\.html',)
        #                    ),
        #      process_request=otherurl_meta, follow=False),
        # Rule(LinkExtractor(allow=(r'eastday.com/.*\.html?',)
        #                    ),
        #      process_request=otherurl_meta, follow=False),
    )


    def parse_item(self, response):
        # http://mpdzh.eastday.com/a/191105153919206187389.html?region=1
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='post-header']/h2").extract_first("")
            pubtime = Pubtime(xp("//span[@class='post-date']/text()").extract_first(""))
            content_div = xp("//div[@class='detail-article']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//a[@class='post-author-name']/text()").extract_first("")
        # except Exception as e:
        #     return self.produce_debugitem(response, "xpath error")
        except:
            return self.parse_item_2(response)
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_2(self, response):

     # http://mpdzh.eastday.com/a/171008113310537474039.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='post-header']/h2").extract_first("")
            pubtime = Pubtime(xp("//span[@class='post-date']/span[1]/text()").extract_first(""))
            content_div = xp("//div[@class='detail-article']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//a[@class='post-author-name']/text()").extract_first("")
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )
