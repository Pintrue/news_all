# -*- coding: utf-8 -*-

from scrapy import Request
from news_all.spider_models import *
from scrapy.conf import settings
import requests
import json


class CctvnewsWapSpider(NewsRSpider):
    '''央视新闻'''
    name = 'cctvnews_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-9Nwml0dIB6wAxgd9EfZA160510&n1=5&version=1": 3104, # 要闻
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-9FHRlePE9rWWSViVn5tW170525&n1=1&version=1": 3105, # 联播
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-aAGEL8CK9DAN7pRRv15z190211&n1=1&version=1": 3106, # VR
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-x1EttmgGbITPUk4msBDj160812&n1=1&version=1": 3130, # V观
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-WRLNzU41eEG7G10Xflg0180117&n1=1&version=1": 3147, # 微视频
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-GxfrDirK3AR2nnyMC9Ub160812&n1=1&version=1": 3175, # 民生
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-Y7GOiDYMu0PLMSWBFJRs160812&n1=1&version=1": 3200, # 财经
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-iqwRTtNj4tQCEkyUkBzW160812&n1=1&version=1": 3213, # 国际
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-BIJQ6pPGvkbp6V9D74Gu160812&n1=1&version=1": 3214, # 夜读
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-uMt97G2SKGTYfI89PynH160812&n1=1&version=1": 3215, # 看台湾
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-D7N9jNkwGwLX5tIo7vSF161101&n1=1&version=1": 3216, # 体育
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-c9aZErstPWnzhTy9ZHTB160812&n1=1&version=1": 3218, # 军事
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-ZzGRAcda1ZRF2a2M05n9170412&n1=1&version=1": 3219, # 科技
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-90H6Ufov92Vcy2DvRPSS160812&n1=1&version=1": 3314, # 评论
        "http://api.cportal.cctv.com/api/rest/navListInfo/getHandDataInfoNew?n2=20&id=Nav-ErgjQIoOLYSQjNcC9gxO180916&n1=1&version=1": 3315, # 台风
    }

    def parse(self, response):
        # print(response.text)
        rj = json.loads(response.text)
        data = rj.get("data")
        bigImg = data.get("bigImg")
        itemList = data.get("itemList")
        itemList += bigImg
        for i in itemList:
            title = i.get("itemTitle")
            itemID = i.get('itemID')
            videoPlayID = i.get("videoPlayID")
            video_url = None
            if videoPlayID:
                video_detail = "https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=" + videoPlayID
                video_url = parse_item_list(video_detail)

            detail_url = "http://api.cportal.cctv.com/api/rest/articleInfo?id=" + itemID
            pubtime = i.get('pubDate') or i.get('operate_time')

            yield Request(
                url=detail_url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                      'video_url': video_url,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )

    def parse_item(self, response):
        try:
            result = json.loads(response.text)
            content = result.get('content') or ''
            media = {}
            if content:
                content, media, *_ = self.content_clean(content)

            origin_name = result.get('source')
            videos = None

            if response.meta.get("video_url"):
                videos = {'1': {'src': response.meta.get("video_url")}}
                content = '<div>#{{1}}#</div>' + content
            else:
                content = content

            if not content:
                photo_album_list = result.get('photo_album_list')
                # http://api.cportal.cctv.com/api/rest/articleInfo?id=ArtiyxFkEPU7leLaqtZCc7GT191024&cb=test.setMyArticalContent
                # 放弃递归解析rj.get('hotList')
                if not photo_album_list:
                    return
                content, media = self.make_img_content(photo_album_list)

        except BaseException:
            return self.produce_debugitem(response, "json error")

        return self.produce_item(
            response=response,
            title=response.meta.get("title"),
            pubtime=response.meta.get("pubtime"),
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )

    def make_img_content(self, img_cons):
        """
        拼接图、文列表为html
        """
        media = {'images': {}}
        content = ''
        for i, j in enumerate(img_cons):
            content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
            if j.get('photo_brief'):
                content += '<p>' + j['photo_brief'] + '</p>'

            media['images'][str(i + 1)] = {"src": j['photo_url']}

        return content, media


def parse_item_list(url):
    try:
        response = requests.get(url)
        rj = json.loads(response.text)
        video = rj.get("video")
        chapters2 = video.get("chapters2")[0]
        video_url = chapters2.get("url")
        return video_url
    except:
        return None