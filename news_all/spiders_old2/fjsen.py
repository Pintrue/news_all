#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 17:08
# @Author  : wjq
# @File    : fjsen.py


from copy import deepcopy
from datetime import datetime
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class FjsenSpider(NewsRCSpider):
    """东南网"""
    name = 'fjsen'
    mystart_urls = {
        'http://news.fjsen.com/node_112576.htm': 1301151,  # 东南网 国内足球-左侧列表
        'http://news.fjsen.com/node_112575.htm': 1301150,  # 东南网 国际足球-左侧列表
        'http://news.fjsen.com/node_173141.htm': 1301377,  # 东南网 影视列表
        'http://money.fjsen.com/HotFinance.htm': 1301375,  # 东南网 经济要闻
        'http://news.fjsen.com/node_173144.htm': 1301376,  # 东南网 音乐新闻
        'http://taihai.fjsen.com/node_144482.htm': 16167,  # 东南网-台海-时政
        'http://taihai.fjsen.com/Cross-strait.htm': 16170,  # 东南网-台海-海峡两岸
        'http://taihai.fjsen.com/node_10480.htm': 16166,  # 东南网-台海-热点推荐
        'http://taihai.fjsen.com/node_144481.htm': 16169,  # 东南网-台海-社会
        'http://taihai.fjsen.com/node_144484.htm': 16168,  # 东南网-台海-闽台往来
        'http://news.fjsen.com/node_2141.htm': 16173,  # 东南网-国内-即时新闻
        'http://news.fjsen.com/node_94858.htm': 16172,  # 东南网-国内-国内要闻-左侧
        'http://news.fjsen.com/e_news.htm': 16174,  # 东南网-国际-国际要闻-左侧
        'http://news.fjsen.com/W_Comments.htm': 16175,  # 东南网-国际-评论
    }
    
    from scrapy.conf import settings
    from copy import deepcopy
    custom_settings = {
        'DEPTH_LIMIT': 0,  # 若翻页则需要设置深度为0
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))  # 禁止重定向
    }
    
    rules = (
        # http://taihai.fjsen.com/2019-06/21/content_22418722.htm
        # http://news.fjsen.com/2019-06/21/content_22421496.htm
        # http://news.fjsen.com/2019-06/21/content_22419437.htm
        # http://news.fjsen.com/2019-06/21/content_22419035.htm
        Rule(LinkExtractor(
            allow=(r'fjsen.com/%s/\d{2}/content_\d+.htm' % datetime.today().strftime('%Y-%m'),),
            # deny=(r'',)
        ),
            callback='parse_item', follow=False),
        
        Rule(LinkExtractor(
            allow=(r'fjsen.com.*?\d+.htm',),
            deny=(r'/201[0-8]', r'/20190[1-9]/', r'/2019-0[1-9]', r'/2019_0[1-5]', r'/20190[1-9]/', '/index.htm',
                  r'/node_\d+',)
        ),
            process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            pubtime = xp(r'.//span[@id="pubtime_baidu"]/text()')[0].extract().strip()
            pubtime = re.sub('\s+', ' ', pubtime) # '2019-06-21   07:29:26'
            og = xp('.//span[@id="source_baidu"]//text()')
            origin_name = og[-1].extract() if og else ""
            cvs = xp('//div[@class="cont-news"]') or xp('//div[@class="content"]/div[@id="zoom"]') or xp(
                '//div[@class="left"]/div[@class="zw"]') or xp('//div[@class="content"]/div[@class="big"]/div[@id="zoom"]')
            content_div = cvs[0]
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")
        title = self.get_page_title(response).split('-')[0]
        next_a = xp('//div[@id="displaypagenum"]/center/a[text()="下一页"]')
        if next_a:
            return response.follow(next_a[0],
                                   callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         }
                                   )
        
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_page(self, response):
        meta_new = deepcopy(response.meta)
        xp = response.xpath
        try:
            cvs = xp('//div[@class="cont-news"]') or xp('//div[@class="content"]/div[@id="zoom"]') or xp(
                '//div[@class="left"]/div[@class="zw"]') or xp('//div[@class="content"]/div[@class="big"]/div[@id="zoom"]')
            content_div = cvs[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()
        next_a = xp('//div[@id="displaypagenum"]/center/a[text()="下一页"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
    
        content, media, _, _ = self.content_clean(meta_new['content'], kill_xpaths=['//div[@id="displaypagenum"]', ])
    
        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),
            content=content,
            media=media
        )
