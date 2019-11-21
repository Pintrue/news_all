#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 15:29
# @Author  : wjq
# @File    : jiemian_wap.py

import random
from copy import deepcopy
from datetime import datetime
import time
import json
from urllib.request import unquote
from scrapy import Request
from scrapy.conf import settings
from news_all.spider_models import NewsRSpider
import re


img_pattern = re.compile(r'\[img\:(\d+)\]')  # [img:0]
UA = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)'
]


class JiemianWapSpider(NewsRSpider):
    chinese_name = """界面新闻app"""
    name = 'jiemian_app'
    dd = deepcopy(settings.getdict('APP_DOWN'))
    dd['news_all.middlewares.ProxyRdMiddleware'] = 100  # 备用 使用隧道代理
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': dd, }
    # custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    sleep_time = 10
    mystart_urls = {
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=137&lastTime=0&page=1&code_p=11&code_c=1100': 3589,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=181&lastTime=0&page=1&code_p=11&code_c=1100': 3590,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=183&lastTime=0&page=1&code_p=11&code_c=1100': 3591,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=259&lastTime=0&page=1&code_p=11&code_c=1100': 3592,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=322&lastTime=0&page=1&code_p=11&code_c=1100': 3593,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=644&lastTime=0&page=1&code_p=11&code_c=1100': 3594,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=643&lastTime=0&page=1&code_p=11&code_c=1100': 3595,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=138&lastTime=0&page=1&code_p=11&code_c=1100': 3596,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=121&lastTime=0&page=1&code_p=11&code_c=1100': 3597,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=406&lastTime=0&page=1&code_p=11&code_c=1100': 3598,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=120&lastTime=0&page=1&code_p=11&code_c=1100': 3599,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=117&lastTime=0&page=1&code_p=11&code_c=1100': 3600,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=118&lastTime=0&page=1&code_p=11&code_c=1100': 3601,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=260&lastTime=0&page=1&code_p=11&code_c=1100': 3602,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=141&lastTime=0&page=1&code_p=11&code_c=1100': 3603,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=669&lastTime=0&page=1&code_p=11&code_c=1100': 3604,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=202&lastTime=0&page=1&code_p=11&code_c=1100': 3605,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=203&lastTime=0&page=1&code_p=11&code_c=1100': 3606,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=158&lastTime=0&page=1&code_p=11&code_c=1100': 3607,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=142&lastTime=0&page=1&code_p=11&code_c=1100': 3608,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=519&lastTime=0&page=1&code_p=11&code_c=1100': 3609,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=937&lastTime=0&page=1&code_p=11&code_c=1100': 3610,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=921&lastTime=0&page=1&code_p=11&code_c=1100': 3611,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=670&lastTime=0&page=1&code_p=11&code_c=1100': 3612,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=671&lastTime=0&page=1&code_p=11&code_c=1100': 3613,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=672&lastTime=0&page=1&code_p=11&code_c=1100': 3614,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=673&lastTime=0&page=1&code_p=11&code_c=1100': 3615,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=313&lastTime=0&page=1&code_p=11&code_c=1100': 3616,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=447&lastTime=0&page=1&code_p=11&code_c=1100': 3617,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=123&lastTime=0&page=1&code_p=11&code_c=1100': 3618,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=140&lastTime=0&page=1&code_p=11&code_c=1100': 3619,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=463&lastTime=0&page=1&code_p=11&code_c=1100': 3620,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=830&lastTime=0&page=1&code_p=11&code_c=1100': 3621,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=666&lastTime=0&page=1&code_p=11&code_c=1100': 3622,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=294&lastTime=0&page=1&code_p=11&code_c=1100': 3623,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=201&lastTime=0&page=1&code_p=11&code_c=1100': 3624,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=182&lastTime=0&page=1&code_p=11&code_c=1100': 3625,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=442&lastTime=0&page=1&code_p=11&code_c=1100': 3626,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=469&lastTime=0&page=1&code_p=11&code_c=1100': 3627,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=152&lastTime=0&page=1&code_p=11&code_c=1100': 3628,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=124&lastTime=0&page=1&code_p=11&code_c=1100': 3629,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=1065&lastTime=0&page=1&code_p=11&code_c=1100': 3630,
        'https://papi.jiemian.com/app/channel/index?version=6.1.1.0&id=530&lastTime=0&page=1&code_p=11&code_c=1100': 3631,
    }
    # 已测试用json或者html都会反爬
    # base_api = 'https://m.jiemian.com/index.php/api/app/article/index?id={}'
    base_api = 'https://m.jiemian.com/article/{}.html'
    start_headers = {
        "User-Agent": "JiemianNews/6.1.1.0 (android; android 6.0; brand-Xiaomi-Redmi Pro)",
        "jmNetwork": "WIFI",
        "jmOSVersion": "6.0",
        "jmResolution": "1080*1920",
        "jmSystemName": "android",
        "jmUDID": "861603035854842",
        "jmVersion": "6.1.1.0",
    }
    """
    备用 start_headers
    "User-Agent": "JiemianNews/6.1.1.0 (android; android 6.0; brand-Xiaomi-Redmi Pro)",
    "jmNetwork": "WIFI",
    "jmOSVersion": "6.0",
    "jmResolution": "1080*1920",
    "jmSystemName": "android",
    "jmUDID": "861603035854842",
    "jmVersion": "6.1.1.0",
    """
    
    def parse(self, response):
        rs = json.loads(response.text)
        data = rs.get('nodeList') or rs.get('result')
        if str(rs.get('code')) != '0' or not isinstance(data, dict):
            return self.produce_debugitem(response, 'json error')
            
        arts = data.get('list', []) + data.get('carousel', [])
        for i in arts:
            a = i.get('article')
            if not a:
                print('have not article key')
                """
                {'type': 'special',
                 'special': {'object_type': 'special',
                            'id': '1066', 'title': '大国匠心',
                             'image': 'https://img1.jiemian.com/101/original/20190327/155366125659486900_a750x422.jpeg',
                              'istemplate': '3', 'special_url': 'https://www.jiemian.com/special/1066.html',
                            'extend': {'typename': '专题'}}
                  }
                """
                continue
            nid = a.get('id')
            if not nid:
                # news_url = a.get('m_url')
                # https://m.jiemian.com/article/3147384.html  用xpath
                # 备用 https://m.jiemian.com/index.php/api/app/article/index?id=3147384 用json  3131368
                continue
            news_url = self.base_api.format(nid)

            title = a.get('title')
            pubtime = a.get('publish_time')

            cat = a.get('category')
            origin_name = cat.get('name') if cat else None
            time.sleep(random.uniform(1, 5))
            yield Request(
                url=news_url,  # 若无User-Agent则connection timed out: 10060: 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。.
                headers={"User-Agent": UA[random.randint(0, len(UA) - 1)]},
                callback=self.parse_item_2,
                meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                       'origin_name': origin_name,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )
    
    def parse_item(self, response):
        rs = json.loads(response.text)
        result = rs.get('result')
        if str(rs.get('code')) != '0' or not result:
            return self.produce_debugitem(response, 'json error')
        a = result.get('article')
        if not a or result.get('videos') or result.get('audios'):
            return  # 排除视频 音频
        pubtime = response.request.meta['pubtime']
        if not pubtime:
            pubtime = a.get('publish_time')
            
        content_raw = a.get('content')
        content = unquote(content_raw)
        img_list = result.get('photos')
        media = {}
        img_count = len(img_pattern.findall(content))
        
        if isinstance(img_list, list):
            if img_list:
                for i, j in enumerate(img_list):
                    media.setdefault("images", {})
                    media['images'][str(i + 1)] = {"src": j.get('image')}
                content, img_count = self.image_clean(content)
            if img_count != len(img_list):
                self.log('图片数量不符!')
        elif img_count > 0:
            self.log('图片数量不符!')
        content = self.parser.cleaner.clean_html(content)  # 再去不要的dom 和 属性
        
        return self.produce_item(
            response=response,
            title=response.meta['title'],
            pubtime=pubtime,
            origin_name=a.get('category_group')[0].get('name'),
            summary=a.get('summary'),
            content=content,
            media=media,
        )
    
    def image_clean(self, content):
        fr = img_pattern.finditer(content)
        new_content = ''
        img_count = 0
        for i, j in enumerate(fr):
            st = content.find(j.group())
            end = st + len(j.group())
            new_content += content[:st] + '${{%s}}$' % (i + 1)
            content = content[end:]
            img_count += 1
        
        new_content += content
        new_content.replace('$$', '$<br>$')  # 连续2图片加换行
        return new_content, img_count
    
    def parse_item_2(self, response):
        # 备用 https://m.jiemian.com/article/3147384.html  用xpath
        xp = response.xpath
        try:
            pubtime = response.meta.get('pubtime') or xp(r'//span[@class="date"]/text()').extract_first().strip()
            origin_name = response.meta.get('origin_name') or xp('//span[@class="user"]/text()').extract_first('')
            cv = xp('//div[@class="article-content"]')[0]
            content, media, video, cover = self.content_clean(cv)
        except:
            return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,
            title=response.meta['title'],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )
