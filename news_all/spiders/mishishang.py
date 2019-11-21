# -*- coding: utf-8 -*-
# @Time   : 2019/10/22 下午4:25
# @Author : mez
# @Project : news_all
# @FileName: mshishang_spider.py
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from news_all.tools.time_translater import Pubtime


class Mshishang(NewsRCSpider):
    name = 'mshishang'

    # 中国时尚网 ==》 补充全站采集
    mystart_urls = {
        'https://www.mshishang.com/': 5185,   #  中国时尚网
        'https://news.mshishang.com/': 5186,   #  中国时尚网
        'https://news.mshishang.com/FashionIndustry/': 5188,   #  中国时尚网
        'https://news.mshishang.com/PeopleDynamic/': 5189,   #  中国时尚网
        'https://news.mshishang.com/yule/': 5190,   #  中国时尚网
        'https://www.mshishang.com/vogue/': 5191,   #  中国时尚网
        'https://www.mshishang.com/vogue/Trend/': 5192,   #  中国时尚网
        'https://www.mshishang.com/vogue/fashion/': 5193,   #  中国时尚网
        'https://www.mshishang.com/vogue/Original/': 5194,   #  中国时尚网
        'https://www.mshishang.com/vogue/news/': 5195,   #  中国时尚网
        'https://www.mshishang.com/vogue/xiu/': 5196,   #  中国时尚网
        'https://www.mshishang.com/vogue/cdzt/': 5213,   #  中国时尚网
        'https://www.mshishang.com/vogue/cdbk/': 5215,   #  中国时尚网
        'https://www.mshishang.com/Luxury/': 5216,   #  中国时尚网
        'https://www.mshishang.com/Luxury/jewelry/': 5219,   #  中国时尚网
        'https://www.mshishang.com/Luxury/watch/': 5220,   #  中国时尚网
        'https://www.mshishang.com/Luxury/digital/': 5221,   #  中国时尚网
        'https://www.mshishang.com/Luxury/cars/': 5222,   #  中国时尚网
        'https://www.mshishang.com/Luxury/deco/': 5223,   #  中国时尚网
        'https://www.mshishang.com/Luxury/skincareperfume/': 5224,   #  中国时尚网
        'https://www.mshishang.com/Luxury/glasses/': 5226,   #  中国时尚网
        'https://www.mshishang.com/Luxury/phb/': 5227,   #  中国时尚网
        'https://mr.mshishang.com/': 5228,   #  中国时尚网
        'https://mr.mshishang.com/makeup/': 5235,   #  中国时尚网
        'https://mr.mshishang.com/hairstyle/': 5236,   #  中国时尚网
        'https://mr.mshishang.com/baike/': 5243,   #  中国时尚网
        'https://www.mshishang.com/life/': 5244,   #  中国时尚网
        'https://www.mshishang.com/life/travel/': 5250,   #  中国时尚网
        'https://www.mshishang.com/life/art/': 5252,   #  中国时尚网
        'https://www.mshishang.com/life/wiki/': 5253,   #  中国时尚网
        'https://www.mshishang.com/life/consume/': 5256,   #  中国时尚网
        'https://www.mshishang.com/life/lifezt/': 5258,   #  中国时尚网
        'https://www.mshishang.com/fshow/': 5263,   #  中国时尚网
        'https://www.mshishang.com/fshow/cnshow/': 5265,   #  中国时尚网
        'https://www.mshishang.com/fshow/blshow/': 5266,   #  中国时尚网
        'https://www.mshishang.com/fshow/nyshow/': 5267,   #  中国时尚网
        'https://www.mshishang.com/fshow/ldshow/': 5268,   #  中国时尚网
        'https://www.mshishang.com/fshow/mlshow/': 5269,   #  中国时尚网

    }

    rules = (

        # https://mr.mshishang.com/a/20191022/301479.html
        Rule(LinkExtractor(allow=r'mshishang.com/\w+/%s\d{2}/\d+\.html' % datetime.today().strftime('%Y%m'),),
             callback='parse_item',
             follow=True),

        Rule(LinkExtractor(allow=r'mshishang.com/.*?\.html', deny=(r'/201[0-8]', r'/20190[1-9]'),),
             process_request=otherurl_meta,
             follow=False),
    )


    def parse_item(self, response):
        # https://mr.mshishang.com/a/20191022/301479.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='con_t']/h1[@class='title']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//span[@class='time']/text()").extract_first())
            content_div = xp("//div[@class='content']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)  # str  list
            origin_name = xp("//span[@class='from']/text()").extract_first()# None  不要用[0]
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



