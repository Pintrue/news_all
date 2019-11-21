from copy import deepcopy
from datetime import datetime
from scrapy import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.tools.time_translater import Pubtime
from news_all.spider_models import NewsRCSpider, otherurl_meta


class PeopleSpider(NewsRCSpider):
    name = 'zgjyw'
    mystart_urls = {
        "http://www.cb.com.cn/":1,
    }

#http://www.cb.com.cn/index/show/gx/cv/cv135194901330

    rules = (
        Rule(LinkExtractor(allow=r'cb.com.cn/index/show/\w+/\w+/cv\d+',
                           ),
             callback='parse_item',follow=False),
        Rule(LinkExtractor(allow=(r'cb.com.cn/.*?\d{6}',)
                           ),
             process_request=otherurl_meta, follow=False),
    )


    def parse_item(self, response):
        #http://www.cb.com.cn/index/show/gx/cv/cv135195161336
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='contenttit auto']").extract_first("")
            pubtime = Pubtime(xp("//div[@class='contentmes auto']/span[1]/text()").extract_first(""))
            content_div = xp("//div[@class='contenttext auto']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//div[@class='contentmes auto']/span[2]/text()").extract_first("")
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

     #http://www.cb.com.cn/index/show/gx/cv/cv135195161336
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='zlshowtit auto']").extract_first("")
            pubtime = Pubtime(xp("//div[@class='contentmes auto']/span[1]/text()").extract_first(""))
            content_div = xp("//div[@class='zlshowtext auto']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//div[@class='contentmes auto']/span[3]/text()").extract_first("")
        except:
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

        # http://www.cb.com.cn/index/show/gx/cv/cv135195161336
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='phototit w998 auto']").extract_first("")
            pubtime = Pubtime(xp("//div[@class='contentmes photomes photomes2']/span[1]/text()").extract_first(""))
            content_div = xp("//div[@class='photoimg-bigcen2 auto']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[], )
            origin_name = xp("//div[@class='contentmes photomes photomes2']/span[2]/text()").extract_first("")
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