from copy import deepcopy
from scrapy import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.tools.time_translater import Pubtime
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime


class PeopleSpider(NewsRCSpider):
    name = 'kaiwind'
    mystart_urls = {
        "http://www.kaiwind.com/": 1,
    }
    #http://news.kaiwind.com/photo/201911/15/t20191115_6919045.shtml
    #http://news.kaiwind.com/info/201911/18/t20191118_6920552.shtml
    #http://news.kaiwind.com/info/201911/17/t20191117_6920457.shtml
    #http://www.kaiwind.com/anticult/xingao/2019/201911/15/t20191115_6919647.shtml
    #http://www.kaiwind.com/anticult/xingao/2019/201910/23/t20191023_6903577.shtml
    rules = (
        Rule(LinkExtractor(allow=r'kaiwind.com/\w+/%s/\d{2}/t\d+_\d+\.shtml' % datetime.today().strftime('%Y%m'),
                           ),
             callback='parse_item',follow=False),
        Rule(LinkExtractor(allow=r'kaiwind.com/\w+/\w+/2019/%s/\d{2}/t\d+_\d+\.shtml' % datetime.today().strftime('%Y%m'),
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'kaiwind.com/.*\.shtml',)
                           ),
             process_request=otherurl_meta, follow=False),
    )


    def parse_item(self, response):
        #http://www.mrjjxw.com/articles/2019-10-21/1380159.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//h1[@id='p_biaoti']").extract_first("")
            pubtime = xp("//div[@id='p_laiyuan']/text()").get().split()[0].split("：")[1]
            content_div = xp("//div[@class='TRS_Editor']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//div[@id='p_laiyuan']/text()").get().split()[1]
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
            title = self.get_page_title(response).split('_')[0] or xp("//h1[@id='p_biaoti']").extract_first("")
            pubtime = Pubtime(xp("//div[@id='p_laiyuan']/span[1]/text()").extract_first(""))
            content_div = xp("//div[@class='TRS_Editor']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//div[@id='p_laiyuan']/span[2]/text()").extract_first("")

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