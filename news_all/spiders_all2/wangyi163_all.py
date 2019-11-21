#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 18:54
# @Author  : wjq
# @File    : wangyi163_all.py
import json
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class WangyiAllSpider(NewsRCSpider):
    chinese_name = """网易网站"""
    name = 'wangyi163_all'
    mystart_urls = {
        'http://ent.163.com/special/star_news/': 2657,
        'http://ent.163.com/movie/': 2658,
        'http://ent.163.com/tv/': 2661,
        'http://ent.163.com/special/00032VQS/zongyijiemu.html': 2663,
        'http://music.ent.163.com/': 2665,
    }
        
    # https://ent.163.com/19/0528/08/EG8IJIO400038FO9.html
    # https://ent.163.com/19/0527/14/EG6IOJLE00037VVV.html
    # https://ent.163.com/19/0528/07/EG8EP0KT00038FO9.html
    y, m, d = datetime.today().strftime('%Y/%m/%d').split('/')
    rules = (
        Rule(LinkExtractor(allow=(r'ent.163.com/%s/%s\d{2}/\d{2}/\w{10,}.html' % (y[2:], m)),
                           # restrict_xpaths=r''
                           ),
             callback='parse_item', follow=False),
        # http://ent.163.com/photoview/00AJ0003/666112.html#p=EG63GI3P00AJ0003NOS
        Rule(LinkExtractor(allow=(r'ent.163.com/photoview/\w{6,}/\d+.html'),
                           # restrict_xpaths=r''
                           ),
             callback='parse_images', follow=False),
        Rule(LinkExtractor(allow=(r'ent.163.com'), deny=(r'/1[0-8]', r'/19/0[1-6]', r'ent.163.com/special/'),
                           # restrict_xpaths=r''
                           ),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            # <meta property="article:published_time" content="2019-05-27T12:03:53+08:00">
            # 2019-05-27 12:03:53
            ps = xp('//div[@class="post_time_source"]').re(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}(?:\d{2})?')
            pubtime = ps[0]
            origin_name = xp('//*[@id="ne_article_source"]/text()').extract_first('')
            content_div = xp('//div[@id="endText"]/p')
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[r'//img[contains(@alt, "公众号")]',
                                                                                           r'//img[contains(@title, "公众号")]',
                                                                                           r'//img[contains(@src, "rTya-fynmzun0700720.jpg")]',
                                                                                           ])

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('_')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    #  http://ent.163.com/photoview/00AJ0003/666112.html#p=EG63GI3P00AJ0003NOS

    def parse_images(self, response):
        xp = response.xpath
        try:
            content_div = xp('//textarea/text()')[0].extract()
            rj = json.loads(content_div)
            info = rj.get('info')
            pubtime = info.get('lmodify')
            img_count = info.get('imgsum')

            title = info.get('setname')
            origin_name = info.get("source")
            con_list = rj.get('list')
            content, media = self.img_cont(con_list)
            if len(media["images"]) != img_count:
                self.log("图片数量不符, url:%s" % response.url)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title or self.get_page_title(response).split('-')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def img_cont(self, con_list):
        media = {"images": {}}
        new_content = ''

        for i, j in enumerate(con_list):
            media["images"][str(i+1)] = {'src': j.get('img')}
            new_content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
            if j.get('title'):
                new_content += '<p>' + j['title'] + '</p>'
            if j.get('note'):
                new_content += '<p>' + j['note'] + '</p>'

        new_content.replace('$$', '$<br>$')  # 连续2图片加换行
        return new_content, media
