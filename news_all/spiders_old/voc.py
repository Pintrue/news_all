#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 10:54
# @Author  : wjq
# @File    : voc.py

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class VocSpider(NewsRCSpider):
    """华声在线"""
    name = 'voc'
    mystart_urls = {
        'http://news.voc.com.cn/class/1915.html': 1301435,  # 华声在线-有料
        'http://hssq.voc.com.cn/list.php?cid=2': 1301434,  # 华声在线-社区-左侧列表
    }
    
    rules = (
        # http://news.voc.com.cn/article/201906/201906231502051514.html
        # http://hssq.voc.com.cn/content-3764-2.html
        Rule(LinkExtractor(allow=(r'news.voc.com.cn/article/%s/\d+.htm' % datetime.today().strftime('%Y%m'),),
                           # deny=(r'',)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'hssq.voc.com.cn/content-\d+-\d+.htm',),
                           ),
             callback='parse_item_2', follow=False),
        Rule(LinkExtractor(allow=(r'voc.com.cn.*?\d+.htm',),
                           deny=(r'/201[0-8]', r'/2019/0[1-5]', r'/20190[1-5]', r'news.voc.com.cn/class/\d+')
                           ),
             process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            pubtime = xp('/html/head/meta[@name="publishdate"]/@content')[0].extract()
            
                
            content_div = xp('//div[@id="content"]')[0]
            origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first('')
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")
        
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=xp('//h1/text()').extract_first('') or self.get_page_title(response).split('-')[0],
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media
        )
    
    def parse_item_2(self, response):
        
        xp = response.xpath
        try:
            sdiv = xp('//div[@class="info"]')[0]
            pubtime = sdiv.xpath('./span[@id="pubtime_baidu"]/text()')[0].extract().strip()
            
                
            content_div = xp('//div[@class="news-editor"]')[0]
            origin_name = sdiv.xpath('./span[@id="source_baidu"]/text()').extract_first("")
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")
        
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=xp('//h1/text()').extract_first('') or self.get_page_title(response).split('-')[0],
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media
        )
