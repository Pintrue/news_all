# -*- coding: utf-8 -*-

from copy import deepcopy
from scrapy import Request
import json
from scrapy.conf import settings
from news_all.spider_models import NewsRSpider
from news_all.tools.html_clean import decode_html, json_load_html


class guangmingSpider(NewsRSpider):
    """光明日报 app"""
    name = 'guangming_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls_base = {  #
        'http://s.cloud.gmw.cn/2016/json/sxw/rd/': 624,  # APP端-中央媒体移动端-光明日报-新闻-热点
        'http://s.cloud.gmw.cn/2016/json/sxw/sp/': 626,  # APP端-中央媒体移动端-光明日报-新闻-时评
        'http://s.cloud.gmw.cn/2016/json/sxw/gn/': 627,  # APP端-中央媒体移动端-光明日报-新闻-时政
        'http://s.cloud.gmw.cn/2016/json/sxw/gj/': 628,  # APP端-中央媒体移动端-光明日报-新闻-国际
        'http://s.cloud.gmw.cn/2016/json/sxw/wy/': 629,  # APP端-中央媒体移动端-光明日报-新闻-文化
        'http://s.cloud.gmw.cn/2016/json/sxw/jy/': 630,  # APP端-中央媒体移动端-光明日报-新闻-教育
        'http://s.cloud.gmw.cn/2016/json/sxw/ds/': 631,  # APP端-中央媒体移动端-光明日报-新闻-悦读
        'http://s.cloud.gmw.cn/2016/json/sxw/sx/': 632,  # APP端-中央媒体移动端-光明日报-新闻-思想
        'http://s.cloud.gmw.cn/2016/json/sxw/xr/': 633,  # APP端-中央媒体移动端-光明日报-新闻-学人
        'http://s.cloud.gmw.cn/2016/json/sxw/cj/': 634,  # APP端-中央媒体移动端-光明日报-新闻-财经
        'http://s.cloud.gmw.cn/2016/json/sxw/kj/': 635,  # APP端-中央媒体移动端-光明日报-新闻-科技
        'http://s.cloud.gmw.cn/2016/json/sxw/jk/': 636,  # APP端-中央媒体移动端-光明日报-新闻-健康
        'http://s.cloud.gmw.cn/2016/json/sxw/ty/': 637,  # APP端-中央媒体移动端-光明日报-新闻-体育
        'http://s.cloud.gmw.cn/2016/json/sxw/yl/': 638,  # APP端-中央媒体移动端-光明日报-新闻-娱乐
        'http://s.cloud.gmw.cn/2016/json/sxw/js/': 640,  # APP端-中央媒体移动端-光明日报-新闻-军事
        'http://s.cloud.gmw.cn/2016/json/sxw/sj/': 641,  # APP端-中央媒体移动端-光明日报-新闻-视觉
        
        # 'http://theory.cloud.gmw.cn/api/v1/feature/concern/list':642,                                                                #APP端-中央媒体移动端-光明日报-理论-理论库 应该也不算新闻
        # 'https://s.cloud.gmw.cn/2016/json/hd/':639,                                                                                   #APP端-中央媒体移动端-光明日报-新闻-活动  不是新闻
        # 'https://gmrb.cloud.gmw.cn/gmrb/html/2019-07/10/node_1.htm':625,                                                                  #APP端-中央媒体移动端-光明日报-新闻-读报
        # 'http://theory.cloud.gmw.cn/api/v1/repository/users?withArticle=true&repositoryType=hot&resType=list&time=1562728787233':643,     #APP端-中央媒体移动端-光明日报-理论-理论库
        
    }

    mystart_urls = deepcopy(mystart_urls_base)
    
    for i in range(2, 13):  # todo 优化多少页之后就没有24时之内的新闻了就不翻下一页了
        for x, y in mystart_urls_base.items():
            if x == 'http://theory.cloud.gmw.cn/api/v1/feature/concern/list':
                url = x + '?page={}'.format(i)
                mystart_urls[url] = y
            elif x == 'http://s.cloud.gmw.cn/2016/json/sxw/sx/':  # '思想' 的请求列表 ：https://s.cloud.gmw.cn/zcms/catalog/22342/Json/
                url = 'https://s.cloud.gmw.cn/zcms/catalog/22342/Json/' + 'index_{}.json'.format(i)
                mystart_urls[url] = y
            
            else:
                url = x + 'index_{}.json'.format(i)
                mystart_urls[url] = y
    
    def parse(self, response):
        rs = json.loads(response.text)
        try:
            for i, j in enumerate(rs['list']):
                title = j['title']
                articleId = j['articleId']
                news_url = 'http://s.cloud.gmw.cn/zcms/getArticleInfo?articleId={}'.format(articleId)
                # news_url = 'http://s.cloud.gmw.cn/zcms/getArticleInfo?articleId=1282342'
                yield Request(
                    url=news_url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}, )
        except:  # http://theory.cloud.gmw.cn/api/v1/feature/concern/list
            for i, j in enumerate(rs['data']):
                title = j['title']
                articleId = j['articleId']
                news_url = 'http://s.cloud.gmw.cn/zcms/getArticleInfo?articleId={}'.format(articleId)
                # news_url = 'http://s.cloud.gmw.cn/zcms/getArticleInfo?articleId=1282342'
                yield Request(
                    url=news_url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}, )

    def parse_item(self, response):  # 返回的json有无法解析的内容，需要清除
        # 'http://s.cloud.gmw.cn/zcms/getArticleInfo?articleId=1283045'
        try:
            rs = json_load_html(response.text)
            if rs['data']['tagText'] == '直播':
                return self.produce_debugitem(response, '直播')
            title = rs['data']['title']
            pubtime = rs['data']['pubTime']
            origin_name = rs['data']['Source']
            content = decode_html(rs['data']['artContent']) if rs['data'].get('artContent') else decode_html(
                rs['data']['content'])
            
            content, media, _, _ = self.content_clean(content)
        except:
            return self.produce_debugitem(response, "json error")
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )
