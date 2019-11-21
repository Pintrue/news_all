#-*- coding:utf-8 -*-
# @Time    : 2019/7/11 17:08
# @Author  : zxy
# @File    : cankaoxiaoxi_wap.py

import json
from scrapy import Request
from bs4 import BeautifulSoup
from scrapy.conf import settings
from news_all.spider_models import NewsRSpider


class CankaoxiaoxiSpider(NewsRSpider):
    chinese_name = """参考消息新闻app"""
    name = 'cankao_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {                                                                                                                                                                                                             
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=devie_id&ip=172.16.2.15&type=android&pagesize=20&menuid=1&page=1":3655,                 #新闻-首页
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=device_id&ip=172.16.2.15&type=android&page=1&pagesize=20&menuid=21":3370,
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=device_id&ip=172.16.2.15&type=android&page=1&pagesize=20&menuid=22":3371,
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=device_id&ip=172.16.2.15&type=android&page=1&pagesize=20&menuid=13":3372,
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=device_id&ip=172.16.2.15&type=android&page=1&pagesize=20&menuid=23":3373,
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=device_id&ip=172.16.2.15&type=android&page=1&pagesize=20&menuid=39":3374,
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=device_id&ip=172.16.2.15&type=android&page=1&pagesize=20&menuid=38":3375,
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=device_id&ip=172.16.2.15&type=android&page=1&pagesize=20&menuid=24":3376,
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=device_id&ip=172.16.2.15&type=android&page=1&pagesize=20&menuid=33":3377,
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=device_id&ip=172.16.2.15&type=android&page=1&pagesize=20&menuid=25":3378,
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=device_id&ip=172.16.2.15&type=android&page=1&pagesize=20&menuid=9":3379,
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=device_id&ip=172.16.2.15&type=android&page=1&pagesize=20&menuid=26":3380,
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=device_id&ip=172.16.2.15&type=android&page=1&pagesize=20&menuid=8":3381,
                    "http://m.api.ckxx.net/v2/menudata?sign=sign&time=time&siteid=10001&clientid=1&modules=common:2&thumbrate=2&device_id=device_id&ip=172.16.2.15&type=android&page=1&pagesize=20&menuid=112":3382,
                    "http://m.api.ckxx.net/v2/subscribe?sign=sign&time=time&siteid=10001&clientid=1&modules=common:1&sid=16&device_id=device_id&memberid=&ip=172.16.2.15&type=android&categoryid=&page=1&pagesize=20":3383,
                    "http://m.api.ckxx.net/v2/subscribe?sign=sign&time=time&siteid=10001&clientid=1&modules=common:1&sid=8&device_id=device_id&memberid=&ip=172.16.2.15&type=android&categoryid=&page=1&pagesize=20":3384,
                    "http://m.api.ckxx.net/v2/subscribe?sign=sign&time=time&siteid=10001&clientid=1&modules=common:1&sid=20&device_id=device_id&memberid=&ip=172.16.2.15&type=android&categoryid=&page=1&pagesize=20":3385,
                    "http://m.api.ckxx.net/v2/subscribe?sign=sign&time=time&siteid=10001&clientid=1&modules=common:1&sid=23&device_id=device_id&memberid=&ip=172.16.2.15&type=android&categoryid=&page=1&pagesize=20":3386,
                    "http://m.api.ckxx.net/v2/subscribe?sign=sign&time=time&siteid=10001&clientid=1&modules=common:1&sid=27&device_id=device_id&memberid=&ip=172.16.2.15&type=android&categoryid=&page=1&pagesize=20":3387,
                    "http://m.api.ckxx.net/v2/subscribe?sign=sign&time=time&siteid=10001&clientid=1&modules=common:1&sid=29&device_id=device_id&memberid=&ip=172.16.2.15&type=android&categoryid=&page=1&pagesize=20":3388,
                    }   
    base_api = 'http://m.api.ckxx.net/v2/article?clientid=1&device_id=device_id&ip=local_host&system_name=android&contentid={}&sign=xxxxx&siteid=10001&time=time&type=android&styleblack=0&modules=common%3A2'    
    gallery_api = 'http://m.api.ckxx.net/v2/gallery?clientid=1&device_id=device_id&ip=local_host&system_name=android&contentid={}&sign=xxxxx&siteid=10001&time=time&type=android&modules=common%3A1'

    def parse(self, response):
        rs = json.loads(response.text)
        data = rs.get('data', {}).get("common", {}).get("list")
        if rs.get('state') != True or not isinstance(data, dict):
            return self.produce_debugitem(response, 'json error')
        for art_data in data.get('lists', []):
            content_id = art_data.get('contentid')
            if not content_id:
                print('have not contentid')
                continue
            news_url = self.base_api.format(content_id)

            title = art_data.get('title')
            origin_name = art_data.get("source")
            meta = {'source_id': response.meta['source_id'], 
                  'title': title,
                  'origin_name': origin_name,
                  'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}

            thumb_view = art_data.get("thumbs_view_count", None)
            if thumb_view is None:
                yield Request(
                    url=news_url,
                    headers=self.start_headers,
                    callback=self.parse_item,
                    meta=meta)
                break
            else:
                yield Request(
                    url=self.gallery_api.format(content_id),
                    headers=self.start_headers,
                    callback=self.parse_gallery,
                    meta=meta)

    def parse_gallery(self, response):
        rs = json.loads(response.text)
        data = rs.get('data', {}).get("common", {})
        if rs.get('state') != True or not isinstance(data, dict):
            return self.produce_debugitem(response, 'json error')
        pubtime = data.get('published')
        media = {}
        contents = []
        img_list = data.get("images", [])
        img_count = len(img_list)
        for idx, img_data in enumerate(img_list):
            img_idx = idx+1
            media.setdefault("images", {})
            media['images'][str(img_idx)] = {"src": img_data["image"]}
            contents.append("<p>%s</p>"%img_data["note"])
            if idx >= img_count-1:
                continue
            contents.append('<p>${{%s}}$</p>' % (img_idx))
        content = "".join(contents)
        return self.produce_item(
            response=response,
            title=response.meta['title'],
            pubtime=pubtime,
            origin_name=response.meta["origin_name"],
            summary=data.get('summary'),
            content=content,
            media=media)

    def parse_item(self, response):
        articel_data = json.loads(response.text)
        common_data = articel_data.get('data', {}).get("common", {})
        pubtime = common_data.get('published')
        soup = BeautifulSoup(common_data.get("content"), "html.parser") 
        elem_article = soup.find("div", {"class":"article"})
        content, media, _, _ = self.content_clean(elem_article.prettify())

        return self.produce_item(
            response=response,
            title=response.meta['title'],
            pubtime=pubtime,
            origin_name=response.meta["origin_name"],
            summary=articel_data.get('summary'),
            content=content,
            media=media)
