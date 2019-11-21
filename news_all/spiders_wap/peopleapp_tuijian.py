# -*- coding: utf-8 -*-
__author__ = 'zwl'

from scrapy.conf import settings
import json
from scrapy import Request
from news_all.spider_models import NewsRSpider
from hashlib import md5


def make_img_content(img_cons):
    """拼接json 中图、文列表为html
    :param img_cons list
    """
    media = {'images': {}}
    content = ''
    for i, j in enumerate(img_cons):
        content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
        media['images'][str(i + 1)] = {"src": j['url']}

        if j['desc']:
            content += '<p>' + j['desc'] + '</p>'
    return content, media


class PeopleAppTjSpider(NewsRSpider):
    name = 'peopleapp_tuijian'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        "https://app.peopleapp.com/Api/700/HomeApi/getContentList": 5146,  # "推荐"
    }
    start_formdata_map ={
        5146:(
            "推荐",
            {
                "category_id":"234",
                "channel":"app store",
                "device":"0C6656C1-E89D-4A35-AD45-B0BEA815171D",
                "device_model":"iPhone",
                "device_os":"iOS 12.4.1",
                "device_product":"苹果",
                "device_size":"828*1792",
                "device_type":"2",
                "fake_id":"23202495",
                "id":"rmh7635800",
                "image_height":"828",
                "image_wide": "1792",
                "interface_code": "700",
                "ios_version_code": "14751",
                "latitude":"",
                "longitude":"",
                "page": "-18",
                "refresh_ids": "",
                "refresh_tag": "0",
                "refresh_time": "",
                "securitykey": "1b9bdf7bea4460cf6cef69f81e7c8dfc",
                "show_num":"20",
                "update_time": "0",
                "userId": "0",
                "user_gov_id":"",
                "version": "7.0.0"
            }
        )
    }
    start_method = 'POST'

    def md5_encrypt(self, str_input):  # 'id=4605188|interface_code=610rbk#$cd2e24e6cf68b7bc6fbbaede395'
        m5 = md5()
        m5.update(str_input.encode(encoding='utf8'))
        return m5.hexdigest()

    def parse(self, response):
        json_body = json.loads(response.body)
        datas = json_body.get("data", {})
        for data in datas:
            id = data.get("id")
            newsurl = data.get("share_url")
            securitykey_md5 = "id={}|interface_code=610rbk#$cd2e24e6cf68b7bc6fbbaede395".format(id)
            securitykey = self.md5_encrypt(securitykey_md5)
            url = "https://app.peopleapp.com/WapApi/610/ArtInfoApi/getInfoUp?id={}&securitykey={}&interface_code=610".format(id, securitykey)
            meta = {
                'source_id': response.meta['source_id'],
                'newsurl':newsurl,
                'start_url_time': response.meta.get('start_url_time'),
                'schedule_time': response.meta.get('schedule_time')
            }
            yield Request(
                url=url,
                meta=meta,
                callback=self.parse_item,
            )

    def parse_item(self, response):
        json_body = json.loads(response.body)
        try:
            data = json_body.get("data", {})
            title = data.get("title")
            newsurl = response.meta.get('newsurl')
            pubtime = data.get('news_datetime')
            origin_name =data.get('copyfrom')
            content_div = data.get("contents")
            video_url = data.get('video_url')
            if not content_div:
                if video_url:
                    videos = {'1': {'src': video_url}}
                    content = '<div>#{{1}}#</div>'
                    media = {}
                else:
                    img_cons = data.get('image')  # 'view_type': 'img'
                    if not img_cons:
                        return self.produce_debugitem(response, "json error")
                    content, media = make_img_content(img_cons)
                    videos = None

            else:
                content, media, videos, video_cover = self.content_clean(content_div, need_video=True, kill_xpaths=[])
                # https://app.peopleapp.com/WapApi/610/ArtInfoApi/getInfoUp?id=rmh7669210&securitykey=4270e3b10ed32ed74bbcaa5a9d278406&interface_code=610
                if video_url and not videos:
                    videos = {'1': {'src': video_url}}

        except:
            return self.produce_debugitem(response, "json error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,
            srcLink=newsurl + '或' + response.url if newsurl else response.url
        )