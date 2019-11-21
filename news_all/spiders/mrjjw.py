from copy import deepcopy
from scrapy import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.tools.time_translater import Pubtime
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime


class PeopleSpider(NewsRCSpider):
    name = 'mrjjw'

    mystart_urls = {
            'http://www.mrjjxw.com/': 6433,  # 每日经济网
            'http://www.mrjjxw.com/mrjjxw/ui_columns/company': 6434,  # 每日经济网
            'http://www.mrjjxw.com/mrjjxw/ui_columns/video': 6435,  # 每日经济网
            'http://www.mrjjxw.com/mrjjxw/ui_columns/new_economy': 6436,  # 每日经济网
            'http://www.mrjjxw.com/mrjjxw/ui_columns/realty': 6437,  # 每日经济网
            'http://www.mrjjxw.com/mrjjxw/ui_columns/auto': 6438,  # 每日经济网
            'http://www.mrjjxw.com/mrjjxw/ui_columns/city': 6439,  # 每日经济网
            'http://www.mrjjxw.com/mrjjxw/ui_columns/digit': 6440,  # 每日经济网
            'http://www.mrjjxw.com/mrjjxw/ui_columns/popular': 6441,  # 每日经济网
    }

    # http://www.mrjjxw.com/articles/2019-10-23/1380626.html
    # http://www.mrjjxw.com/articles/2019-10-22/1380468.html

    rules = (
        Rule(LinkExtractor(allow=r'.mrjjxw.com/articles/%s-\d{2}/\d+\.html' % datetime.today().strftime('%Y-%m'),
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'.mrjjxw.com/.*\.html', deny=(r'201[0-8]', r'2019-0[1-9]', r'2019-1[0]')
                           ),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        # http://www.mrjjxw.com/articles/2019-10-21/1380159.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='m-articleBox']/h1").extract_first("")
            pubtime = Pubtime(xp("//span[@class='u-articleTime']/text()").extract_first(""))
            content_div = xp("//div[@class='m-articleContent']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//div[@class='u-source']/span/text()").extract_first("")
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

    # def parse_item_2(self, response):
    #
    #  #http://www.cb.com.cn/index/show/gx/cv/cv135195161336
    #     xp = response.xpath
    #     try:
    #         title = self.get_page_title(response).split('_')[0] or xp("//div[@class='zlshowtit auto']").extract_first("")
    #         pubtime = Pubtime(xp("//div[@class='contentmes auto']/span[1]/text()").extract_first(""))
    #         content_div = xp("//div[@class='zlshowtext auto']")[0]
    #         content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
    #         origin_name = xp("//div[@class='contentmes auto']/span[3]/text()").extract_first("")
    #     except:
    #         return self.parse_item_3(response)
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