#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/21 7:01
# @Author  : wjq
# @File    : jksb.py

import re
import json
from scrapy import Request
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings

from news_all.tools.others import to_list

img_pattern = re.compile(r'''<img.*?(?:data-original|src)=['"](.*?)['"].*?>''')


class JksbSpider(NewsRSpider):
    """健康时报 app"""
    name = 'jksb_app'
    mystart_urls = {'http://app.jksb.com.cn:10882/jksbApp/API.jhtml': [182, 183, 186, 200]}
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    # LimitatedDaysHoursMinutes = (3, 0, 0)
    start_body_map = {
        182: ("新闻", {"requestId": "1005", "osType": "1", "apiVersion": "1.0", "reqcode": "GVBZRKo3zzxKnL0Yo+WQmQ==",
                     "page": "1", "pageSize": "10", "id": "1"}),  # 407, 新闻
        183: ("生活", {"requestId": "1005", "osType": "1", "apiVersion": "1.0", "reqcode": "GVBZRKo3zzxKnL0Yo+WQmQ==",
                     "page": "1",
                     "pageSize": "10", "id": "1"}),  # 408, 生活
        186: ("心理", {"requestId": "1005", "osType": "1", "apiVersion": "1.0", "reqcode": "GVBZRKo3zzxKnL0Yo+WQmQ==",
                     "page": "1", "pageSize": "10", "id": "13"}),  # 409, 心理
        200: ("眼健康", {"requestId": "1005", "osType": "1", "apiVersion": "1.0", "reqcode": "GVBZRKo3zzxKnL0Yo+WQmQ==",
                      "page": "1", "pageSize": "10", "id": "33"}),  # 410, 眼健康
    }
    
    start_method = "POST"
    
    def parse(self, response):
        
        rs = json.loads(response.text)
        if str(rs.get('result')) != '0':
            return self.produce_debugitem(response, 'json error')
        
        data = rs.get('data', dict)
        
        for i in to_list(data.get('list')) + to_list(data.get('shuflist')):
            iid = i.get('id')
            news_url = 'http://app.jksb.com.cn//staticPage/commonMessage/{}.htm'.format(iid)
            pubtime = i.get('createTime')
            origin_name = i.get('infoSource', '健康时报客户端')
            summary = i.get('summary', '')
            title = i.get('title')
            yield Request(
                url=news_url,
                callback=self.parse_item,
                meta={'pubtime': pubtime, 'title': title, 'origin_name': origin_name, 'summary': summary,
                      'source_id': response.meta['source_id'],
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')})
    
    def parse_item(self, response):
        pubtime = response.request.meta['pubtime']
        title = response.request.meta['title']
        
        try:
            if not pubtime:
                time_strs = response.xpath('//*[@id="source_time"]/text()').re(
                    r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
                pubtime = time_strs[0]
            content_div = response.xpath('.//div[@id="ddiv"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        
        """
        "<div><strong><img alt=\"\" data-original=\"http://app.jksb.com.cn:10882/jksbApp/news/49929cfe-146a-4a90-8909-0e37f1419d96small.jpg\"></strong><div><strong>本文专家：</strong><br>北京大学第三医院放射科  田帅 张艳</div><br>X线、CT、MRI检查，对于备孕和哺乳期女性来说，到底能不能做？<br><img alt=\"\" data-original=\"http://app.jksb.com.cn:10882/jksbApp/news/4be0adfd-73e7-4cee-9fe6-4e51ed1fbd8dsmall.jpg\"><br> <div><img alt=\"\" data-original=\"http://app.jksb.com.cn:10882/jksbApp/news/0a9b8571-2019-446a-b3f4-23acfc399ebesmall.jpg\"></div><strong>备孕期：3</strong><strong>个月后可怀孕</strong><br> <br>X线和CT确实属于辐射性检查，但用于医学诊断的辐射剂量对人体是相对安全的，考虑到辐射检查的随机性效应，<strong>育龄期女性在接受</strong><strong>X</strong><strong>线或CT</strong><strong>检查的三个月之后怀孕是安全的。</strong><br> <br><strong>哺乳期：可以进行检查</strong><br> <br>有些宝妈担心放射性检查会对自己的乳房造成损害。其实，乳汁的主要成分为水、脂肪、蛋白质、糖和无机盐等，这些成分均不受医用X线照射的影响，宝妈们在接受X线或CT检查后，不会对乳汁造成任何影响，所以，在检查之后即可为宝宝哺乳。<br> <div><img alt=\"\" data-original=\"http://app.jksb.com.cn:10882/jksbApp/news/cebf78a4-bdf6-44ed-8504-75b3e5171b29small.jpg\"></div><strong>备孕期和哺乳期均可做。</strong><br> <br>磁共振成像（MRI）检查利用磁场成像，没有放射性，对人体无辐射。<br> <br>目前世界上尚没有关于人体因进行磁共振检查导致基因突变或染色体畸变发生率增高的报道，<strong>在备孕期和哺乳期做</strong><strong>MRI</strong><strong>检查是安全的。</strong><br> <br>对于妊娠期能否做MRI检查，目前<strong>普遍认为妊娠期前三个月应慎行</strong><strong>MRI</strong><strong>检查，而增强MRI</strong><strong>检查应尽量避免。</strong><br> <br>编辑：郑新颖<br><img alt=\"\" data-original=\"http://app.jksb.com.cn:10882/jksbApp/news/39c4c606-ff74-439c-ba3d-0f0d007a9b38small.jpg\"></div>"
        """
        content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[
            '//img[contains(@src|@data-original, "42344b82-c649-4b34-8b54-1db46b121624small")]'], img_re=img_pattern)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=response.request.meta['origin_name'],
            summary=response.request.meta['summary'],
            content=content,
            media=media,
            videos=videos,
        )
