# -*- coding: utf-8 -*-
import json
from datetime import datetime
from scrapy import Request
from news_all.spider_models import NewsRSpider


class NxrbSpider(NewsRSpider):
    '''宁夏日报'''
    # 目前存在的问题：
    # 2、包含主题页的链接 http://app.nxnews.net/ningxia/cfwz/zt/201906/t20190610_6315696.html
    # 3、包含微信公众号的链接 https://mp.weixin.qq.com/s/O7ZNiu3kDgpdo0bhPEgQSQ
    # 6、https://rmt.imugeda.com/c/-bhl/x100/index.html?t=1549098561&custom=&crid=&s=2&from=singlemessage
    name = 'nxrb'
    mystart_urls = {
        'http://app.nxnews.net/ningxia/cfwz/tt/index_v2.json': 1301806,  # 宁夏日报-头条
        'http://app.nxnews.net/ningxia/cfwz/xx/index.json': 1301807,  # 宁夏日报-学习
        'http://app.nxnews.net/ningxia/cfwz/sj/index.json': 1301808,  # 宁夏日报-时事
        'http://app.nxnews.net/ningxia/cfwz/sp/index.json': 1301811,  # 宁夏日报-时评
        'http://app.nxnews.net/ningxia/cfwz/wx/index.json': 1301812,  # 宁夏日报-生活
        'http://app.nxnews.net/ningxia/cfwz/cj/index.json': 1301809,  # 宁夏日报-财经
        'http://app.nxnews.net/ningxia/cfwz/yc/index.json': 1301814,  # 宁夏日报-银川
    }
    
    custom_settings ={'DEPTH_LIMIT': 2}  # 在详情页又抽取新闻设置深度为0 或者 >1
   
    def parse(self, response):
        rj = json.loads(response.text)
        results = rj.get('response')
        try:
            topic_datas = results.get('topic_datas')
            for i in topic_datas:
                url = i.get("url")

                title = i.get("title")
                origin_name = i.get("source")
                pubtime = i.get("ptime")

                yield Request(
                    url=url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,"origin_name":origin_name,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )
            datas = results.get('datas')
            for j in datas:
                url = j.get("url")

                title = j.get("title")
                origin_name = j.get("source")
                pubtime = j.get("ptime")

                yield Request(
                    url=url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                          "origin_name": origin_name,
                          
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )
        except:
            datas = results.get('datas')
            for j in datas:
                url = j.get("url")

                title = j.get("title")
                origin_name = j.get("source")
                pubtime = j.get("ptime")

                yield Request(
                    url=url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                          "origin_name": origin_name,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )

    def parse_item(self, response):
        xp = response.xpath
        try:
             cvs = xp('//section[@class="content"]') \
                          or xp('//div[@class="cnt_bd"]') \
                          or xp('//div[@class="main-text-container"]/section')
             content_div = cvs[0]
        except:
            return self.parse_item_2(response)

        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            
            content=content,
            media=media,
            videos=videos,
        )
    
    def parse_item_2(self, response):
        rj = json.loads(response.text)
        results = rj.get('response', {})
        topic_datas = results.get('topic_datas', [])
        for i in topic_datas:
            url = i.get("url")
            try:
                title = i.get("title")
                origin_name = i.get("source")
                pubtime = i.get("ptime")

                yield Request(
                    url=url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                          "origin_name": origin_name,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )
            except:
                yield self.produce_debugitem(response, "json error")

