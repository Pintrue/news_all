from copy import deepcopy
from scrapy import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.tools.time_translater import Pubtime
<<<<<<< HEAD
from news_all.spider_models import NewsRCSpider, otherurl_meta
=======
from news_all.spider_models import NewsRCSpider, otherurl_meta, js_meta
>>>>>>> ba077309f1ae7873931c74f776f818a1b0648465
from datetime import datetime
from scrapy.conf import settings


class PeopleSpider(NewsRCSpider):
    name = 'tiexue'
<<<<<<< HEAD
    # start_meta = {'jstype': True}
=======
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
>>>>>>> ba077309f1ae7873931c74f776f818a1b0648465
    mystart_urls = {
        "https://www.tiexue.net/": 1,
    }

    # https://bbs.tiexue.net/post2_13504465_1.html
    # https://topic.tiexue.net/cpost_9056809.html
<<<<<<< HEAD

    rules = (
        Rule(LinkExtractor(allow=(r'tiexue.net/post2_\d+_1\.html',)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'tiexue.net/cpost_\d+\.html',)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'tiexue.net/.*?_d+\.html',)
=======
    # https://topic.tiexue.net/cpost_9056809.html

    rules = (
        Rule(LinkExtractor(allow=(r'tiexue.net/\w+\.html',)
                           ),
             callback='parse_item', follow=False, process_request=js_meta),
        Rule(LinkExtractor(allow=(r'tiexue.net/.*?\.html',)
>>>>>>> ba077309f1ae7873931c74f776f818a1b0648465
                           ),
             process_request=otherurl_meta, follow=False),
    )


    def parse_item(self, response):
        # https://bbs.tiexue.net/post2_13504480_1.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//h1[@class='a-title']").extract_first("")
<<<<<<< HEAD
            # pubtime = Pubtime(xp("='time']").extract_first(""//span[@class))
            content_div = xp("//div[@class='newconli2']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
#            origin_name = {}
#         except Exception as e:
#              return self.produce_debugitem(response, "xpath error")
=======
            pubtime = Pubtime(xp("//span[@class='time']/text()").get())
            content_div = xp("//div[@class='newconli2']")[0]
            content, media, videos, video_cover = self.content_clean(content_div,
                                                                     kill_xpaths=["//iframe[@id='iframeu3137068_0']"],)
            origin_name = {}

>>>>>>> ba077309f1ae7873931c74f776f818a1b0648465
        except:
            return self.parse_item_2(response)
        return self.produce_item(
            response=response,
            title=title,
<<<<<<< HEAD
            # pubtime=pubtime,
#            origin_name=origin_name,
=======
            pubtime=pubtime,
            origin_name=origin_name,
>>>>>>> ba077309f1ae7873931c74f776f818a1b0648465
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_2(self, response):

     # https://topic.tiexue.net/cpost_9069906.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//h1[@class='post_tit']").extract_first("")
            pubtime = Pubtime(xp("///span[@class='float_L']/text()").extract_first(""))
            content_div = xp("//div[@class='newconli2']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
<<<<<<< HEAD
#            origin_name = {}
#         except:
#             return self.parse_item_3(response)
=======
            origin_name = {}
>>>>>>> ba077309f1ae7873931c74f776f818a1b0648465
        except Exception as e:
             return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
<<<<<<< HEAD
#            origin_name=origin_name,
=======
            origin_name=origin_name,
>>>>>>> ba077309f1ae7873931c74f776f818a1b0648465
            content=content,
            media=media,
            videos=videos,

        )

#     def parse_item_3(self, response):
#
#         # http://www.cb.com.cn/index/show/gx/cv/cv135195161336
#         xp = response.xpath
#         try:
#             title = self.get_page_title(response).split('_')[0] or xp("//h1[@class='post_tit']").extract_first("")
#             pubtime = Pubtime(xp("//span[@class='float_L']/text()").extract_first(""))
#             content_div = xp("//p[@class='font14g']")[0]
#             content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[], )
# #            origin_name = {}
#         except Exception as e:
#             return self.produce_debugitem(response, "xpath error")
#
#         return self.produce_item(
#             response=response,
#             title=title,
#             pubtime=pubtime,
# #            origin_name=origin_name,
#             content=content,
#             media=media,
#             videos=videos,
#
#         )