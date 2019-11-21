#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 17:47
# @Author  : wjq
# @File    : enorth.py

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class EnorthSpider(NewsRCSpider):
    """北方网"""
    name = 'enorth'
    mystart_urls = {
        'http://sports.enorth.com.cn/gnzt/zhongchao/': 16113,  # 北方网-体育-国内足坛-右侧列表采集
        
        'http://ent.enorth.com.cn/star/neidi/index.htm': 16109,  # 北方网-文娱-内地明星-全部列表采集
        'http://ent.enorth.com.cn/music/huayu/index.htm': 16112,  # 北方网-文娱-华语乐坛-全部列表采集
        'http://ent.enorth.com.cn/star/gangtai/index.htm': 16110,  # 北方网-文娱-港台明星
        
        'http://fashion.enorth.com.cn/mtss/jfcl/index.shtml': 16125,  # 北方网-时尚-减肥
        'http://fashion.enorth.com.cn/blmf/czmq/index.shtml': 16122,  # 北方网-时尚-彩妆
        'http://fashion.enorth.com.cn/blmf/hfzx/index.shtml': 16121,  # 北方网-时尚-护肤
        'http://fashion.enorth.com.cn/yrfs/mxzb/index.shtml': 16119,  # 北方网-时尚-明星-右侧列表抓取
        'http://fashion.enorth.com.cn/nrbl/nrx/index.shtml': 16130,  # 北方网-时尚-男人型
        'http://fashion.enorth.com.cn/blmf/sfsk/index.shtml': 16123,  # 北方网-时尚-秀发
        'http://fashion.enorth.com.cn/yrfs/nsyy/index.shtml': 16117,  # 北方网-时尚-霓裳-右侧
        'http://fashion.enorth.com.cn/blmf/xfgc/index.shtml': 16124,  # 北方网-时尚-香芬
        'http://ms.enorth.com.cn/': 1201028,  # 北方网-民生频道-除去右下块全部抓取
        
    }
    rules = (
        # http://sports.enorth.com.cn/system/2019/06/19/037358842.shtml
        # http://ent.enorth.com.cn/system/2019/06/14/037344499.shtml
        # http://fashion.enorth.com.cn/system/2019/06/19/037357568.shtml
        # http://ms.enorth.com.cn/system/2019/06/21/037368127.shtml
        Rule(LinkExtractor(
            allow=(r'enorth.com.cn/system/%s/\d{2}/\d+.s?htm' % datetime.today().strftime('%Y/%m'),),
            # deny=(r'',)
        ),
            callback='parse_item', follow=False),
        
        Rule(LinkExtractor(
            allow=(r'enorth.com.cn.*?\d+.s?htm',),
            deny=(r'/201[0-8]', r'/2019/0[1-9]', r'/2019-0[1-9]', r'/2019_0[1-9]', r'/20190[1-9]', '/index.htm')
        ),
            process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            sidv = xp('//*[@class="col-sm-8 info"]')[0]
            pubtime = sidv.re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')[0]  # 2019-02-22 14:55:11
            og = sidv.re(r'来源：\s?\w+')
            origin_name = og[0] if og else ""
            content_div = xp('//div[@class="content"]')[0]
            content, media, _, _ = self.content_clean(content_div)
        except BaseException:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('-')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
