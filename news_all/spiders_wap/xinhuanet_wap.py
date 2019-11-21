# -*- coding: utf-8 -*-
from copy import deepcopy
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings
import json
from scrapy import Request
import jsonpath


class XinhuanetAppSipder(NewsRSpider):
    """新华网客户端"""
    name = 'xinhuanet_app'
    dd = deepcopy(settings.getdict('APP_DOWN'))
    dd['news_all.middlewares.ProxyRdMiddleware'] = 100  # 备用 使用隧道代理
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': dd}

    mystart_urls = {
        'http://api.app.xinhuanet.com/1.0/article/zhishi/list?pageNum=1&pageSize=10&device-token=14e79cd954de8e21170a8df526a65890': 2906,  # APP端-中央媒体移动端-新华网-资讯-知视
        'http://api.app.xinhuanet.com/1.0/channel/getArticlesOfSpecialChannel?channelId=14&pageSize=10&pageNum=1&device-token=14e79cd954de8e21170a8df526a65890': 2907,
    # # APP端-中央媒体移动端-新华网-资讯-听闻
        'http://api.app.xinhuanet.com/1.0/channel/getArticlesOfSpecialChannel?channelId=8&pageSize=10&pageNum=1&device-token=14e79cd954de8e21170a8df526a65890': 2908,
    # # APP端-中央媒体移动端-新华网-资讯-数据
        'http://api.app.xinhuanet.com/1.0/govPart/getAnswerList?pageNum=1&pageSize=20&device-token=14e79cd954de8e21170a8df526a65890': 2909,  # APP端-中央媒体移动端-新华网-资讯-政情
        'http://api.app.xinhuanet.com/1.0/channel/getVideoList?orderByType=0&pageNum=1&pageSize=10&device-token=14e79cd954de8e21170a8df526a65890': 2910,
    # APP端-中央媒体移动端-新华网-视频
        'http://api.app.xinhuanet.com/1.0/top10/getArticleTopVOsByType?type=2&device-token=14e79cd954de8e21170a8df526a65890': 3656,
    # APP端-中央媒体移动端-新华网-TOP10-视频
        'http://api.app.xinhuanet.com/1.0/top10/getArticleTopVOsByType?type=1&device-token=14e79cd954de8e21170a8df526a65890': 3657,
    # APP端-中央媒体移动端-新华网-TOP10-图文
        'http://api.app.xinhuanet.com/1.0/channel/getArticlesOfSpecialChannel?channelId=1&pageSize=10&pageNum=1&device-token=14e79cd954de8e21170a8df526a65890': 3678,
    # APP端-中央媒体移动端-新华网-国际
        'http://api.app.xinhuanet.com/1.0/channel/getArticlesOfSpecialChannel?channelId=2&pageSize=10&pageNum=1&device-token=14e79cd954de8e21170a8df526a65890': 3679,
    # APP端-中央媒体移动端-新华网-财经
        'http://api.app.xinhuanet.com/1.0/channel/getArticlesOfSpecialChannel?channelId=3&pageSize=10&pageNum=1&device-token=14e79cd954de8e21170a8df526a65890': 3693,
    # APP端-中央媒体移动端-新华网-军情
        'http://api.app.xinhuanet.com/1.0/channel/getArticlesOfSpecialChannel?channelId=7&pageSize=10&pageNum=1&device-token=14e79cd954de8e21170a8df526a65890': 3694,
    # APP端-中央媒体移动端-新华网-科技
        'http://api.app.xinhuanet.com/1.0/channel/getArticlesOfSpecialChannel?channelId=5&pageSize=10&pageNum=1&device-token=14e79cd954de8e21170a8df526a65890': 3695,
    # APP端-中央媒体移动端-新华网-健康
        'http://api.app.xinhuanet.com/1.0/channel/getArticlesOfSpecialChannel?channelId=6&pageSize=10&pageNum=1&device-token=14e79cd954de8e21170a8df526a65890': 3696,
    # APP端-中央媒体移动端-新华网-教育
        'http://api.app.xinhuanet.com/1.0/channel/getArticlesOfSpecialChannel?channelId=4&pageSize=10&pageNum=1&device-token=14e79cd954de8e21170a8df526a65890': 3697,
    # APP端-中央媒体移动端-新华网-汽车
        'http://api.app.xinhuanet.com/1.0/channel/getArticlesOfSpecialChannel?channelId=31&pageSize=10&pageNum=1&device-token=14e79cd954de8e21170a8df526a65890': 3698,
    # APP端-中央媒体移动端-新华网-公司头条
    }

    def parse(self, response):
        rs = json.loads(response.body)
        uuid_list = jsonpath.jsonpath(rs, '$..uuid')
        articleUuid = jsonpath.jsonpath(rs, '$..articleUuid')
        articleids = []
        if articleUuid:
            articleids+=articleUuid
        if uuid_list:
            articleids+=uuid_list
        if articleids:
            articleids = [x for x in articleids if x != '']
            for j in articleids:
                detail_url = 'http://api.app.xinhuanet.com/1.0/article/getArticleDetails?articleUuid=' + j + '&channelId=2&index=1&device-token=14e79cd954de8e21170a8df526a65890'
                yield Request(
                    url=detail_url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'],
                          
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )

    def parse_item(self, response):
        rj = json.loads(response.text)
        try:
            title = jsonpath.jsonpath(rj, '$..title')[0]
            origin_name = jsonpath.jsonpath(rj, '$..sourceName')[0]
            content_div = jsonpath.jsonpath(rj, '$..content')[0]
            video_url = jsonpath.jsonpath(rj, '$..mediaUrl')[0]
            pubtime = jsonpath.jsonpath(rj, '$..publishTime')[0]
            content, media, videos, cover = self.content_clean(content_div, need_video=True)
            if video_url:
                videos = {'1': {'src': video_url}}
                content = '<div>#{{1}}#</div>'+content

        except:
            return self.produce_debugitem(response, "json error")
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )
