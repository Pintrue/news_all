# -*- coding: utf-8 -*-
# @Time   : 2019/11/11 下午4:25
# @Author : mez
# @Project : news_all
# @FileName: aili_spider.py
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from copy import deepcopy
from scrapy.conf import settings
from datetime import datetime
from news_all.tools.time_translater import Pubtime


class Aili(NewsRCSpider):
    name = 'aili'

    # 爱丽时尚网 ==》 补充全站采集
    mystart_urls = {
        'http://www.aili.com/': 1,   #  爱丽时尚网
        'http://fashion.aili.com/': 2,   #  爱丽时尚网
        'http://fashion.aili.com/inside/': 3,   #  爱丽时尚网
        'http://fashion.aili.com/style/': 4,   #  爱丽时尚网
        'http://fashion.aili.com/gossip/': 5,   #  爱丽时尚网
        'http://fashion.aili.com/new/': 6,   #  爱丽时尚网
        'http://fashion.aili.com/brand/': 7,   #  爱丽时尚网
        'http://feature.aili.com/beauty/': 8,   #  爱丽时尚网
        'http://beauty.aili.com/': 9,   #  爱丽时尚网
        'http://beauty.aili.com/skincare/': 10,   #  爱丽时尚网
        'http://beauty.aili.com/color/': 11,   #  爱丽时尚网
        'http://beauty.aili.com/hair/': 12,   #  爱丽时尚网
        'http://beauty.aili.com/perfume/': 13,   #  爱丽时尚网
        'http://beauty.aili.com/news/': 14,   #  爱丽时尚网
        'http://beauty.aili.com/perfumenew/': 15,   #  爱丽时尚网
        'http://watch.aili.com/': 16,   #  爱丽时尚网
        'http://watch.aili.com/newarriva/': 17,   #  爱丽时尚网
        'http://watch.aili.com/timepiece/': 18,   #  爱丽时尚网
        'http://watch.aili.com/whatbuy/': 19,   #  爱丽时尚网
        'http://ent.aili.com/': 20,   #  爱丽时尚网
        'http://ent.aili.com/baguaxingwen/': 21,   #  爱丽时尚网
        'http://ent.aili.com/bangyangrenwu/': 22,   #  爱丽时尚网
        'http://ent.aili.com/remenzongyi/': 23,   #  爱丽时尚网
        'http://ent.aili.com/teyueyingping/': 24,   #  爱丽时尚网
        'http://lifestyle.aili.com/': 25,   #  爱丽时尚网
        'http://lifestyle.aili.com/lolpet/': 26,   #  爱丽时尚网
        'http://lifestyle.aili.com/lomeish/': 27,   #  爱丽时尚网
        'http://auto.aili.com/': 28,   #  爱丽时尚网
        'http://auto.aili.com/woxuanwoche/': 29,   #  爱丽时尚网
        'http://digi.aili.com/': 30,   #  爱丽时尚网
        'http://digi.aili.com/shouji/': 31,   #  爱丽时尚网
        'http://digi.aili.com/yingxiang/': 32,   #  爱丽时尚网
        'http://digi.aili.com/chuandai/': 33,   #  爱丽时尚网
        'http://digi.aili.com/wanwukong/': 34,   #  爱丽时尚网

    }
    custom_settings = {
        'DEPTH_LIMIT': 0,
        # 禁止重定向
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    rules = (
        # http://ent.aili.com/2789/2818731.html
        # http://auto.aili.com/2397/2713235p.html
        Rule(LinkExtractor(allow=r'.aili.com/\d+/\w+\.html',),
             callback='parse_item',
             follow=False),

        Rule(LinkExtractor(allow=r'.aili.com/.*?\.html',),
             process_request=otherurl_meta,
             follow=False),
    )


    def parse_item(self, response):
        # http://ent.aili.com/2789/2818731.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//h1[@class='zarticle_title']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = xp("//div[@class='zfrom fl']/text()").get()
            content_div = xp("//div[@id='icontent']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False,)  # str  list
            origin_name = xp("//a[@class='zfrom_link']/text()").extract_first()  # None  不要用[0]
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")
        next_a = xp('.//a[contains(text(), "下一页")]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'origin_name': origin_name,
                                         'content': content_div.extract(), 'title': title,
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         })

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,

        )

    def parse_page(self, response):
        meta_new = deepcopy(response.meta)
        xp = response.xpath
        try:
            content_div = xp("//div[@id='icontent']")[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()
        next_a = xp('.//a[contains(text(), "下一页")]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
        content, media, videos, video_cover = self.content_clean(meta_new['content'],
                                                                 kill_xpaths=['//h2[@class="mBqSm"]'])
        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),
            content=content,
            media=media
        )



