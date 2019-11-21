#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 18:54
# @Author  : wjq
# @File    : tmt_all.py


from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class TmtAllSpider(NewsRCSpider):
    chinese_name = """钛媒体网站"""
    name = 'tmt_all'
    mystart_urls = {
        'https://www.tmtpost.com/': 2588,
        'https://www.tmtpost.com/column/2446155': 2589,
        'https://www.tmtpost.com/column/3189960': 2590,
        'https://www.tmtpost.com/column/3882035': 2591,
    }
    
    # https://www.tmtpost.com/3970689.html
    rules = (
        Rule(LinkExtractor(allow=(r'tmtpost.com/\d{6,}.html'),
                           # restrict_xpaths=r''
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'tmtpost.com.*?\d'), deny=(
            r'/201[0-8]', r'/20190[1-9]/', r'/column/\d', r'/user/\d', r'/tag/\d', r'tmtpost.com/events'),
                           # restrict_xpaths=r''
                           ),
             process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            # //article/div[@class='post-info']/span[@class='time']
            ps = xp('//*[starts-with(@class,"time")]/text()').extract()
            pubtime = ps[0].strip()  # todo why 用浏览器明明打开了网页居然返回了403状态码
            og = xp('//head/meta[@name="author"]/@content').extract()
            if og:  # ['   ']
                og = og[0].split()
            origin_name = og[0].split()[0] if og else '钛媒体'
            content_div = xp('//article/div[@class="inner"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content_div,
                                                                 kill_xpaths=[
                                                                     r'//*[contains(text(), "点击链接、登录")]/following::*',
                                                                     r'//*[contains(text(), "点击链接、登录")]',
                                                                     r'//*[contains(text(), "更多精彩内容，关注钛媒体微信号")]/following::*',
                                                                     r'//*[contains(text(), "更多精彩内容，关注钛媒体微信号")]',
                                                                     r'//img[contains(@src, "/20171204114042938.jpg")]'
                                                                 ])
        
        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('-')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
