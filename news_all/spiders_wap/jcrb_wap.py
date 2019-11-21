#!/usr/bin/env python
# -*- coding:utf-8 _*-
# Time: 2019/07/25
# Author: zcy

from news_all.spider_models import *
from scrapy.conf import settings
import json
from scrapy import Request
import requests
import datetime
import re


class ZgjwSpider(NewsRSpider):
    """检察日报 app"""
    name = 'jcrb_app'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN'),
        'DEPTH_LIMIT': 20
    }

    mystart_urls_base = {
        'http://jcrbapp.techjc.cn/api/getArticles?sid=1&cid=2&lastFileID=%s&rowNumber=%s': 3389,  # 热点
        'http://jcrbapp.techjc.cn/api/getArticles?sid=1&cid=3&lastFileID=%s&rowNumber=%s': 3391,  # 时政
        'http://jcrbapp.techjc.cn/api/getArticles?sid=1&cid=4&lastFileID=%s&rowNumber=%s': 3393,  # 检察
        'http://jcrbapp.techjc.cn/api/getArticles?sid=1&cid=6&lastFileID=%s&rowNumber=%s': 3396,  # 锐评
        'http://jcrbapp.techjc.cn/api/getArticles?sid=1&cid=7&lastFileID=%s&rowNumber=%s': 3397,  # 视觉
        'http://jcrbapp.techjc.cn/api/getArticles?sid=1&cid=8&lastFileID=%s&rowNumber=%s': 3398,  # 万象
        'http://jcrbapp.techjc.cn/api/getAllSubscribeArticle?cid=10&lastFileID=%s&rowNumber=%s': 3399,  # 发布大厅
        # 'http://jcrbapp.techjc.cn/api/getArticles?sid=1&cid=3612&lastFileID=%s&rowNumber=%s': 7,  # 专题

        # todo http://szb.techjc.cn/mobile/2019/20190725/20190725_m.html
        # 'http://szb.techjc.cn/mobile/%s_m.html'date.today().strftime('%Y/%Y%m%d/%Y%m%d'): 3394  # 数字报
        'http://szb.techjc.cn/mobile/%s/%s/%s_m.html': 3394  # 数字报
    }
    article_list_url_base = 'http://jcrbapp.techjc.cn/api/getArticles?sid=1&cid=%s&lastFileID=%s&rowNumber=%s'
    article_url_base = 'http://jcrbapp.techjc.cn/api/getArticle?sid=1&aid=%s'
    column_url_base = 'http://jcrbapp.techjc.cn/api/getColumns?sid=1&cid=%s&order=desc'
    mystart_urls = {}
    for url, source_id in mystart_urls_base.items():
        if source_id != 3394:
            mystart_urls[url % (0, 0)] = source_id
        else:  # 数字报
            today = datetime.date.today()
            # http://szb.techjc.cn/mobile/2019/20190725/20190725_m.html
            mystart_urls[url % (
                today.strftime('%Y'),
                today.strftime('%Y%m%d'),
                today.strftime('%Y%m%d')
            )] = source_id

    def parse(self, response):
        source_id = response.meta['source_id']
        if source_id != 3394:
            current_base_url = response.meta.get('current_base_url')
            if current_base_url is None:
                # 根据 source_id 获取当前列表 base url
                current_base_url = list(self.mystart_urls_base.keys())[
                    list(self.mystart_urls_base.values()).index(source_id)]

            article_list = json.loads(response.body).get('list')
            if article_list is None or len(article_list) == 0:
                return

            lastFileID = article_list[-1]['fileID']
            for article in article_list:
                # 普通文章
                if article['linkID'] == 0:
                    yield Request(
                        url=self.article_url_base % article['fileID'],
                        callback=self.parse_item,
                        meta={
                            'video': article['videoUrl'],
                            'source_id': source_id,
                            'start_url_time': response.meta.get('start_url_time'),
                            'schedule_time': response.meta.get('schedule_time')
                        }
                    )
                else:
                    # 专题
                    column_page = requests.get(self.column_url_base % article['linkID'])
                    columnID = json.loads(column_page.text)['columns'][0]['columnID']
                    current_url = response.request.url
                    lastFileID = re.findall('lastFileID=(\d+)', current_url)[0]
                    yield Request(
                        self.article_list_url_base % (columnID, 0, 0),
                        callback=self.parse,
                        meta={
                            'source_id': source_id,
                            'current_base_url': self.article_list_url_base % (columnID, '%s', '%s'),
                            'start_url_time': response.meta.get('start_url_time'),
                            'schedule_time': response.meta.get('schedule_time')
                        }
                    )

            # 获取下一页列表
            yield Request(
                current_base_url % (lastFileID, 20),
                callback=self.parse,
                meta={
                    'source_id': source_id,
                    'isStartUrl': True,
                    'start_url_time': response.meta.get('start_url_time'),
                    'schedule_time': response.meta.get('schedule_time')
                }
            )
        else:  # 数字报
            today = datetime.date.today()
            article_urls = response.xpath('//ul[@class="nav-list-group"]/li/a/@href').extract()
            article_urls = [
                'http://szb.techjc.cn/mobile/' + today.strftime('%Y') + '/' + today.strftime('%Y%m%d') + i[1:] for i in
                article_urls]
            for article_url in article_urls:
                yield Request(
                    url=article_url,
                    callback=self.parse_item,
                    meta={
                        'source_id': source_id,
                        'pubtime': today.strftime('%Y/%m/%d') + '0:0:0',
                        'start_url_time': response.meta.get('start_url_time'),
                        'schedule_time': response.meta.get('schedule_time')
                    }
                )

    def parse_item(self, response):
        source_id = response.meta['source_id']
        if source_id != 3394:
            article_dict = json.loads(response.body)
            title = article_dict['title']
            pubtime = article_dict['publishTime']

            origin_name = article_dict['source']
            content = article_dict['content']
            content_clean, media, video, cover = self.content_clean(content, kill_xpaths=[
                '//img[re:match(@src, "/\d{15,}.jpg")]',
                '//img[re:match(@src, "/\d{15,}_\d+x\d{1,2}.jpg")]',
                '//img[re:match(@src, "/\d{15,}_\d+x[1-4]\d\d.jpg")]'])
            video = {'1': {'src': response.meta['video']}} if response.meta['video'] != '' else ''
            if video:
                print()
            yield self.produce_item(
                response=response,
                title=title,
                pubtime=pubtime,
                origin_name=origin_name,
                content=re.sub('<div><video[\w\W]*</div>', '<div>#{{1}}#</div></br>',
                               content_clean) if video != '' else content_clean,
                media=media,
                videos=video
            )
        else:  # 数字报
            pubtime = response.meta['pubtime']
            main_body = response.xpath
            main_title = main_body('//font[@id="main-title"]/b/text()').extract_first()
            sub_title = main_body('//font[@id="sub-title"]/text()').extract_first()
            title = main_title if main_title is not None else '' + ' ' + sub_title if sub_title is not None else ''
            content = main_body('//div[@id="content"]').extract_first()
            img = main_body('//div[@id="content"]//img').extract()

            current_url = re.findall('(.+)content', response.request.url)[0]
            if img is not None and len(img) != 0:
                content = content.replace(re.findall('img\ src="(\./[\d_]+)', content)[0],
                                          current_url + re.findall('[\d_]+', content)[0])
            content_clean = self.content_clean(content)
            yield self.produce_item(
                response=response,
                title=title,
                pubtime=pubtime,
                origin_name='检察日报',
                content=content_clean[0],
                media=content_clean[1],
            )
