from copy import deepcopy
from scrapy import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.tools.time_translater import Pubtime
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from scrapy.conf import settings


class PeopleSpider(NewsRCSpider):
    name = 'tiexue'
    # start_meta = {'jstype': True}
    mystart_urls = {
        "https://www.tiexue.net/": 1,
    }

    # https://bbs.tiexue.net/post2_13504465_1.html
    # https://topic.tiexue.net/cpost_9056809.html

    rules = (
        Rule(LinkExtractor(allow=(r'tiexue.net/post2_\d+_1\.html',)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'tiexue.net/cpost_\d+\.html',)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'tiexue.net/.*?_d+\.html',)
                           ),
             process_request=otherurl_meta, follow=False),
    )


    def parse_item(self, response):
        # https://bbs.tiexue.net/post2_13504480_1.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//h1[@class='a-title']").extract_first("")
            # pubtime = Pubtime(xp("='time']").extract_first(""//span[@class))
            content_div = xp("//div[@class='newconli2']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
#            origin_name = {}
#         except Exception as e:
#              return self.produce_debugitem(response, "xpath error")
        except:
            return self.parse_item_2(response)
        return self.produce_item(
            response=response,
            title=title,
            # pubtime=pubtime,
#            origin_name=origin_name,
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
#            origin_name = {}
#         except:
#             return self.parse_item_3(response)
        except Exception as e:
             return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
#            origin_name=origin_name,
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