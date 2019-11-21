# -*- coding: utf-8 -*-

import json
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings
from news_all.tools.time_translater import timestamps


class QmagxAppSpider(NewsRSpider):
    '''全民爱搞笑'''
    name = 'qmagx_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}

    mystart_urls = {
        "https://api.gaoxiaoapp.com/api/v30/get_gaoxiao_list?since_id=0&type=0&page=1&title=%E6%8E%A8%E8%8D%90&platform=android&device_brand=HONOR&device_system_model=PCT-AL10&device_system_version=9&uuid=860087042314522": 3808,
        # APP端-垂直媒体移动端-全民爱搞笑-推荐
        "https://api.gaoxiaoapp.com/api/v30/get_gaoxiao_list?since_id=0&type=1&page=1&title=%E8%A7%86%E9%A2%91&platform=android&device_brand=HONOR&device_system_model=PCT-AL10&device_system_version=9&uuid=860087042314522": 3809,
        # APP端-垂直媒体移动端-全民爱搞笑-视频
        "https://api.gaoxiaoapp.com/api/v30/get_gaoxiao_list?since_id=0&type=2&page=1&title=%E5%9B%BE%E7%89%87&platform=android&device_brand=HONOR&device_system_model=PCT-AL10&device_system_version=9&uuid=860087042314522": 3812,
        # APP端-垂直媒体移动端-全民爱搞笑-图片
        "https://api.gaoxiaoapp.com/api/v30/get_gaoxiao_list?since_id=0&type=3&page=1&title=%E6%AE%B5%E5%AD%90&platform=android&device_brand=HONOR&device_system_model=PCT-AL10&device_system_version=9&uuid=860087042314522": 3814,
        # APP端-垂直媒体移动端-全民爱搞笑-段子
    }

    def parse(self, response):
        result = json.loads(response.text)
        data1 = result.get("data")
        data2 = data1.get("data")

        for data in data2:
            # pubtime = data.get("time")
            user = data.get("user")
            origin_name = user.get("nickname")
            title = data.get("text")[:16] + '...'
            content = data.get("text")
            video_list = data.get("video_list")
            video_url = ''
            for video in video_list:
                video_url = video.get("video_url")
            videos = {'1': {'src': video_url}}
            content = '<div>#{{1}}#</div>' + content
            if not video_url:
                print()

            yield self.produce_item(
                response=response,
                title=title,
                pubtime=timestamps(),
                origin_name=origin_name,
                content=content,
                media={},
                videos=videos,
                srcLink=video_url
            )

