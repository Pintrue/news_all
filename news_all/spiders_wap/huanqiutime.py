# -*- coding: utf-8 -*-

import json
from copy import deepcopy
from scrapy import Request
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings


class HuanqiuTimeSpider(NewsRSpider):
    """环球TIME app"""
    name = 'huanqiutime_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls_base = {
        'http://api.hqtime.huanqiu.com/api/news/list/general/hot': 148,  # 289,  # 热点
        'http://api.hqtime.huanqiu.com/api/news/list/general/international': 149,  # 293,  # 国际
        'http://api.hqtime.huanqiu.com/api/news/list/general/military': 150,  # 294,  # 军事
        'http://api.hqtime.huanqiu.com/api/news/list/general/comment': 151,  # 302,  # 评论
        'http://api.hqtime.huanqiu.com/api/news/list/general/taihai': 152,  # 303,  # 台海
        'http://api.hqtime.huanqiu.com/api/news/list/general/internal': 153,  # 306,  # 国内
        'http://api.hqtime.huanqiu.com/api/news/list/general/society': 154,  # 307,  # 社会
        'http://api.hqtime.huanqiu.com/api/news/list/general/overseas': 156,  # 318,  # 海外看中国
        'http://api.hqtime.huanqiu.com/api/news/list/general/finance': 158,  # 319,  # 财经
    }
    mystart_urls = deepcopy(mystart_urls_base)
    for i in range(2, 15):
        for x, y in mystart_urls_base.items():
            url = x + '/' + str(i)
            mystart_urls[url] = y
    
    start_headers = {
        "Accept": "application/vnd.hq_time.v2+json",  # 4月28日都报404 start_url加headers
        "clientversion": "Android/v8.4.2",  # V8.3.5
        "Host": "api.hqtime.huanqiu.com",  # 4月28日都报404 start_url加headers
    }
    baseurl = 'http://hqtime.huanqiu.com/article/{}'
    
    def parse(self, response):
        rs = json.loads(response.text)
        
        if rs.get('msg') != 'success':
            return self.produce_debugitem(response, 'json error')
        
        for i in rs.get('data', []):
            group_style = i.get('group_style')
            
            for j in i.get('group_data'):
                iid = j.get('id')
                news_url = self.baseurl.format(iid)
                title = j.get('title')
                pubtime = j.get('time_publish')

                origin_name = j.get('source')
                summary = j.get('summary')
                is_video = j.get('is_video')
                # list_type: 8 新闻是滑动图集 但用baseurl可得到单页全图文
                
                yield Request(url=news_url,
                              callback=self.parse_item,
                              # headers=self.start_headers,
                              headers={"clientversion": "Android/v8.4.2"},
                              meta={'title': title, 'pubtime': pubtime, 'origin_name': origin_name, 'summary': summary,
                                    'group_style': group_style, 'is_video': is_video,
                                    'source_id': response.meta['source_id'],
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                              )
    
    def parse_item(self, response):
        group_style = response.meta.get('group_style')
        xp = response.xpath
        try:
            if group_style < 3:
                cvs = xp("//div[@class='inner']/div[@class='content_con']") or xp('//*[@id="hideContent"]')
                content_div = cvs[0]
            else:
                self.log('url: %s, group_style !=1 or 2, response.text: %s' % (group_style, response.text))
                raise IndexError
            content, media, videos, _ = self.content_clean(content_div, need_video=response.meta.get('is_video'))
        except BaseException:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            summary=response.request.meta['summary'],
            content=content,
            media=media,
            videos=videos
        )
