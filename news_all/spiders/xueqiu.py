# -*- coding: utf-8 -*-
# @Time   : 2019/11/11 下午4:25
# @Author : mez
# @Project : news_all
# @FileName: xueqiu_spider.py
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta

class Xueqiu(NewsRCSpider):
    name = 'xueqiu'

    # 雪球网 ==》 补充全站采集
    mystart_urls = {
        'https://xueqiu.com/': 1,   #  雪球网
        'https://xueqiu.com/?category=all': 2,   #  雪球网
        'https://xueqiu.com/?category=livenews': 3,   #  雪球网
        'https://xueqiu.com/?category=cn': 4,   #  雪球网
        'https://xueqiu.com/?category=tech_board': 5,   #  雪球网
        'https://xueqiu.com/?category=hk': 6,   #  雪球网
        'https://xueqiu.com/?category=financial_management': 7,   #  雪球网
        'https://xueqiu.com/?category=us': 8,   #  雪球网
        'https://xueqiu.com/?category=property': 9,   #  雪球网
        'https://xueqiu.com/?category=private_fund': 10,   #  雪球网
        'https://xueqiu.com/?category=car': 11,   #  雪球网
        'https://xueqiu.com/?category=insurance': 12,   #  雪球网
        'https://xueqiu.com/today': 13,   #  雪球网
        'https://xueqiu.com/today#/livenews': 14,   #  雪球网
        'https://xueqiu.com/today#/cn': 15,   #  雪球网
        'https://xueqiu.com/today#/tech_board': 16,   #  雪球网
        'https://xueqiu.com/today#/hk': 17,   #  雪球网
        'https://xueqiu.com/today#/financial_management': 18,   #  雪球网
        'https://xueqiu.com/today#/us': 19,   #  雪球网
        'https://xueqiu.com/today#/property': 20,   #  雪球网
        'https://xueqiu.com/today#/private_fund': 21,   #  雪球网
        'https://xueqiu.com/today#/car': 22,   #  雪球网
        'https://xueqiu.com/today#/insurance': 23,   #  雪球网
        'https://xueqiu.com/people': 24,   #  雪球网
        'https://xueqiu.com/ask/square': 25,   #  雪球网
        'https://xueqiu.com/ask/square/offer': 26,   #  雪球网
        'https://xueqiu.com/hq': 27,   #  雪球网
        'https://xueqiu.com/hq#exchange=CN&firstName=1&secondName=1_0': 28,   #  雪球网
        'https://xueqiu.com/hq#exchange=CN&type=kcb&firstName=%E7%A7%91%E5%88%9B%E6%9D%BF': 29,   #  雪球网
        'https://xueqiu.com/hq#xgss': 30,   #  雪球网
        'https://xueqiu.com/hq#LHB': 31,   #  雪球网
        'https://xueqiu.com/hq#AH': 32,   #  雪球网
        'https://xueqiu.com/hq/insider': 33,   #  雪球网
        'https://xueqiu.com/f/home?insider=1': 34,   #  雪球网
        'https://xueqiu.com/f/rank': 35,   #  雪球网
        'https://xueqiu.com/f/home/fof': 36,   #  雪球网
        'https://xueqiu.com/f/home/ugc': 37,   #  雪球网
        'https://xueqiu.com/hq/screener': 38,   #  雪球网
        'https://xueqiu.com/p/discover': 39,   #  雪球网

    }

    rules = (

        # https://xueqiu.com/6146592061/135519381
        Rule(LinkExtractor(allow=r'xueqiu.com/\d+/\d+',),
             callback='parse_item',
             follow=True),

        Rule(LinkExtractor(allow=r'xueqiu.com/.*?',),
             process_request=otherurl_meta,
             follow=False),
    )


    def parse_item(self, response):
        # https://xueqiu.com/1541753132/135507506
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//h1[@class='article__bd__title']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            # 发布于11-10 16:30
            try:
                pubtime = xp("//a[@class='time']/text()").extract_first().replace('发布于', '')

            except:
                pubtime = xp("//a[@class='edit-time']/text()").get().replace('修改于','')

            content_div = xp("//div[@class='article__bd__detail']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)  # str  list
            origin_name = xp("//div[@class='article__bd__from']/a/text()").extract_first()# None  不要用[0]
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,

        )



