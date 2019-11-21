#!/usr/bin/env python
# -*- coding:utf-8 _*-
# Time: 2019/07/25
# Author: zcy


from copy import deepcopy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider
from news_all.tools.time_translater import timestamps


class ChickenSoupSpider(NewsRCSpider):
    """心灵鸡汤"""
    name = '59xihuan_all'
    mystart_urls = {
        'http://www.59xihuan.cn/': 1120,  # 首页
        'http://www.59xihuan.cn/meiwen/': 1068,  # 人生感悟
        'http://www.59xihuan.cn/lizhi/': 1122,  # 励志一生
        'http://www.59xihuan.cn/aiqing/': 1222,  # 爱情物语
        'http://www.59xihuan.cn/yulu/': 1297,  # 经典语录
        'http://www.59xihuan.cn/zaoanxinyu/': 1315,  # 早安心语
        'http://www.59xihuan.cn/wananxinyu/': 1334,  # 晚安心语
        'http://www.59xihuan.cn/weimeidejuzi/': 1337,  # 唯美的句子
    }

    rules = (
        # Rule(LinkExtractor(allow=r'59xihuan.cn/.*?/%s/\d+.html' % datetime.today().strftime('%Y%m')),
        Rule(LinkExtractor(allow=r'59xihuan.cn/.*?/\d{6}/\d+.html'),
             callback='parse_item',
             follow=False
             ),
        Rule(LinkExtractor(allow=r'59xihuan.cn/content_\d+.html'),
             callback='parse_item',
             follow=False
             ),
    )

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//h4/text()').extract_first() or self.get_page_title(response).split('_')[0].replace(' - 心灵鸡汤、经典语录', '')
            content_div = xp('//div[@class="pic_text0" or @class="pic_text"]')[0]
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, 'xpath error')

        yield self.produce_item(
            response=response,
            title=title,
            pubtime=timestamps(),
            content=content,
            media=media
        )
