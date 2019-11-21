#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/1
# @Author  : wjq


from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class ChinadailyAllSpider(NewsRCSpider):
    """中国日报"""
    name = 'chinadaily_all'
    
    mystart_urls = {
        'http://world.chinadaily.com.cn/5bda6641a3101a87ca904fe6': 1316,
        'http://world.chinadaily.com.cn/5bd55927a3101a87ca8ff616': 1317,
        'http://world.chinadaily.com.cn/5bd55927a3101a87ca8ff614': 1318,
        'http://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5bd54dd6a3101a87ca8ff5f8': 1319,
        'http://pic.chinadaily.com.cn/': 1320, 'http://cn.chinadaily.com.cn/yuanchuang/': 1321,
        'http://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff62e': 1322,
        'https://world.chinadaily.com.cn/5bd55927a3101a87ca8ff616': 1323,
        'http://caijing.chinadaily.com.cn/5b761fc9a310030f813cf44d': 1324,
        'http://caijing.chinadaily.com.cn/finance': 1325,
        'http://caijing.chinadaily.com.cn/5b762029a310030f813cf44f': 1326,
        'http://caijing.chinadaily.com.cn/5b7620d3a310030f813cf453': 1327,
        'http://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5bd54ba2a3101a87ca8ff5ee/5bd54bdea3101a87ca8ff5f4': 1328,
        'http://finance.chinadaily.com.cn/': 1329, 'http://cnews.chinadaily.com.cn/5b8f78eba310030f813ed4d0': 1330,
        'http://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5bd54dd6a3101a87ca8ff5f6/5bd54e0aa3101a87ca8ff600': 1331,
        'https://fashion.chinadaily.com.cn/5b762404a310030f813cf462': 1332,
        'http://fashion.chinadaily.com.cn/5b762404a310030f813cf468': 1344,
        'http://fashion.chinadaily.com.cn/5b762404a310030f813cf463': 1345,
        'http://fashion.chinadaily.com.cn/5b762404a310030f813cf469': 1346,
        'http://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5bd54ba2a3101a87ca8ff5ee/5bd54bdea3101a87ca8ff5f0': 1347,
        'https://world.chinadaily.com.cn/5bd55927a3101a87ca8ff618': 1348, 'http://world.chinadaily.com.cn/': 1350,
        'https://fashion.chinadaily.com.cn/5b762404a310030f813cf461': 1351,
        'https://fashion.chinadaily.com.cn/5b762404a310030f813cf468': 1352,
        'https://fashion.chinadaily.com.cn/5b762404a310030f813cf467': 1353,
        'http://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5bd549f1a3101a87ca8ff5e4': 1354,
        'https://fashion.chinadaily.com.cn/5b762404a310030f813cf469': 1355,
        'http://cn.chinadaily.com.cn/lvyou/5bac7d20a3101a87ca8ff52d': 1356,
        'http://cn.chinadaily.com.cn/lvyou/5b7628c6a310030f813cf48c': 1357,
        'http://cn.chinadaily.com.cn/lvyou/5b7628c6a310030f813cf493': 1358,
        'http://cn.chinadaily.com.cn/lvyou/5b7628c6a310030f813cf492': 1359,
        'http://cn.chinadaily.com.cn/lvyou/5b7628c6a310030f813cf48a': 1360,
        'http://cn.chinadaily.com.cn/jiankang': 1361,
        'http://cn.chinadaily.com.cn/lvyou/5b7628c6a310030f813cf48f': 1362,
        'https://ent.chinadaily.com.cn/5b761f98a310030f813cf441': 1363,
        'https://ent.chinadaily.com.cn/5b761f98a310030f813cf44a': 1364,
        'https://ent.chinadaily.com.cn/5b8f7721a310030f813ed4c6': 1365,
        'http://ent.chinadaily.com.cn/5b8f7721a310030f813ed4c6': 1366,
        'https://ent.chinadaily.com.cn/5b761f98a310030f813cf445': 1367,
        'http://ent.chinadaily.com.cn/5b761f98a310030f813cf441': 1368,
        'https://ent.chinadaily.com.cn/5b761f98a310030f813cf43f': 1369,
        'http://ent.chinadaily.com.cn/5b761f98a310030f813cf442': 1370,
        'http://ent.chinadaily.com.cn/5b761f98a310030f813cf44a': 1371,
        'https://ent.chinadaily.com.cn/5b761f98a310030f813cf440': 1372,
        'http://ent.chinadaily.com.cn/5b761f98a310030f813cf443': 1373,
        'http://che.chinadaily.com.cn/5b8f780ea310030f813ed4ca': 1374,
        'http://finance.chinadaily.com.cn/5b9799c1a310f8f8a09b240b': 1375,
        'http://finance.chinadaily.com.cn/5b761ef4a310030f813cf43e': 1376,
        'http://finance.chinadaily.com.cn/5b761e81a310030f813cf438': 1377,
        'http://finance.chinadaily.com.cn/5b761ea4a310030f813cf439': 1378,
        'http://finance.chinadaily.com.cn/5b8f7837a310030f813ed4cc': 1379,
        'http://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5bd54dd6a3101a87ca8ff5f6': 1380,
        'http://tech.chinadaily.com.cn/5b762186a310030f813cf457': 1381,
        'http://ent.chinadaily.com.cn/5b761f98a310030f813cf43f': 1382,
        'http://qiye.chinadaily.com.cn/5bac42f8a3101a87ca8feb34': 1383,
        'http://qiye.chinadaily.com.cn/5b7627bba310030f813cf480': 1384,
        'http://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff634/5bd5669ba3101a87ca8ff662': 1385,
        'http://qiye.chinadaily.com.cn/5b7627bba310030f813cf485': 1386,
        'https://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff62e': 1387,
        'http://china.chinadaily.com.cn/theory/5bd56628a3101a87ca8ff656': 1388,
        'http://tech.chinadaily.com.cn/5b8f760ea310030f813ed4c4': 1389,
        'http://chuangxin.chinadaily.com.cn/5b754389a310030f813cf427': 1390,
        'http://chuangxin.chinadaily.com.cn/5b75433ea310030f813cf423': 1391,
        'http://chuangxin.chinadaily.com.cn/5b754361a310030f813cf425': 1392,
        'http://chuangxin.chinadaily.com.cn/5b7543b6a310030f813cf429': 1393,
        'http://chuangxin.chinadaily.com.cn/5b7542d1a310030f813cf41f': 1394,
        'https://caijing.chinadaily.com.cn/5b7620c4a310030f813cf452': 1395,
        'https://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff636': 1396,
        'http://fj.chinadaily.com.cn/5bd5875fa3101a87ca8ff77c': 1397,
        'https://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5bd549f1a3101a87ca8ff5e4': 1398,
        'https://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5bd54ba2a3101a87ca8ff5ee/5bd54bdea3101a87ca8ff5f0': 1399,
        'https://column.chinadaily.com.cn/': 1400,
        'http://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5b940cbaa310030f813ed4d7/5bd5487ea3101a87ca8ff5ce': 1401,
        'https://caijing.chinadaily.com.cn/finance/': 1402,
        'https://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5b940cbaa310030f813ed4d7/5bd5487ea3101a87ca8ff5ce': 1403,
        'https://tech.chinadaily.com.cn/5b762218a310030f813cf45f': 1404,
        'https://chuangxin.chinadaily.com.cn/5b7543b6a310030f813cf429': 1405,
        'https://cnews.chinadaily.com.cn/5bd5693aa3101a87ca8ff676': 1406,
        'https://finance.chinadaily.com.cn/5b761ea4a310030f813cf439': 1407,
        'https://finance.chinadaily.com.cn/5b761e81a310030f813cf438': 1408,
        'https://finance.chinadaily.com.cn/5b761ef4a310030f813cf43e': 1409,
        'https://finance.chinadaily.com.cn/5b9799c1a310f8f8a09b240b': 1410,
        'https://ent.chinadaily.com.cn/5b761f98a310030f813cf443': 1411,
        'http://ent.chinadaily.com.cn/5b761f98a310030f813cf445': 1412,
        'https://cn.chinadaily.com.cn/lvyou/5b7628c6a310030f813cf48a': 1413,
        
        # 4月22日 采风整理亿媒的
        'http://column.chinadaily.com.cn/5bea245ea3101a87ca925fbb/5bea2544a3101a87ca925ff8': 1831,
        'http://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff634': 1832,
        'http://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5bd54dd6a3101a87ca8ff5f8/5bd54e59a3101a87ca8ff606': 1833,
        'http://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff636': 1834,
        'http://ent.chinadaily.com.cn/5b761f98a310030f813cf446': 1835,
        'http://fang.chinadaily.com.cn/5b75426aa310030f813cf41c': 1836,
        'http://cnews.chinadaily.com.cn/5bd5693aa3101a87ca8ff676': 1837,
        'http://chuangxin.chinadaily.com.cn/5b754352a310030f813cf424': 1838,
        'http://fashion.chinadaily.com.cn/5b8f77a7a310030f813ed4c8': 1839,
        'http://finance.chinadaily.com.cn/5b761eb1a310030f813cf43a': 1840,
        'http://chuangxin.chinadaily.com.cn/5b754372a310030f813cf426': 1841,
        'http://column.chinadaily.com.cn/': 1842,
        'http://world.chinadaily.com.cn/5bd55927a3101a87ca8ff616/5bd559a9a3101a87ca8ff620': 1843,
        'http://fang.chinadaily.com.cn/5b75426aa310030f813cf418': 1844,
        # 'https://language.chinadaily.com.cn/news_hotwords/': 1845,
        'http://column.chinadaily.com.cn/allarticle': 1846,
        'http://column.chinadaily.com.cn/5bea245ea3101a87ca925fbb/5bea2544a3101a87ca926000': 1847,
        'http://column.chinadaily.com.cn/5bea245ea3101a87ca925fbb/5bea2544a3101a87ca925ffa': 1848,
        'http://column.chinadaily.com.cn/5bea245ea3101a87ca925fbb/5bea2544a3101a87ca925ff2': 1849,
        'http://column.chinadaily.com.cn/5bea245ea3101a87ca925fbb/5c467176a31010568bdc599b': 1850,
        'http://china.chinadaily.com.cn/theory/5bd56628a3101a87ca8ff65c': 1851,
        'http://world.chinadaily.com.cn/5bd55927a3101a87ca8ff616/5bd559a9a3101a87ca8ff61e': 1852,
        'http://column.chinadaily.com.cn/5bea245ea3101a87ca925fbb/5bea2544a3101a87ca925ffe': 1853,
        'http://china.chinadaily.com.cn/theory/5bd56628a3101a87ca8ff654': 1854,
        'http://tech.chinadaily.com.cn/5b762218a310030f813cf45f': 1855,
        # 'https://language.chinadaily.com.cn/trans_collect/': 1856,
        'http://column.chinadaily.com.cn/5bea245ea3101a87ca925fbb/5bea2544a3101a87ca925ff6': 1857,
        'http://cn.chinadaily.com.cn/lvyou/5b7628dfa310030f813cf495': 1858,
        'http://cnews.chinadaily.com.cn/5bd5693aa3101a87ca8ff67a': 1859,
        'http://fang.chinadaily.com.cn/5b75426aa310030f813cf41d': 1860,
        # 'https://language.chinadaily.com.cn/5af95d44a3103f6866ee845c/': 1861,
        'http://china.chinadaily.com.cn/theory/5bd56628a3101a87ca8ff65a': 1862,
        'http://ent.chinadaily.com.cn/5b761f98a310030f813cf444': 1863,
        'http://caijing.chinadaily.com.cn/5b7620c4a310030f813cf452': 1864,
        'http://fang.chinadaily.com.cn/5b75426aa310030f813cf416': 1865,
        'http://world.chinadaily.com.cn/5bd55927a3101a87ca8ff618': 1866,
        'http://fashion.chinadaily.com.cn/5b762404a310030f813cf461': 1867,
        'http://fashion.chinadaily.com.cn/5b762404a310030f813cf467': 1868,
        'http://finance.chinadaily.com.cn/5b761ed0a310030f813cf43c': 1869,
        'http://fang.chinadaily.com.cn/5b75426aa310030f813cf419': 1870,
        # 'https://language.chinadaily.com.cn/practice_tongue/': 1871,  # 英文不要
        'http://column.chinadaily.com.cn/authorlist/zhanzhang': 1872,
        # 'https://language.chinadaily.com.cn/news_bilingual/': 1873,  # 英文不要
        'http://world.chinadaily.com.cn/5bd55927a3101a87ca8ff610': 1874,
        'http://cnews.chinadaily.com.cn/5bd5696ea3101a87ca8ff680': 1875,
        'http://column.chinadaily.com.cn/5bea245ea3101a87ca925fbb/5bea2544a3101a87ca925ffc': 1876,
        'http://china.chinadaily.com.cn/theory/5bd56628a3101a87ca8ff65e': 1877,
        'http://world.chinadaily.com.cn/5bd55927a3101a87ca8ff616/5bd559a9a3101a87ca8ff61c': 1878
    }
    
    rules = (
        # http://china.chinadaily.com.cn/a/201903/31/WS5ca06f73a310e7f8b1573a7b.html
        Rule(LinkExtractor(allow=(r'chinadaily.com.cn/a/%s/\d{2}/\w{26}.html' % datetime.today().strftime('%Y%m'),),
                           # 排除英语/视频
                           deny=(r'language.chinadaily.com.cn', r'kan.chinadaily.com.cn')),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'chinadaily.com.cn/.*?/\w{26}.html',),
                           deny=(r'language.chinadaily.com.cn', r'kan.chinadaily.com.cn', r'/201[0-8]', r'/20190[1-9]/')),
             process_request=otherurl_meta, follow=False),
    )
    from scrapy.conf import settings
    from copy import deepcopy
    custom_settings = {
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    def parse_item(self, response):
        xp = response.xpath
        try:
            content_div = xp('.//div[@id="Content"]')[0]
            source_div = xp('.//div[@class="fenx"]')[0]
            op = source_div.xpath('./div[1]/text()').re('来源：(\w{2,})')
            origin_name = op[0].strip() if op else ""
            pubtime = source_div.xpath('./div[2]/text()').extract_first('').strip() or source_div.xpath(
                './div[1]/text()').extract_first('').strip()
        except Exception as e:
            return self.parse_item_2(response)
        

            
        title = xp('.//*[@class="dabiaoti"]/text()').extract_first('') or self.get_page_title(response).split('-')[0]
        
        next_a = xp('//div[@id="div_currpage"]//a[contains(text(), "下一页")]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         })
        content, media, videos, video_cover = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item_2(self, response):
        xp = response.xpath
        try:
            content_div = xp('.//div[@class="article"]')[0]
            source_div = xp('.//div[@class="fenx"]')[0]
            pubtime = source_div.xpath('./div[2]/text()').extract_first('').strip() or source_div.xpath(
                './div[1]/text()').extract_first('').strip()
        except:
            return self.produce_debugitem(response, "xpath error")
        

        
        title = xp('.//*[@class="dabiaoti"]/text()').extract_first('') or self.get_page_title(response).split('-')[
            0]
        
        next_a = xp('//div[@id="div_currpage"]//a[contains(text(), "下一页")]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': "中国日报网",
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         })
        content, media, videos, video_cover = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="中国日报网",
            content=content,
            media=media
        )
    
    def parse_page(self, response):
        xp = response.xpath
        meta_new = deepcopy(response.meta)
        
        try:
            content_div = xp('.//div[@id="Content" or @class="article"]')[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()
        
        next_a = xp('//div[@id="div_currpage"]//a[contains(text(), "下一页")]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
        
        content, media, videos, video_cover = self.content_clean(meta_new['content'],
                                                                 kill_xpaths='//div[@id="div_currpage"]')
        
        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),
            content=content,
            media=media
        )