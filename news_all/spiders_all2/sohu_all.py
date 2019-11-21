#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 18:54
# @Author  : wjq
# @File    : sohu_all.py


from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from news_all.tools.html_clean import img_fn


class SohuAllSpider(NewsRCSpider):
    chinese_name = """搜狐网站"""
    name = 'sohu_all'
    mystart_urls = {
        'http://yule.sohu.com/?spm=smpc.ch19.ctag.2.1558405481560rflPHpK': 2666,
        'http://yule.sohu.com/1406?spm=smpc.ch19.ctag.15.1558405545985QbROuYl': 2671,
        'http://yule.sohu.com/1408': 2676,
        'http://yule.sohu.com/1409': 2678,
        'http://yule.sohu.com/1410': 2679,
        'http://yule.sohu.com/1407': 2680,
    }

    rules = (
        # sohu.com/picture/316181594
        Rule(LinkExtractor(allow=(r'sohu.com/picture/\d+'), deny=r'mp.sohu.com/profile'
                           # restrict_xpaths=r''
                           ),
             callback='parse_images', follow=False),
        # http://www.sohu.com/a/316696471_114941?scm=1002.280027.0.0-0&spm=smpc.ch19.fd.4.1558947736962IouRb2Q
        # http://www.sohu.com/a/316775708_534591
        Rule(LinkExtractor(allow=(r'sohu.com/a/'), deny=r'mp.sohu.com/profile'
                           ),
             callback='parse_item', follow=False),

        Rule(LinkExtractor(allow=(r'sohu.com'), deny=(r'/201[0-8]', r'/20190[1-9]/', r'mp.sohu.com/profile'),
                           ),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            if "新闻已删除" in xp("//h1[@class='at-title']/text()").extract_first(''):
                return
            # <meta itemprop="datePublished" content="2019-05-27 10:10">
            pubtime = xp('//head/meta[@itemprop="datePublished"]/@content').extract_first('')
            origin_name = xp('//head/meta[@name="mediaid"]/@content').extract_first('')
            content_div = xp('//article[@id="mp-editor"]')[0]
            title = xp('//head/meta[@property="og:title"]/@content').extract_first('')
            title = title.split('_')[0] if title else xp('//h1/text()').extract_first('')
        except:
            return self.parse_item2(response)

        content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[r'//*[@class="backword"]',
                                                                                           r'//*[text()="返回搜狐，查看更多"]',
                                                                                           r'//*[text()="点击"]',
                                                                                           r'//*[text()="责任编辑："]',
                                                                                           r'//*[text()="责任编辑"]',
                                                                                           
                                                                 ])
        
        return self.produce_item(
            response=response,
            title=title or self.get_page_title(response).split('_')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item2(self, response):
        page_title = self.get_page_title(response)
        if page_title and '404 Not Found' in page_title:
            print('url: %s, 404 Not Found' % response.url)
            return
        xp = response.xpath

        try:
            pubtime = xp("//span[@class='at-time']/text()").extract_first()
            cvs = xp('//div[@class="at-cnt-main"]') or xp('//div[@class="at-content ui-cf"]')
            content_div = cvs[0].extract()
            origin_name = xp("//span[@class='at-media-name']/text()").extract_first()
            content, media, videos, video_cover = self.content_clean(content_div,
                                                                     kill_xpaths=['//*[text()="打开APP，查看更多精彩图片"]',
                                                                                  '//*[@id="at-img-all"]',
                                                                                  '//*[contains(text(),"展开全部")]',
                                                                                  '//*[contains(text(),"展开全文")]',
                                                                                  '//*[contains(text(), "打开搜狐新闻APP")]'
                                                                                  ])
        except:
            return self.parse_images(response)

        return self.produce_item(
            response=response,
            title=page_title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_images(self, response):
        xp = response.xpath
        try:
            pubtime = xp('//div[@class="info"]/*[@class="time"]/text()')[0].extract()
            origin_name = xp('//div[@class="info"]/*[@class="name"]/text()').extract_first('')
            imgs = xp('//div[@class="pic-area"]//img/@src').extract()
            ps = xp('//div[@class="pic-exp"]/div[@class="txt"]/p/text()').extract()
            content, media = self.img_cont(ps, imgs)
            title = xp('//*[@id="article-title-hash"]/text()').extract_first('')
        except BaseException:
            return self.produce_debugitem(response, "xpath error")
        
        return self.produce_item(
            response=response,
            title=title or self.get_page_title(response).split('-')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def img_cont(self, ps, img_list):
        # print('p len: %s, img len: %s' % (len(ps), len(img_list)))
        media = {"images": {}}
        new_content = ''

        for i, j in enumerate(img_list):
            new_content += '${{%s}}$' % (i + 1) + '<p>' + ps[i] + '</p>'
            media['images'][str(i + 1)] = {"src": img_fn(j)}

        new_content.replace('$$', '$<br>$')  # 连续2图片加换行
        return new_content, media
