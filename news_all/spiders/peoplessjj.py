#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/18 11:08
# @Author  : mez
# @File    : peoplelessjj.py

import re
from copy import deepcopy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider, otherurl_meta
from news_all.tools.time_translater import Pubtime


class Peoplespider(NewsRCSpider):
    """时事经济观察"""
    name = 'peoplessjj'
    mystart_urls = {
        'http://www.peoplessjj.com': 5147,  # 网站-中央网站-时事经济观察-时政
        'http://www.peoplessjj.com/list-38-1.html': 5148,  # 网站-中央网站-时事经济观察-图片新闻
        'http://www.peoplessjj.com/list-10-1.html': 5149,  # 网站-中央网站-时事经济观察-经济
        'http://www.peoplessjj.com/list-11-1.html': 5150,  # 网站-中央网站-时事经济观察-环境
        'http://www.peoplessjj.com/list-12-1.html': 5151,  # 网站-中央网站-时事经济观察-法治
        'http://www.peoplessjj.com/list-13-1.html': 5153,  # 网站-中央网站-时事经济观察-教育
        'http://www.peoplessjj.com/list-14-1.html': 5154,  # 网站-中央网站-时事经济观察-房产
        'http://www.peoplessjj.com/list-24-1.html': 5155,  # 网站-中央网站-时事经济观察-民生
        'http://www.peoplessjj.com/list-16-1.html': 5156,  # 网站-中央网站-时事经济观察-公益
        'http://www.peoplessjj.com/list-17-1.html': 5157,  # 网站-中央网站-时事经济观察-旅游
        'http://www.peoplessjj.com/list-18-1.html': 5158,  # 网站-中央网站-时事经济观察-扶贫攻坚
        'http://www.peoplessjj.com/list-26-1.html': 5159,  # 网站-中央网站-时事经济观察-乡村振兴
        'http://www.peoplessjj.com/list-30-1.html': 5161,  # 网站-中央网站-时事经济观察-商会
        'http://www.peoplessjj.com/list-21-1.html': 5163,  # 网站-中央网站-时事经济观察-舆情
        'http://www.peoplessjj.com/list-19-1.html': 5164,  # 网站-中央网站-时事经济观察-招商
        # 网站-中央网站-时事经济观察-律法
        'http://www.peoplessjj.com/index.php?m=content&c=index&a=lists&catid=20': 5165,
        'http://www.peoplessjj.com/list-23-1.html': 5166,  # 网站-中央网站-时事经济观察-食品
        'http://www.peoplessjj.com/list-15-1.html': 5167,  # 网站-中央网站-时事经济观察-企业
        'http://www.peoplessjj.com/list-29-1.html': 5168,  # 网站-中央网站-时事经济观察-娱乐
        'http://www.peoplessjj.com/list-28-1.html': 5176,  # 网站-中央网站-时事经济观察-网评
        # 网站-中央网站-时事经济观察-综合
        'http://www.peoplessjj.com/index.php?m=content&c=index&a=lists&catid=22': 5177,
        'http://www.peoplessjj.com/list-31-1.html': 5179,  # 网站-中央网站-时事经济观察-百姓呼声
        'http://www.peoplessjj.com/list-25-1.html': 5180,  # 网站-中央网站-时事经济观察-医疗健康
        # 网站-中央网站-时事经济观察-图库
        'http://www.peoplessjj.com/index.php?m=content&c=index&a=lists&catid=39': 5182,
    }
    custom_settings = {
        # 禁止重定向
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    rules = (
        # http://www.peoplessjj.com/show-12-13143-1.html'
        # http://www.peoplessjj.com/index.php?m=content&c=index&a=show&catid=22&id=13113
        # http://www.peoplessjj.com/index.php?m=content&c=index&a=show&catid=22&id=13098
        # http://www.peoplessjj.com/index.php?m=content&c=index&a=show&catid=22&id=9126

        Rule(LinkExtractor(allow=(r'peoplessjj.com/show-\d{1,3}\-\d+\-\d+\.html',),
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'http://www.peoplessjj.com/index\.php\?.*?\&a=show&catid=\d{2}\&id=\d+',),
                           ),
             callback='parse_item', follow=False),

        # 防止正则覆盖不全
        Rule(LinkExtractor(allow=(r'peoplessjj.com.*?\d+\.html?',), deny='peoplessjj.com/list'
                           ),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        # http://www.peoplessjj.com/show-9-13145-1.html
        xp = response.xpath
        try:
            title = xp("//div[@class='title']/h1/text()").extract_first(
            ) or re.split(r'-|_', self.get_page_title(response))[0]
            pubtime = Pubtime(xp("//div[@class='resource']").extract_first())
            content_div = xp("//div[@class='content']")[0]
            content, media, videos, _ = self.content_clean(content_div, need_video=True, kill_xpaths=[
                "//div[@class='content']/b/font"], )  # str  list
        except BaseException:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media,
            videos=videos,
        )
