#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/28 16:59
# @Author  : wjq
# @File    : zaker_wap.py


from datetime import datetime
import json
from scrapy import Request
from news_all.tools.html_clean import IMG_PATTERN
from news_all.spider_models import NewsRSpider
import re
from scrapy.conf import settings


class ZakerWapSpider(NewsRSpider):
    chinese_name = """ZAKER新闻app"""
    name = 'zaker_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}

    mystart_urls = {
        # 7月19日api已失效
        # 'http://hotphone.myzaker.com/daily_hot_new.php?_appid=AndroidPhone&_brand=OPPO&_bsize=720_1280&_city=%E5%8C%97%E4%BA%AC&_dev=31&_imei=865685026456493&_lat=39.926975&_lbs_city=%E5%8C%97%E4%BA%AC&_lbs_province=%E5%8C%97%E4%BA%AC%E5%B8%82&_lng=116.480181&_mac=a8%3A1b%3A5a%3A2d%3A98%3Ad5&_mcode=2FCFD3E1&_net=wifi&_nudid=076cb49629a4527b&_os=4.4.4_R8207&_os_name=R8207&_province=%E5%8C%97%E4%BA%AC%E5%B8%82&_udid=865685026456493&_v=8.4.4&_version=8.44&act=pre&last_time=1558592297&time=1558592294': 3586,
        'http://iphone.myzaker.com/zaker/blog.php?_appid=AndroidPhone&_brand=OPPO&_bsize=720_1280&_city=%E5%8C%97%E4%BA%AC&_dev=31&_imei=865685026456493&_lat=39.926975&_lbs_city=%E5%8C%97%E4%BA%AC&_lbs_province=%E5%8C%97%E4%BA%AC%E5%B8%82&_lng=116.480181&_mac=a8%3A1b%3A5a%3A2d%3A98%3Ad5&_mcode=2FCFD3E1&_net=wifi&_nudid=076cb49629a4527b&_os=4.4.4_R8207&_os_name=R8207&_province=%E5%8C%97%E4%BA%AC%E5%B8%82&_udid=865685026456493&_v=8.4.4&_version=8.44&app_id=13799': 3587,
        'http://iphone.myzaker.com/zaker/selected_article.php?_appid=AndroidPhone&_brand=OPPO&_bsize=720_1280&_city=%E5%8C%97%E4%BA%AC&_dev=31&_imei=865685026456493&_lat=39.926975&_lbs_city=%E5%8C%97%E4%BA%AC&_lbs_province=%E5%8C%97%E4%BA%AC%E5%B8%82&_lng=116.480181&_mac=a8%3A1b%3A5a%3A2d%3A98%3Ad5&_mcode=2FCFD3E1&_net=wifi&_nudid=076cb49629a4527b&_os=4.4.4_R8207&_os_name=R8207&_province=%E5%8C%97%E4%BA%AC%E5%B8%82&_udid=865685026456493&_v=8.4.4&_version=8.44': 3588,
    }
        
    def parse(self, response):
        rj = json.loads(response.text)
        if rj.get("msg") != "ok":
            return self.produce_debugitem(response, 'json error')
        data = rj.get('data', {})
        articles = data.get('articles', [])

        for i in articles:
            result = None
            if i.get('full_url'):
                result = self.deal_one_article(i, response)
            elif i.get('article_group'):
                items = i.get('article_group').get('items', [])
                for it in items:
                    if it.get('type') != 'a':
                        print(it)
                        continue
                    result = self.deal_one_article(it.get('article'), response)
            if result:
                yield result

    def deal_one_article(self, art, response):
        news_url = art.get('full_url')

        # 排除视频
        special_info = art.get('special_info')
        if special_info and special_info.get('video_inside') == 'Y':
            return

        title = art.get('title')
        pubtime = art.get('list_dtime')
        origin_name = art.get('auther_name')
        return Request(
            url=news_url,
            callback=self.parse_item,
            meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                  'origin_name': origin_name,
                  'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
        )

    def parse_item(self, response):
        rj = json.loads(response.text)
        if rj.get("msg") != "ok":
            return self.produce_debugitem(response, 'json error')

        data = rj.get('data')
        content_div = data.get('content')
        media_dict_list = data.get('media', [])

        media = {}
        idx = 0
        for i in media_dict_list:
            media.setdefault("images", {})
            if i.get("type") == "image":
                idx += 1
                media['images'][str(idx+1)] = {"src": i.get('url')}

        content, img_count = self.image_clean(content_div)
        if img_count != idx:
            self.log('图片数量不符!')
        # <div class="img_box" id="id_imagebox_19" onclick='window.location.href="http://www.myzaker.com/?_zkcmd=open_media&index=19"'>
        content = self.parser.cleaner.clean_html(content, kill_xpaths=[r'//div[@class="img_box"]'])

        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            content=content,
            media=media
        )

    def image_clean(self, content):
        """
        <img id="id_image_20" class="" src="article_html_content_loading.png"></img>
        :param content:
        :return:
        """
        fr = re.finditer(IMG_PATTERN, content)
        new_content = ''
        img_count = 0
        for i, j in enumerate(fr):
            img_count += 1
            st = content.find(j.group())
            end = st + len(j.group())
            new_content += content[:st] + '${{%s}}$' % (i + 1)
            content = content[end:]

        new_content += content
        new_content.replace('$$', '$<br>$')  # 连续2图片加换行
        return new_content, img_count