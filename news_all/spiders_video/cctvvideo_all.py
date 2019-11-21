# -*- coding: utf-8 -*-

import json
from scrapy import Request
from news_all.spider_models import NewsRSpider
from news_all.tools.others import to_list


class CctvVideoSpider(NewsRSpider):
    """央视新闻客户端 滚动视频"""
    name = 'cctvvideo_wap'

    mystart_urls = {
        'http://api.cportal.cctv.com/api/rest/column/getNavColumnVideoInfoNew?id=ColuSSSQbjqtPhDYENI2cfng160812&sort=allDown&version=1': 7651,
    }

    def parse(self, response):
        rj = json.loads(response.text)
        data = rj.get("data")

        bigImg=data.get("bigImg")
        itemList=data.get("itemList")
        for i in bigImg:
            itemList.append(i)

        for j in itemList:
            videoPlayID = j.get("videoPlayID")
            title = j.get("itemTitle")
            pubtime = j.get("operate_time")
            yield Request(
                url="https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid="+videoPlayID+"&client=androidapp&tsp=1561982684&vn=4&vc=3AAC8A088D8F1F6866BD24AA03F1CCEC",
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title,'pubtime':pubtime,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )

    def parse_item(self, response,only_video=False):
        pubtime = response.request.meta['pubtime']
        rj = json.loads(response.text)
        video = rj.get("video")
        origin_name = rj.get("play_channel")
        chapters4 = video.get("chapters4")[0]
        video_url = chapters4.get("url")
        image = chapters4.get("image")

        videos = {'1': {'src': video_url}}
        video_cover = to_list(image)

        if only_video:
            return videos, video_cover
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=pubtime,
            origin_name=origin_name,
            
            content='<div>#{{1}}#</div>',
            media={},
            videos=videos
        )

