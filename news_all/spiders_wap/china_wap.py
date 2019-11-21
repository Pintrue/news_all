#!/usr/bin/env python
# -*- coding:utf-8 _*-
# Time: 2019/07/17
# Author: zcy
import re
from news_all.spider_models import *
from scrapy.conf import settings
import json
from scrapy import Request

img_pattern = re.compile(r'''<img.*?data-original=['"](.*?)['"].*?>''')


class ChinaAppSipder(NewsRSpider):
    """中国网"""
    name = 'china_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}

    mystart_urls_base = {
        'https://k1.m.china.com.cn/scene/query/list?columnId=6&page=%d&size=20': 3046,  # 观点
        'https://k1.m.china.com.cn/scene/query/list?columnId=18&page=%d&size=20': 3047,  # 国际
        'https://k1.m.china.com.cn/scene/query/list?columnId=8&page=%d&size=20': 3048,  # 军事
        'https://k1.m.china.com.cn/scene/query/list?columnId=11&page=%d&size=20': 3049,  # 财经
        'https://k1.m.china.com.cn/scene/query/list?columnId=9&page=%d&size=20': 3050,  # 旅游
        'https://k1.m.china.com.cn/scene/query/list?columnId=20&page=%d&size=20': 3051,  # 社会
        'https://k1.m.china.com.cn/scene/query/list?columnId=3785&page=%d&size=20': 3052,  # 政协
        'https://k1.m.china.com.cn/scene/query/list?columnId=10&page=%d&size=20': 3053,  # 艺术
        'https://k1.m.china.com.cn/app/article/cnumber/list?columnId=13234&page=%d&size=20': 3054,  # 中国3分钟
        'https://k1.m.china.com.cn/app/article/cnumber/list?columnId=13229&page=%d&size=20': 3055,  # 世相
        'https://k1.m.china.com.cn/app/article/list?columnId=832668&page=%d&size=20': 3056,  # 中国暖
        'https://m.china.com.cn//app/chinahao.do?columnId=764318&page=%d&size=20': 3057,  # 他说中国
        'https://k1.m.china.com.cn/scene/query/list?columnId=14&page=%d&size=20': 3058,  # 科技
        'https://k1.m.china.com.cn/scene/query/list?columnId=34&page=%d&size=20': 3059,  # 图片
        'https://k1.m.china.com.cn/scene/query/list?columnId=2446&page=%d&size=20': 3060,  # 汽车
        'https://k1.m.china.com.cn/scene/query/list?columnId=15&page=%d&size=20': 3061,  # 体育
        'https://k1.m.china.com.cn/scene/query/list?columnId=28&page=%d&size=20': 3062,  # 生态
        'https://m.china.com.cn/app/newslist.do?columnId=12&page=%d&size=20': 3063,  # 教育
        'https://m.china.com.cn/app/newslist.do?columnId=29&page=%d&size=20': 3064,  # 娱乐
        'https://k1.m.china.com.cn/scene/query/list?columnId=100000006&page=%d&size=20': 3065,  # 国新办
        'https://k1.m.china.com.cn/scene/query/list?columnId=100000014&page=%d&size=20': 3066,  # 国务院
        'https://k1.m.china.com.cn/scene/query/list?columnId=100000013&page=%d&size=20': 3067,  # 全国人大
        'https://k1.m.china.com.cn/scene/query/list?columnId=100000007&page=%d&size=20': 3068,  # 部委办
        'https://k1.m.china.com.cn/scene/query/list?columnId=100000011&page=%d&size=20': 3069,  # 国台办
        'https://k1.m.china.com.cn/scene/query/list?columnId=100000012&page=%d&size=20': 3070,  # 科研院所
        'https://k1.m.china.com.cn/scene/query/list?columnId=100000015&page=%d&size=20': 3071,  # 会议活动
    }
    mystart_urls = {}

    for page in range(0, 4):
        for i, j in mystart_urls_base.items():
            mystart_urls[i % page] = j

    def parse(self, response):
        rs = json.loads(response.body)
        result_list = rs.get('list')

        for result in result_list:
            if result.get('title') == '置顶' or result.get('title') == '我要入驻':
                continue

            yield Request(
                url=result.get('artUrl'),
                callback=self.parse_item,
                meta={
                    'title': result.get('title'),
                    'pubtime': result.get('pubTime'),
                    'origin_name': result.get('sourceName'),
                    'videos': result.get('videoUrl'),
                    'source_id': response.meta['source_id'],
                    'start_url_time': response.meta.get('start_url_time'),
                    'schedule_time': response.meta.get('schedule_time')
                }
            )

    def parse_item(self, response):
        url = response.url
        if re.match('.*live.*', url):  # 去掉直播分区
            return self.produce_debugitem(response, 'live filter')
        video_url = response.meta['videos']
        videos = None
        if video_url:
            videos = {'1': {'src': video_url}}

        xp = response.xpath
        if xp('//body/text()').extract_first() is None:
            return  # http://m.china.com.cn/opinion_213772_artUrl.html?lm=1567296821000

        content_div = xp('//div[@class="content contentBody"]')

        content, media, _, _ = self.content_clean(content_div, img_re=img_pattern,
                                                  kill_xpaths=['//*[re:match(text(),"版权所有 中国互联网新闻中心")]',
                                                               '//*[re:match(text(),"京公网安备110108006329号")]',
                                                               '//div[contains(text(), "当前位置： >")]',
                                                               # 注意这里要写html实际符号>不要写&gt;
                                                               '//dl[1]'
                                                               ])

        return self.produce_item(
            response=response,
            title=response.meta.get('title'),
            pubtime=response.meta.get('pubtime') or xp("//span[@id='title_time']/text()").extract_first('').strip(),
            origin_name=response.meta.get('origin_name'),
            content=content,
            media=media,
            videos=videos
        )
