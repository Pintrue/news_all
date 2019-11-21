# -*- coding: utf-8 -*-

import json
from datetime import datetime
from scrapy import Request
from news_all.spider_models import NewsRSpider


class YscjSpider(NewsRSpider):
    """央视财经 app"""
    name = 'yscj_app'
    
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    
    mystart_urls = {
        'https://a0.news.ghwx.com.cn/server/article/list?gid=4616246792659402752&version=1.1&page=0&isParent=1&pageSize=5&sf=': 390,
        'https://a0.news.ghwx.com.cn/server/article/list?gid=4616752568008179712&version=1.1&page=0&isParent=1&pageSize=5&sf=': 396,
        'https://a0.news.ghwx.com.cn/server/article/load?aid=6226238458636010496': 407,
        'https://a0.news.ghwx.com.cn/server/article/list?version=1.1&gid=4616756966054690816&page=0&pageSize=1&sf=': 410,
        'https://a0.news.ghwx.com.cn/server/article/list?gid=4616761364101201920&version=1.1&page=0&isParent=1&pageSize=8&sf=': 412,
        'https://a0.news.ghwx.com.cn/server/article/list?version=1.1&gid=4616941684008157184&page=0&pageSize=10&sf=': 414,
        'https://a0.news.ghwx.com.cn/server/article/list?gid=4616827334798868480&version=1.1&page=0&isParent=1&pageSize=3&sf=': 423,
        'https://a0.news.ghwx.com.cn/server/article/list?version=1.1&gid=4616831732845379584&page=0&pageSize=10&sf=': 428,
        'https://a0.news.ghwx.com.cn/server/article/list?gid=4616915295729090560&version=1.1&page=0&isParent=1&pageSize=5&sf=': 434,
        'https://a0.news.ghwx.com.cn/server/article/list?gid=4616919693775601664&version=1.1&page=0&isParent=1&pageSize=5&sf=': 437,
        'https://a0.news.ghwx.com.cn/server/article/list?version=1.1&gid=4616928489868623872&page=0&pageSize=10&sf=': 444,
        'https://a0.news.ghwx.com.cn/server/article/list?version=1.1&gid=4616198414147780608&page=0&pageSize=10&sf=': 446,
        'https://a0.news.ghwx.com.cn/server/article/list?version=1.1&gid=4616202812194291712&page=0&pageSize=10&sf=': 448,
        'https://a0.news.ghwx.com.cn/server/article/list?version=1.1&gid=4616207210240802816&page=0&pageSize=10&sf=': 456,
        'https://a0.news.ghwx.com.cn/server/article/list?version=1.1&gid=4616211608287313920&page=0&pageSize=10&sf=': 508,
        'https://a0.news.ghwx.com.cn/server/article/list?version=1.1&gid=4616216006333825024&page=0&pageSize=10&sf=': 515,
        'https://a0.news.ghwx.com.cn/server/article/list?version=1.1&gid=4616224802426847232&page=0&pageSize=10&sf=': 520,
        'https://a0.news.ghwx.com.cn/server/article/list?version=1.1&gid=4616836130891890688&page=0&pageSize=10&sf=': 521,
    }


    def parse(self, response):
        rj = json.loads(response.text)
        result = rj.get('list')
        
        for i in result:
            url = i.get("urlShare")

            title = i.get("title")
            origin_name = i.get("from")
            pubtime = i.get("orderTime")
            yield Request(
                url=url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'],
                      # 新闻详情页必须用浏览器渲染
                      # 比如https://s0.news.ghwx.com.cn/a.html?aid=6252889437907190784&gid=4616836130891890688
                      'jstype': True,
                      'title': title,
                      'pubtime': pubtime,
                      "origin_name": origin_name,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )
   
    def parse_item(self, response):
        try:
            content_div = response.xpath('//div[@class="content white"]')[0]
            # 过滤视频

        except Exception as e:
            return self.produce_debugitem(response, "xpath error")
        
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