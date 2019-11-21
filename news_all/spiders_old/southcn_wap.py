#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 9:36
# @Author  : wjq
# @File    : southcn_wap.py

import re
import json
from scrapy import Request
from scrapy.conf import settings
from news_all.spider_models import NewsRSpider


ip = re.compile(r'\<\!--IMAGE\w+#\d+--\>')  # <!--IMAGEARRAY#23242145--></p>
vp = re.compile(r'\<\!--VIDEO\w+#\d+--\>')  # <!--VIDEOARRAY#0-->  or <!--VIDEOS#1-->


class SouthcnWapSpider(NewsRSpider):
    chinese_name = """南方PLUS客户端"""
    name = 'southcn_wap'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        'https://api.nfapp.southcn.com/nanfang_if/getArticles?adv=1&columnId=1667&service=1&count=20&lastFileId=0&rowNumber=0&version=0': 1301994,
        # 南方PLUS 体育
        'https://api.nfapp.southcn.com/nanfang_if/getArticles?adv=1&columnId=100&service=1&count=20&lastFileId=0&rowNumber=0&version=0': 1302000,
        # 南方PLUS 健康
        'https://api.nfapp.southcn.com/nanfang_if/getArticles?adv=1&columnId=94&service=1&count=20&lastFileId=0&rowNumber=0&version=0': 1301991,
        # 南方PLUS 国际
        'https://api.nfapp.southcn.com/nanfang_if/getArticles?adv=1&columnId=1205&service=1&count=20&lastFileId=0&rowNumber=0&version=0': 1301993,
        # 南方PLUS 房产
        'https://api.nfapp.southcn.com/nanfang_if/recommend/article/getPersonalArticles?pageNo=0&deviceId=00000000-6a03-82c9-ffff-ffffca01fdf4&version=4.5.0': 1302001,
        # 南方PLUS 推荐
        'https://api.nfapp.southcn.com/nanfang_if/getArticles?adv=1&columnId=410&service=1&count=20&lastFileId=0&rowNumber=0&version=0': 1301996,
        # 南方PLUS 教育
        'https://api.nfapp.southcn.com/nanfang_if/getArticles?adv=1&columnId=653&service=1&count=20&lastFileId=0&rowNumber=0&version=0': 1301995,
        # 南方PLUS 数码
        'https://api.nfapp.southcn.com/nanfang_if/getArticles?adv=1&columnId=17&service=1&count=20&lastFileId=0&rowNumber=0&version=0': 1301999,
        # 南方PLUS 文娱
        'https://api.nfapp.southcn.com/nanfang_if/getArticles?adv=1&columnId=1206&service=1&count=20&lastFileId=0&rowNumber=0&version=0': 1301997,
        # 南方PLUS 旅游
        'https://api.nfapp.southcn.com/nanfang_if/getArticles?adv=1&columnId=59&service=1&count=20&lastFileId=0&rowNumber=0&version=0': 1301998,
        # 南方PLUS 社会
        'https://api.nfapp.southcn.com/nanfang_if/getArticles?adv=1&columnId=16&service=1&count=20&lastFileId=0&rowNumber=0&version=0': 1301992,
        # 南方PLUS 经济
    }

    def parse(self, response):
        rs = json.loads(response.text)
        if not isinstance(rs.get("list"), list):
            da = rs.get("data", {})
            if isinstance(da, dict) and isinstance(da.get('list'), list):
                data = da['list']
            else:
                return self.produce_debugitem(response, 'json error')
        else:
            data = rs.get("list", [])
        
        for i in data:
            if i.get('articleType') in [6, ]:  # 0原创 3专题 6直播 10视频
                continue

            if i.get('articleType') == 3 and i.get('SpecialTopicList'):  # 是专题
                SpecialTopicList = i['SpecialTopicList']
                for s in SpecialTopicList:
                    # http://api.nfapp.southcn.com/nanfang_if/getArticleContent?articleId=2531643&colID=7747
                    result = self.get_detail_req(s, response)
                    if result:
                        yield result
            else:
                result = self.get_detail_req(i, response)
                if result:
                    yield result
    
    def get_detail_req(self, news_dict, response):
        news_url = news_dict.get('contentUrl')

        pubtime = news_dict.get('publishtime') or news_dict.get('createTime')
        if pubtime.endswith('.0'):
            pubtime = pubtime[:-2]
            
        title = news_dict.get('title')
        origin_name = news_dict.get('releaseSource')
        return Request(
            url=news_url,
            callback=self.parse_item,
            meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                  'origin_name': origin_name,
                  'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
        )
 
    def parse_item(self, response):
        """
        # 因为有的是js渲染就放弃 html 解析方式
        # https://static.nfapp.southcn.com/apptpl/videoToShare/index.html?id=2548361#/landscape?id=2548361
        xp = response.xpath
        try:
            content_div = xp("//div[@class='article']")[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, _, _ = self.content_clean(content_div, kill_xpaths=[
            '//img[contains(@src, "45c855b2-ff57-49c8-bda0-c75db468d456.jpg")]/parent::p',
            '//img[contains(@title|@alt, "二维码")]/parent::p'],)
        """
        try:
            rj = json.loads(response.text)
            
            content, img_count, vid_count = self.__clean(rj.get('content', ''))

            media = {}
            images = rj.get('images', [])
            if images:
                media.setdefault("images", {})
                # if len(images[0].get('imagearray', [])) != img_count:
                #     print()
                for i, j in enumerate(images[0].get('imagearray', [])):
                    media['images'][str(i + 1)] = {"src": j.get('imageUrl')}
            
            videos = {}
            videos_list = rj.get('videos', [])
            if videos_list:
                # if len(videos_list[0].get('videoarray', [])) != vid_count:
                #     print()
                for i, j in enumerate(videos_list[0].get('videoarray', [])):
                    videos[str(i + 1)] = {"src": j.get('videoUrl')}
            
            content = self.parser.cleaner.clean_html(content)
        except:
            return self.produce_debugitem(response, 'json error')
            
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            
            content=content,
            media=media,
            videos=videos
        )

    def __clean(self, content):
        imgs = ip.findall(content)
        vids = vp.findall(content)
    
        for i, j in enumerate(imgs):
            content = content.replace(j, '${{%s}}$' % (i + 1))
        for i, j in enumerate(vids):
            content = content.replace(j, '#{{%s}}#' % (i + 1))
    
        content = content.replace('$$', '$<br>$')  # 连续2图片 视频加换行
        return content, len(imgs), len(vids)


"""
频道
[
    {
        "id": 14,
        "name": "首页",
        "pageName": "index",
    },
    {
        "id": 1275,
        "name": "南方号",
        "pageName": "nanfanghao",
    },
    {
        "id": 11389,
        "name": "粤港澳大湾区",
        "pageName": "yuegangaodawanqu",
    },
    {
        "id": 8967,
        "name": "视频",
        "pageName": "shipin",
    },
    {
        "id": 7747,
        "name": "党建",
        "pageName": "dangjian",
    },
    {
        "id": 18,
        "name": "观点",
        "pageName": "guandian",
    },
    {
        "id": 16,
        "name": "经济",
        "pageName": "jingji",
    },
    {
        "id": 12722,
        "name": "文化",
        "pageName": "wenhua",
    },
    {
        "id": 17,
        "name": "娱乐",
        "pageName": "yule",
    },
    {
        "id": 59,
        "name": "社会",
        "pageName": "shehui",
    },
    {
        "id": 100,
        "name": "健康",
        "pageName": "jiankang",
    },
    {
        "id": 94,
        "name": "国际",
        "pageName": "guoji",
    },
    {
        "id": 1667,
        "name": "体育",
        "pageName": "tiyu",
    },
    {
        "id": 2038,
        "name": "乡村振兴",
        "pageName": "xiangcunzhenxing",
    },
    {
        "id": 14229,
        "name": "文创",
        "pageName": "wenchuang",
    },
    {
        "id": 14126,
        "name": "广东市场监管发布厅",
        "pageName": "guangdongshichangjianguanfabuting",
    },
    {
        "id": 13670,
        "name": "广东乡村振兴发布厅",
        "pageName": "guangdongxiangcunzhenxingfabuting",
    },
    {
        "id": 13370,
        "name": "广东金融发布厅",
        "pageName": "guangdongjinrongfabuting",
    },
    {
        "id": 12817,
        "name": "南方5G",
        "pageName": "nanfang5G",
    },
    {
        "id": 12698,
        "name": "广东应急管理发布厅",
        "pageName": "guangdongyingjiguanlifabuting",
    },
    {
        "id": 10997,
        "name": "马上办",
        "pageName": "mashangban",
    },
    {
        "id": 10908,
        "name": "产业园",
        "pageName": "chanyeyuan",
    },
    {
        "id": 8710,
        "name": "茶业",
        "pageName": "chaye",
    },
    {
        "id": 4913,
        "name": "直播",
        "pageName": "zhibo",
    },
    {
        "id": 6242,
        "name": "视觉",
        "pageName": "shijue",
    },
    {
        "id": 1207,
        "name": "消费",
        "pageName": "xiaofei",
    },
    {
        "id": 1206,
        "name": "旅游",
        "pageName": "lvyou",
    },
    {
        "id": 1205,
        "name": "房产",
        "pageName": "fangchan",
    },
    {
        "id": 653,
        "name": "数码",
        "pageName": "shuma",
    },
    {
        "id": 674,
        "name": "汽车",
        "pageName": "qiche",
    },
    {
        "id": 652,
        "name": "专题",
        "pageName": "zhuanti",
    },
    {
        "id": 410,
        "name": "教育",
        "pageName": "jiaoyu",
    }
]
"""