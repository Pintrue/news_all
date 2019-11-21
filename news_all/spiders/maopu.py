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
<<<<<<< HEAD
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
=======
    start_meta = {'jstype': True}
    mystart_urls = {
        'http://www.mop.com/': 6322,   #  猫扑网
        'https://www.mop.com/energy.html': 6323,   #  猫扑网
        'https://mpqc.eastday.com/': 6324,   #  猫扑网
        'https://mpqc.eastday.com/new-car-recommend/recommend.html': 6325,   #  猫扑网
        'https://mpqc.eastday.com/yongche.html': 6326,   #  猫扑网
        'https://mpqc.eastday.com/video.html': 6327,   #  猫扑网
        'https://mpqc.eastday.com/photo.html': 6328,   #  猫扑网
        'https://mpqc.eastday.com/listpage/auto.html': 6329,   #  猫扑网
        'https://mpqc.eastday.com/mch/mch.html': 6330,   #  猫扑网
        'https://mpqc.eastday.com/playmop.html': 6331,   #  猫扑网
        'https://mpqc.eastday.com/quality.html': 6332,   #  猫扑网
        'https://mpqc.eastday.com/auto-refitting.html': 6333,   #  猫扑网
        'https://mpqc.eastday.com/auto-model.html': 6334,   #  猫扑网

    }

    # http://mpdzh.eastday.com/a/191023135950951983422.html?region=1
    # https://mpqc.eastday.com/a/191112095359623.html
>>>>>>> ba077309f1ae7873931c74f776f818a1b0648465

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
<<<<<<< HEAD
        # http://mpdzh.eastday.com/a/191105153919206187389.html?region=1
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='post-header']/h2").extract_first("")
            pubtime = Pubtime(xp("//span[@class='post-date']/text()").extract_first(""))
=======
        # http://www.mrjjxw.com/articles/2019-10-21/1380159.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='post-header']/h2").extract_first("")
            pubtime = xp("//span[@class='post-date']/text()").extract_first("")
>>>>>>> ba077309f1ae7873931c74f776f818a1b0648465
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
<<<<<<< HEAD
            pubtime = Pubtime(xp("//span[@class='post-date']/span[1]/text()").extract_first(""))
=======
            pubtime = xp("//span[@class='post-date']/span[1]/text()").extract_first("")
>>>>>>> ba077309f1ae7873931c74f776f818a1b0648465
            content_div = xp("//div[@class='detail-article']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//a[@class='post-author-name']/text()").extract_first("")
        except Exception as e:
<<<<<<< HEAD
=======
            return self.parse_item_3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_3(self, response):
        # https://mpqc.eastday.com/a/191112092513701.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//h1[@class='artice-title']/text()").extract_first("")
            pubtime = xp("//div[@class='clear-fix subtile gray']/span[@class='fr']/text()").extract_first("")
            content_div = xp("//div[@class='article']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=["//div[@class='text']"],)
            origin_name = xp("//span[@class='news-source']/text()").extract_first("")
        except Exception as e:
>>>>>>> ba077309f1ae7873931c74f776f818a1b0648465
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
<<<<<<< HEAD
=======
    #
    # def parse_item_3(self, response):
    #
    #     # http://www.cb.com.cn/index/show/gx/cv/cv135195161336
    #     xp = response.xpath
    #     try:
    #         title = self.get_page_title(response).split('_')[0] or xp("//div[@class='phototit w998 auto']").extract_first("")
    #         pubtime = Pubtime(xp("//div[@class='contentmes photomes photomes2']/span[1]/text()").extract_first(""))
    #         content_div = xp("//div[@class='photoimg-bigcen2 auto']")[0]
    #         content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[], )
    #         origin_name = xp("//div[@class='contentmes photomes photomes2']/span[2]/text()").extract_first("")
    #     except Exception as e:
    #         return self.produce_debugitem(response, "xpath error")
    #
    #     return self.produce_item(
    #         response=response,
    #         title=title,
    #         pubtime=pubtime,
    #         origin_name=origin_name,
    #         content=content,
    #         media=media,
    #         videos=videos,
    #
    #     )
>>>>>>> ba077309f1ae7873931c74f776f818a1b0648465
