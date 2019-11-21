#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 10:42
# @Author  : wjq
# @File    : hubpd.py


import re
from lxml import etree
from news_all.spider_models import NewsRSpider


video_pat = re.compile(r'<embed(?: style="display:none;")?( type="application/x-shockwave-flash".*?>)')


class HubpdXmlSpider(NewsRSpider):
    """中央厨房_xml"""
    name = 'hubpd_xml'

    mystart_urls = {
        'http://rev.uar.hubpd.com/recom/rss?appkey=UAR-000457_279': 1000151,
    }

    def parse(self, response):
        html = etree.fromstring(bytes(bytearray(response.text, encoding='utf-8')))
        channel_node = html.find('channel')
        if not channel_node:
            return self.produce_debugitem(response, "xpath error")

        for i in channel_node.findall('item'):
            origin_div = i.find('source')
            url = origin_div.attrib.get('url') or i.find('link').text

            pubtime = i.find('pubDate').text.replace('+0800', '').strip()

            title = i.find('title').text

            origin_name = origin_div.text
            content_div = i.find('description').text
            if 'video' in content_div:
                print()
            content_div = video_pat.sub(r'<video\1</video>', content_div)
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True,
                                                                     kill_xpaths='//*[contains(text(),"To view this video please enable JavaScript")]')

            yield self.produce_item(response=response,
                                    title=title,
                                    pubtime=pubtime,
                                    origin_name=origin_name,
                                    content=content,
                                    media=media,
                                    videos=videos,
                                    cover=video_cover,
                                    srcLink=url
                                    )