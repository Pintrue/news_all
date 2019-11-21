# -*- coding: utf-8 -*-
# @Time   : 2019/7/25 上午10:05
# @Author : NewmanZhou
# @Project : news_all
# @FileName: zgsk_web.py
# @Software: PyCharm

import json
from scrapy import Request
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings


class ZGSKSpider(NewsRSpider):
    """中国社科 app"""
    name = 'zgsk_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        'http://app.cssn.cn/yaowen/documents.json': 391,  # 要闻
        'http://app.cssn.cn/guoji/documents.json': 392,  # 国际
        'http://app.cssn.cn/pinglun/documents.json': 393,  # 评论
        'http://app.cssn.cn/shipin/documents.json': 394,  # 视频
        'http://app.cssn.cn/tushu/documents.json': 395,  # 图书
        'http://app.cssn.cn/wenhua/documents.json': 397,  # 文化
        # 'http://app.cssn.cn/skysklian/documents.json' : 408,   #  高校
        'http://app.cssn.cn/skysklian/documents.json': 409,  # 社科院社科联
        'http://app.cssn.cn/dfzhi/documents.json': 411,  # 地方
        'http://app.cssn.cn/skpjia/documents.json': 413,  # 评价
    }
    
    def parse(self, response):
        rs = json.loads(response.text)
        list_datas = rs['list_datas']
        source_id = response.meta['source_id'],
        source_id = source_id[0]
        for item in list_datas:
            sharelink = item['sharelink']
            # print(sharelink)
            if sharelink:
                yield Request(sharelink, callback=self.parse_item, meta={'source_id': source_id,
                                                                         'start_url_time': response.meta.get(
                                                                             'start_url_time')})
    
    def parse_item(self, response):
        source_id = response.meta['source_id']
        xp = response.xpath
        try:
            title = xp('//h1[@class="title"]/text()').extract_first('')
            pubtime = xp('//span[@class="time"]/text()').extract_first('')
            origin_name = xp('//span[@class="source"]/text()').extract_first('')
            content_div = xp('//div[@class="article"]')[0]
            content, media, videos, video_cover = self.content_clean(content_div)
            return self.produce_item(
                response=response,
                title=title,
                pubtime=pubtime,
                origin_name=origin_name,
                content=content,
                media=media,
                videos=videos
            )
        except:
            return self.produce_debugitem(response, "xpath error")
