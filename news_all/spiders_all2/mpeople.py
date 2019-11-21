# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider


class MpeopleAllSpider(NewsRCSpider):
    name = 'mpeople_all'

    mystart_urls = {
        'http://m.people.cn/35/index.html': 1000205,  # 手机人民网-体育
        'http://m.people.cn/24/index.html': 1000201,  # 手机人民网-军事-全部
        'http://m.people.cn/36/677/index.html': 1000208,  # 手机人民网-历史
        'http://m.people.cn/32/index.html': 1000209,  # 手机人民网-娱乐
        'http://m.people.cn/901/index.html': 1000210,  # 手机人民网-房产
        'http://m.people.cn/33/index.html': 1000206,  # 手机人民网-时尚
        'http://m.people.cn/29/index.html': 1000203,  # 手机人民网-汽车
        'http://m.people.cn/28/index.html': 1000204,  # 手机人民网-科技
        'http://m.people.cn/26/index.html': 1000202,  # 手机人民网-财经
        'http://m.people.cn/': 1000200,  # 手机人民网-首页


    }

    # http://m.people.cn/n4/2019/0619/c131-12845109.html    http://m.people.cn/n4/2019/0619/c35-12843208.html
    rules = (
        Rule(LinkExtractor(allow=r'm.people.cn/n4/%s/.*?\d+.html' % datetime.today().strftime('%Y'),
                           deny='video', ), callback='parse_item',
             follow=False),
    )

    custom_settings = {
        # 'DEPTH_LIMIT': 3,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    def parse_item(self, response):
        # https://sports.dbw.cn/system/2019/06/17/058217425.shtml
        
        xp = response.xpath
        try:
            title = xp('//h1').extract()[0]
            content_div = xp('//div[@id="p_content"]')[0]
            source = xp('//html/head/meta[@name="source"]/@content')[0].extract()
            pubtime = xp('//html/head/meta[@name="publishdate"]/@content')[0].extract()
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(response=response,  # 一定要写response=response, 不能是response
                                 title=title,
                                 pubtime=pubtime,
                                 origin_name=source,
                                 content=content,
                                 media=media,
                                 )

