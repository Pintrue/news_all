from copy import deepcopy
from scrapy import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.tools.time_translater import Pubtime
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from scrapy.conf import settings


class PeopleSpider(NewsRCSpider):
    name = 'xilu'
    # start_meta = {'jstype': True}
    mystart_urls = {
        "http://www.xilu.com/": 1,
    }

    # http://www.xilu.com/sstj/20191024/1000010001110126.html?hot
    # http://dili.xilu.com/20191024/1000010001110110.html?hot

    rules = (
        Rule(LinkExtractor(allow=(r'xilu.com/\w+/%s\d{2}/\d+\.html?' % datetime.today().strftime('%Y%m'),)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'xilu.com/%s\d{2}/\d+\.html?' % datetime.today().strftime('%Y%m'),)
                           ),
             callback='parse_item', follow=False),

        Rule(LinkExtractor(allow=(r'xilu.com/.*?/\d{2}\.html',)
                           ),
             process_request=otherurl_meta, follow=False),
    )


    def parse_item(self, response):
        # http://www.xilu.com/sstj/20191024/1000010001110126.html?hot
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='tagpagetitle mt10']/h1").extract_first("")
            pubtime = Pubtime(xp("//div[@class='time-x left']/text()").extract_first(""))
            content_div = xp("///div[@id='xilucontentid']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//a[@class='from']/text()").extract_first("")
        # except Exception as e:
        #      return self.produce_debugitem(response, "xpath error")
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
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='tagpagetitle mt10']/h1").extract_first("")
            pubtime = Pubtime(xp("//div[@class='time right']/text()").extract_first(""))
            content_div = xp("//div[@id='xilucontentid']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//div[@class='from left']/text()").extract_first("")
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