# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider
from news_all.tools.time_translater import Pubtime


class DdxfwSpider(NewsRCSpider):
    '''当代先锋网'''
    name = 'ddxfw'
    allowed_domains = ["ddcpc.cn"]
    mystart_urls = {
        'http://www.ddcpc.cn/gy/': 1301139,  # 当代先锋网 公益-列表-左侧列表
        'http://www.ddcpc.cn/yt/': 1301147,  # 当代先锋网 娱体-列表
        'http://www.ddcpc.cn/znl/': 1301146,  # 当代先锋网 政能量-左侧列表
        'http://www.ddcpc.cn/jy/': 1301137,  # 当代先锋网 教育-列表-首屏和新闻排行区域
        'http://www.ddcpc.cn/ly/': 1301355,  # 当代先锋网 旅游-列表-头条及图集右侧列表
        'http://www.ddcpc.cn/ss/': 1301142,  # 当代先锋网 时尚-列表
        'http://www.ddcpc.cn/sh/': 1301140,  # 当代先锋网 社会-列表
        'http://www.ddcpc.cn/ms/': 1301144,  # 当代先锋网 美食-列表
        'http://www.ddcpc.cn/tpgj/': 1301141,  # 当代先锋网 脱贫攻坚-列表
        'http://www.ddcpc.cn/news/': 1301145,  # 当代先锋网 要闻-列表-首屏区域
        'http://www.ddcpc.cn/gd/': 1301143,  # 当代先锋网 观点
    }
    rules = (
        # http://www.ddcpc.cn/gy/201906/t20190624_502620.shtml?spm=zm1040-001.0.0.1.hrqS5P&file=t20190624_502620.shtml
        # http://www.ddcpc.cn/jy/201812/t20181228_342575.shtml
        Rule(LinkExtractor(
            allow=(r'ddcpc.cn/[a-z]+/\d{6}/t%s\d{2}_\d{6}\.s?html.*?' % datetime.today().strftime('%Y%m')),
            deny='/newvideo/'), callback='parse_item',  # todo 解析腾讯视频
            follow=False),
    )

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))  # 禁止重定向
    }

    def parse_item(self, response):
        xp = response.xpath
        if xp('//script[contains(text(), "window.location.replace")]'):
            return
        try:
            title = xp("//div[@class='center text_title']/h1/text()").extract_first()
            content_div = xp("//div[@class='detail']")[0]
            pubtime = xp("//div[@class='fl']/text()").extract()[1].replace('发布时间：', '').strip()
            origin_name = xp("//div[@class='fl']/a/text()").extract_first()
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_2(self, response):
        # http://www.ddcpc.cn/yt/201808/t20180821_200951.shtml
        xp = response.xpath
        try:
            title = xp("//header[@class='news-basic']/h1/text()").extract_first()
            content_div = xp("//section[@class='main-text-container']")[0]
            pubtime = xp("//p[@class='s-sub-sub']/text()").extract_first().strip()
            origin_name = xp("//p[@class='source']/text()").extract_first()
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_3(self, response):
        # http://www.ddcpc.cn/news/201910/t20191024_655684.shtml
        xp = response.xpath
        try:
            title = xp("//h3[@class='detail-title-content']/text()").extract_first()
            content_div = xp("//div[@class='detail-content']")[0]
            pubtime = Pubtime(xp("//li[@class='detail-title-sum-last']/span/text()").extract_first(''))
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media
        )
