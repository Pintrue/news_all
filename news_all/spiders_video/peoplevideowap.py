# -*- coding: utf-8 -*-
from news_all.spider_models import *
from scrapy.conf import settings
from scrapy import Request
import json


class PeopleVideoWapSpider(NewsRSpider):
    '''人民视频客户端'''
    name = 'peoplevideo_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        'http://apiapp.people.cn//a/a/m/list_1_0.sjson?page=1': 3822,  # 精选
        'http://apiapp.people.cn//a/a/x/list_1_0.sjson?page=1': 3824,  # 70年
        'http://apiapp.people.cn//a/a/n/list_1_0.sjson?page=1': 3825,  # 资讯
        'http://apiapp.people.cn//a/a/ac/list_1_0.sjson?page=1': 3827,  # 政务
        'http://apiapp.people.cn//a/a/af/list_1_0.sjson?page=1': 3830,  # 生活
        'http://apiapp.people.cn//a/a/aa/list_1_0.sjson?page=1': 3833,  # v.鲁
        'http://apiapp.people.cn//a/a/z/list_1_0.sjson?page=1': 3835,  # 西藏
        'http://apiapp.people.cn//a/a/v/list_1_0.sjson?page=1': 3837,  # 影像丝路
        'http://apiapp.people.cn//a/a/e/list_1_0.sjson?page=1': 3839,  # 军事
        'http://apiapp.people.cn//a/a/h/list_1_0.sjson?page=1': 3840,  # 金台点兵
        'http://apiapp.people.cn//a/a/y/list_1_0.sjson?page=1': 3842,  # Vlog
        'http://apiapp.people.cn//a/a/j/list_1_0.sjson?page=1': 3845,  # VR
    }

    def parse(self, response):
        base_url = "http://apiapp.people.cn/"
        # print(response.text)
        rj = json.loads(response.text)
        list = rj.get("list")
        for i in list:
            contentUrl = i.get("contentUrl")
            if contentUrl:
                detail_url = base_url + contentUrl
                yield Request(
                    url=detail_url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'],
                          'start_url_time': response.meta.get('start_url_time'),
                          'schedule_time': response.meta.get('schedule_time')}
                )

    def parse_item(self, response):
        rj = json.loads(response.text)
        for i in rj:
            try:
                title = i.get("title")
                pubtime = i.get("time")
                videourl = i.get("videourl")
                videos = {'1': {'src': videourl}}
                content = '<div>#{{1}}#</div>'
            except:
                return self.produce_debugitem(response, "json error")
            yield self.produce_item(
                response=response,
                title=title,
                pubtime=pubtime,
                origin_name="人民视频",
                content=content,
                media={},
                videos=videos
            )
