#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 17:08
# @Author  : wjq
# @File    : yicai.py

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class YicaiSpider(NewsRCSpider):
    """一财网"""
    name = 'yicai'
    mystart_urls = {
        'https://www.yicai.com/news/shijie/': 1301279,  # 一财网-世界
        'https://www.yicai.com/news/gongsi/': 1301273,  # 一财网-公司
        'https://www.yicai.com/news/hongguan/': 1301275,  # 一财网-宏观
        'https://www.yicai.com/news/': 1301280,  # 一财网-新闻
        'https://www.yicai.com/news/loushi/': 1301277,  # 一财网-楼市-左侧列表
        'https://www.yicai.com/news/automobile/': 1301282,  # 一财网-汽车
        'https://www.yicai.com/news/kechuang/': 1301281,  # 一财网-科创
        'https://www.yicai.com/news/gushi/': 1301274,  # 一财网-股市
        # 'https://www.yicai.com/video/': 1301283,  # 一财网-视听  # todo
        'https://www.yicai.com/news/comment/': 1301278,  # 一财网-评论
        'https://www.yicai.com/news/jinrong/': 1301276,  # 一财网-金融
        # 'http://www.yicai.com/news/jinrong/': 2925,  # 第一财经-金融新闻-左侧列表  重复
        'http://www.yicai.com/news/': 99130,  # 第一财经-新闻-左下列表
    }
    
    rules = (
        # https://www.yicai.com/news/100234362.html
        Rule(LinkExtractor(allow=(r'yicai.com/news/\d+.html',),
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'yicai.com.*\d+.htm',),
                           ),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            pubtime = xp('//div[@class="title f-pr"]/p/em/text()')[0].extract()
            content_div = xp('//div[@class="m-txt"]/p')
            content, media, _, _ = self.content_clean(content_div, kill_xpaths=r'//div[@class="news-edit-info"]')
        except BaseException:
            return self.produce_debugitem(response, "xpath error")
        title = self.get_page_title(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="第一财经",
            content=content,
            media=media
        )
