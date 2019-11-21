#!/usr/bin/env python 
# -*- coding:utf-8 _*-  
# Time: 2019/08/21
# Author: zcy
from copy import deepcopy
from scrapy.conf import settings
from news_all.spider_models import *
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.tools.time_translater import timestamps

mystart_urls_base = {
    'https://www.qiushibaike.com/8hr/page/%s/': 3803,  # 热门
    'https://www.qiushibaike.com/hot/page/%s/': 3805,  # 24小时
    'https://www.qiushibaike.com/imgrank/page/%s/': 3806,  # 热图
    'https://www.qiushibaike.com/text/page/%s/': 3807,  # 文字
    'https://www.qiushibaike.com/history/page/%s': 3810,  # 穿越
    'https://www.qiushibaike.com/pic/page/%s/': 3811,  # 糗图
    'https://www.qiushibaike.com/textnew/page/%s/': 3813,  # 新鲜
}


class QsbkSpider(NewsRCSpider):
    """糗事百科"""
    name = 'qsbk_all'

    # todo why 有少量详情页加载慢 打开浏览器弹出验证码
    dd = deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES'))
    dd['news_all.middlewares.ProxyRdMiddleware'] = 100
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': dd,
        'RETRY_TIMES': 5,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1
    }

    mystart_urls = {i % p: j for p in range(1, 14) for i, j in mystart_urls_base.items()}

    rules = (
        Rule(LinkExtractor(allow=(r'qiushibaike.com/article/\d+')),
             callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//h1[@class="article-title"]/text()').extract_first('') or self.get_page_title(
                response).replace('- 糗事百科', '')
            c1 = xp('//div[@id="single-next-link"]').extract()
            c2 = xp('//video[@id="article-video"]').extract()
            # 删除表情符号
            content, media, videos, _ = self.content_clean(c1 + c2, need_video=True, video_prefix=response.url,
                                                           kill_xpaths='//img[contains(@src, "static.qiushibaike.com/static/images/emoji/")]')

        except:
            return self.produce_debugitem(response, 'xpath error')

        return self.produce_item(
            response=response,
            title=title,
            pubtime=timestamps(),
            content=content,
            media=media,
            videos=videos
        )
