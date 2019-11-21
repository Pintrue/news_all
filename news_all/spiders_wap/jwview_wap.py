# -*- coding: utf-8 -*-

import json
from scrapy.conf import settings
from news_all.spider_models import NewsRSpider
import jsonpath
from scrapy import FormRequest


class JwviewWapSpider(NewsRSpider):
    """中新经纬 app"""
    name = 'jwview_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        'http://jw.jwview.com/jwview/getHomeList?user=864416035963936&pageIndex=1&pageSize=20': 3699,
    # APP端-中央媒体移动端-中新经纬-新闻-要闻
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E9%AB%98%E5%B1%82&platform_chinanews=android': 3700,
    # APP端-中央媒体移动端-中新经纬-新闻-高层
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E5%AE%8F%E8%A7%82&platform_chinanews=android': 3701,
    # APP端-中央媒体移动端-中新经纬-新闻-宏观
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E9%87%91%E8%9E%8D&platform_chinanews=android': 3702,
    # APP端-中央媒体移动端-中新经纬-新闻-金融
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E9%93%B6%E8%A1%8C&platform_chinanews=android': 3703,
    # APP端-中央媒体移动端-中新经纬-新闻-银行
        'http://jw.jwview.com/jwview/getFundNewsList?pageIndex=1&pageSize=20&column=all': 3704,
    # APP端-中央媒体移动端-中新经纬-新闻-基金
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E8%82%A1%E5%B8%82&platform_chinanews=android': 3705,
    # APP端-中央媒体移动端-中新经纬-新闻-股市
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E7%90%86%E8%B4%A2&platform_chinanews=android': 3706,
    # APP端-中央媒体移动端-中新经纬-新闻-理财
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E8%A7%86%E9%A2%91&platform_chinanews=android': 3707,
    # APP端-中央媒体移动端-中新经纬-新闻-视频
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E5%9B%BE%E7%89%87&platform_chinanews=android': 3708,
    # APP端-中央媒体移动端-中新经纬-新闻-图片
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E4%BA%A7%E7%BB%8F&platform_chinanews=android': 3709,
    # APP端-中央媒体移动端-中新经纬-新闻-产经
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E6%88%BF%E4%BA%A7&platform_chinanews=android': 3710,
    # APP端-中央媒体移动端-中新经纬-新闻-房产
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E7%A7%91%E6%8A%80&platform_chinanews=android': 3711,
    # APP端-中央媒体移动端-中新经纬-新闻-科技
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E6%B1%BD%E8%BD%A6&platform_chinanews=android': 3712,
    # APP端-中央媒体移动端-中新经纬-新闻-汽车
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E6%B8%B8%E6%88%8F&platform_chinanews=android': 3713,
    # APP端-中央媒体移动端-中新经纬-新闻-游戏
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E5%8E%9F%E5%88%9B&platform_chinanews=android': 3714,
    # APP端-中央媒体移动端-中新经纬-新闻-原创
        'http://jw.jwview.com/jwview/getNewsList?user=&pageIndex=1&pageSize=20&searchType=1&channel=%E6%8E%A8%E8%8D%90&deviceId=864416035963936&zone=%E4%B8%AD%E5%9B%BD%E5%8C%97%E4%BA%AC%E5%B8%82&platform_chinanews=android': 3715,
    # APP端-中央媒体移动端-中新经纬-新闻-推荐
        'http://jw.jwview.com/jwview/getNewsList?user=864416035963936&pageIndex=1&pageSize=20&searchType=1&channel=%E8%B4%A2%E4%BA%BA&platform_chinanews=android': 3716,
    # APP端-中央媒体移动端-中新经纬-新闻-财人
        'http://jw.jwview.com/jwview/getBulletinList?user=864416035963936&isred=&pageIndex=1&pageSize=40': 3717,
    # APP端-中央媒体移动端-中新经纬-经纬快报
        'http://jw.jwview.com/jwview/getVylist?pagesize=10&page=1&type=2': 3718,  # APP端-中央媒体移动端-中新经纬-V言
        'http://jw.jwview.com/jwview/getLcarHomeNews': 3719,  # APP端-中央媒体移动端-中新经纬-直通车-企业

    }

    def parse(self, response):
        if response.url=="http://jw.jwview.com/jwview/getLcarHomeNews":
            formdata_body ={'user': '864416035963936', 'channel': 'qyzt'}
            yield FormRequest(
                url=response.url,
                formdata=formdata_body,
                method="POST",
                callback=self.parse_post,
                meta={'source_id': response.meta['source_id'],
                      
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )
        rj = json.loads(response.text)
        flashNewsList = rj.get('flashNewsList')
        newslist = rj.get('newslist')
        data = rj.get('data')
        item_list = []
        origin_name = None
        hydt = jsonpath.jsonpath(rj, '$..hydt')

        type = rj.get('type')
        if type:
            type2List= type.get('type2List')
            item_list+=type2List
        if hydt:
            hydt = hydt[0]
            item_list+=hydt

        if flashNewsList:
            item_list = flashNewsList
        if newslist:
            item_list+=newslist
        if data:
            item_list+=data
        if item_list:
            for i in item_list:
                try:
                    title = jsonpath.jsonpath(i, '$..title')[0]
                    content = jsonpath.jsonpath(i, '$..content')[0]
                    source = jsonpath.jsonpath(i, '$..source')
                    news_url = jsonpath.jsonpath(i, '$..shareUrl')[0]

                    pubtime = jsonpath.jsonpath(i, '$..pubtime')[0]
                    origin_name = source[0] if source else ""
                    if origin_name:
                        origin_name = None
                except:
                    return self.produce_debugitem(response, "json error")
                content, media, videos, cover = self.content_clean(content,kill_xpaths=['//*[starts-with(text(), "中新经纬版权所有，未经书面授权，任何单位及个人不得转载、摘编以其它方式使用")]'])

                yield self.produce_item(
                    response=response,
                    title=title,
                    pubtime=pubtime,
                    origin_name=origin_name,
                    content=content,
                    media=media,
                    srcLink=news_url
                )

    # 'http://jw.jwview.com/jwview/getLcarHomeNews',  #APP端-中央媒体移动端-中新经纬-直通车-企业
    # 该url为post请求
    def parse_post(self,response):
        rj = json.loads(response.text)

        data = rj.get("data")
        for i in data:
            try:
                title = jsonpath.jsonpath(i, '$..title')[0]
                content = jsonpath.jsonpath(i, '$..content')[0]
                source = jsonpath.jsonpath(i, '$..source')
                pubtime = jsonpath.jsonpath(i, '$..pubtime')[0]
            except:
                return self.produce_debugitem(response, "json error")
            content, media, videos, cover = self.content_clean(content)
            yield self.produce_item(
                response=response,
                title=title,
                pubtime=pubtime,
                origin_name=source[0] if source else "",
                content=content,
                videos=videos
            )
