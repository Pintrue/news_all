#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 18:54
# @Author  : wjq
# @File    : sina_all.py
import json
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, isStartUrl_meta, otherurl_meta


class SinaMilSpider(NewsRCSpider):
    chinese_name = """新浪军事"""
    name = 'sina_mil'
    mystart_urls = {
        'http://mil.news.sina.com.cn/roll/index.d.html?cid=57918': 2576,
        'http://mil.news.sina.com.cn/roll/index.d.html?cid=57919': 2577,
        'https://mil.news.sina.com.cn/jssd/': 2578,
        'http://mil.news.sina.com.cn/dgby/': 2579,
        'http://mil.news.sina.com.cn/jshm/': 2580,
    }
    
    # https://mil.news.sina.com.cn/2019-05-22/doc-ihvhiews3686776.shtml
    # https://mil.news.sina.com.cn/2019-05-23/doc-ihvhiews4107741.shtml
    # https://mil.news.sina.com.cn/world/2019-05-24/doc-ihvhiqay0981240.shtml
    # https://mil.news.sina.com.cn/2019-05-24/doc-ihvhiews4165207.shtml
    y, m, d = datetime.today().strftime('%Y-%m-%d').split('-')

    rules = (
        Rule(LinkExtractor(allow=(r'mil.news.sina.com.cn.*?/%s-%s-\d{2}/doc-\w+\d+.s?htm' % (y, m)),
                           # restrict_xpaths=r'//div[@class="fixList"]/ul/li/span[contains(text(), "%s月")]/parent::li' % m
                           ),
             callback='parse_item', follow=False),
        # <a title="下一页" href="http://mil.news.sina.com.cn/roll/index.d.html?cid=57919&amp;page=2">下一页</a>
        Rule(LinkExtractor(allow=(r'mil.news.sina.com.cn/roll/index.d.html'), deny=r'page=[5-9]',
                           restrict_xpaths=r'//*[@id="_function_code_page"]//a[@title="下一页"]'),
             follow=True, process_request=isStartUrl_meta, callback='pp'),
        Rule(LinkExtractor(allow=(r'sina.com.cn.*?\d+.s?htm'), deny=(r'/201[0-8]', r'/2019-0[1-8]-',),
                           # restrict_xpaths=r'//div[@class="fixList"]/ul/li/span[contains(text(), "%s月")]/parent::li' % m,
                           ),
                           process_request=otherurl_meta, follow=False),
             )

    custom_settings = {
        'DEPTH_LIMIT': 3,
    }

    def parse_item(self, response):
        xp = response.xpath
        try:
            ps = xp('//div[@class="date-source"]/span[@class="date"]/text()') or xp('//span[@id="pub_date"]/text()')
            pubtime = ps[0].extract().strip()
            og = xp('//div[@class="date-source"]/*[@class="source"]//text()').extract()
            #  http://tech.sina.com.cn/csj/2019-05-24/doc-ihvhiews4176899.shtml
            #  xp('/html/head/meta[@name="mediaid"]/@content').extract()
            if og:  # ['   ']
                og = og[0].split()
            origin_name = og[0].split()[0] if og else '新浪网'
            cvs = xp('//div[@id="artibody"]') or xp('//div[@id="article"]')
            content_div = cvs[0]
            # <meta property="og:title" content="直击|OYO发布2.0战略 目标成为全球最大连锁酒店集团">
            title = xp('/html/head/meta[@property="og:title"]/@content').extract_first('') or xp(
                '//*[@class="main-title"]/text()').extract_first('') or xp('//h1/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content_div,
                                                                 kill_xpaths=[r'//*[@id="sinaadsInsId"]', ])

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )


class SinaTechSpider(SinaMilSpider):
    """新浪科技"""
    name = 'sina_tech'
    mystart_urls = {
        'https://tech.sina.com.cn/internet/': 2600,
        'http://tech.sina.com.cn/chuangshiji/': 2623,
        'http://tech.sina.com.cn/apple/': 2624,
        'http://tech.sina.com.cn/apple/iphone/': 2625,
        'http://tech.sina.com.cn/apple/ipad/': 2626,
        'http://tech.sina.com.cn/apple/applewatch/': 2627,
        'http://tech.sina.com.cn/apple/mac/': 2628,
        'http://tech.sina.com.cn/apple/inc/': 2629,
        'https://tech.sina.com.cn/tele/': 2630,
        'https://tech.sina.com.cn/it/': 2631,
        'http://digi.sina.com.cn/': 2632,
        'http://tech.sina.com.cn/elec/': 2633,
        'http://chuangye.sina.com.cn/': 2634,
    }
    # https://tech.sina.com.cn/it/2019-05-24/doc-ihvhiqay1058182.shtml
    # http://tech.sina.com.cn/csj/2019-05-24/doc-ihvhiews4225019.shtml
    # https://tech.sina.com.cn/mobile/n/n/2019-05-21/doc-ihvhiews3366322.shtml
    y, m, d = datetime.today().strftime('%Y-%m-%d').split('-')

    rules = (
        Rule(LinkExtractor(allow=(r'tech.sina.com.cn.*?/%s-%s-\d{2}/doc-\w+\d+.s?htm' % (y, m)),
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'sina.com.cn.*?\d+.s?htm'), deny=(r'/201[0-8]', r'/2019-0[1-8]-',),
                           ),
                           process_request=otherurl_meta, follow=False),
             )


class SinaRollSpider(SinaMilSpider):
    """新浪 列表页js新闻"""
    # https://feed.sina.com.cn/api/roll/get?pageid=106&lid=1237&num=30&versionNumber=1.2.4&page=1&encode=utf-8&callback=feedCardJsonpCallback&_=1558699740296
    name = "sina_roll"
    mystart_urls = {
        # 'http://tech.sina.com.cn/roll/#pageid=372&lid=2431&k=&num=50&page=1': 2635,
        # 'http://ent.sina.com.cn/rollnews.shtml#pageid=382&lid=2990&k=&num=50&page=1': 2636,
        'http://ent.sina.com.cn/hollywood/': 2648,
        'https://ent.sina.com.cn/film/': 2655,
    }
    
    #  todo <200 http://tech.sina.com.cn/roll/> res.headers['Etag'] = [b'"5c3dbf0e-1ec4"V=CCD0B746']
    y, m, d = datetime.today().strftime('%Y-%m-%d').split('-')

    rules = (
        Rule(LinkExtractor(allow=(r'sina.com.cn.*?/%s-%s-\d{2}/doc-\w+\d+.s?htm' % (y, m)),
                           ),
             callback='parse_item', follow=False),

        Rule(LinkExtractor(allow=(r'sina.com.cn.*?\d+.s?htm'), deny=(r'/201[0-8]', r'/2019-0[1-8]-',),
                           ),
                           process_request=otherurl_meta, follow=False),
             )

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }
    }
    start_meta = {'jstype': True}


class SinaEntSpider(SinaMilSpider):
    """新浪娱乐"""
    name = 'sina_ent'
    mystart_urls = {
        'https://ent.sina.com.cn/korea/': 2652,
        'https://ent.sina.com.cn/zongyi/': 2653,
        'https://ent.sina.com.cn/tv/': 2654,
        'https://ent.sina.com.cn/star/': 2656,
    }
    
    y, m, d = datetime.today().strftime('%Y-%m-%d').split('-')
    # # https://ent.sina.com.cn/s/h/2019-05-24/doc-ihvhiqay1144077.shtml
    rules = (
        Rule(LinkExtractor(allow=(r'ent.sina.com.cn.*?/%s-%s-\d{2}/doc-\w+\d+.s?htm' % (y, m)),
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'sina.com.cn.*?\d+.s?htm'), deny=(r'/201[0-8]', r'/2019-0[1-8]-',),
                           ),
                           process_request=otherurl_meta, follow=False),
             )


class SinaSlideSpider(NewsRCSpider):
    """新浪 图集"""
    name = 'sina_slide'
    mystart_urls = {
        'http://slide.ent.sina.com.cn/': 2637, 'http://slide.ent.sina.com.cn/star/': 2638,
        'http://slide.ent.sina.com.cn/film/': 2639, 'http://slide.ent.sina.com.cn/tv/': 2640,
        'http://slide.ent.sina.com.cn/y/': 2646,
    }

    rules = (
        # http://slide.ent.sina.com.cn/film/h/slide_4_704_314650.html#p=1
        Rule(LinkExtractor(allow=(r'slide.ent.sina.com.cn.*?_\d+.s?htm'),
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'sina.com.cn.*?\d+.s?htm'), deny=(r'/201[0-8]', r'/2019-0[1-8]-',),
                           ),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            ss = xp('//script[contains(text(), "var slide_data")]/text()')[0].extract()
            start = ss.index('{"slide":')
            end = ss.index('\n      var ARTICLE_DATA')
            rj = json.loads(ss[start:end])  # 去最后
            pubtime = rj.get('slide').get('createtime')
            content_div = rj.get('images')
            content, media = self.make_img_content(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=rj.get('slide').get('title').replace('_高清图集_新浪网', ''),
            pubtime=pubtime,
            origin_name="",
            content=content,
            media=media
        )

    def make_img_content(self, img_cons):
        """
        拼接图、文列表为html
        """
        media = {'images': {}}
        content = ''
        for i, j in enumerate(img_cons):
            content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
            if j.get('intro'):
                content += '<p>' + j['intro'] + '</p>'

            media['images'][str(i + 1)] = {"src": j['image_url']}

        return content, media
