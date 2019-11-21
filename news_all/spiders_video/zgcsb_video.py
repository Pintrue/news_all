# -*- coding:utf-8 -*-

import os
import base64
import re
from scrapy import Request
from news_all.spider_models import NewsRCSpider, otherurl_meta
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from datetime import datetime


VIDEO_API = "http://tvplayer.people.com.cn/getXML.php?path={}"
VIDEO_API_vblogPlayerV4 = "http://vblog.people.com.cn/getWapXML.php?pid={}"


class ZgcsbSpider(NewsRCSpider):
    """中国城市报 视频"""
    name = "zgcsb_video"
    mystart_urls = {"http://www.zgcsb.com/video/": 3881}

    # http://www.zgcsb.com/video/news/2019-08-19/117202.html
    # http://www.zgcsb.com/video/news/2018-11-14/79313.html
    # http://www.zgcsb.com/video/news/2019-01-23/85489.html 腾讯视频
    rules = (
        Rule(LinkExtractor(allow=(r'www.zgcsb.com/video/news/%s-\d{2}/\d+.htm') % datetime.today().strftime('%Y-%m'),),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'www.zgcsb.com.*?\d+.htm'), ),
             process_request=otherurl_meta, follow=False),
    )

    custom_settings = {
        'DEPTH_LIMIT': 2,  # 设置深度
    }
    # LimitatedDaysHoursMinutes = (10, 0, 0)

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//*[@id="artical_topic"]/text()').extract_first('')
            pubtime = xp('//*[@itemprop="datePublished"]/text()').extract_first('')
            origin_name = xp('//*[@class="ss03"]/text()').extract_first('')
            content_div = xp("//div[@id='artical_real']/div[@id='main_content']").extract()[0]
            content, media, _, _ = self.content_clean(content_div, kill_xpaths="//embed")

            swf_url = xp('//embed/@src').extract()[0]
            video_path = os.path.basename(os.path.dirname(swf_url))
            if os.path.basename(swf_url) == 'playerByOsmf.swf':
                # 'L3B2c2VydmljZS94bWwvLzIwMTkvOC8yMS85YzdjOTAyZi05ZWFhLTQyOTUtYTJjOC04Y2UwNjA3MGI1ZjcueG1s'
                # decodestr = '/pvservice/xml//2019/8/21/9c7c902f-9eaa-4295-a2c8-8ce06070b5f7.xml'
                decodestr = base64.b64decode(video_path).decode("utf-8")
                video_url = VIDEO_API.format(decodestr)
                # http://tvplayer.people.com.cn/getXML.php?path=/pvservice/xml//2019/8/21/9c7c902f-9eaa-4295-a2c8-8ce06070b5f7.xml

            elif os.path.basename(swf_url) == 'vblogPlayerV4.swf':
                # swf_url = "http://tvplayer.people.com.cn/vPlayer.php/pid/20190816_8786_sylz_esep/vblogPlayerV4.swf"
                # http://vblog.people.com.cn/getWapXML.php?pid=20190816_8786_sylz_esep&callback=playForMobile
                video_url = VIDEO_API_vblogPlayerV4.format(re.search('pid/(\w+)/', swf_url).group(1))
            else:
                return self.produce_debugitem(response, 'video parse error')
        except:
            return self.produce_debugitem(response, 'xpath error')
        return Request(video_url,
                       callback=self.parse_video,
                       meta={'source_id': response.meta['source_id'],
                             'title': title,
                             'pubtime': pubtime,
                             'origin_name': origin_name,
                             'content': content,
                             'media': media,
                             'news_url': response.url,
                             'start_url_time': response.meta.get('start_url_time'),
                             'schedule_time': response.meta.get('schedule_time')}
                       )

    def parse_video(self, response):
        video_url, *_ = eval(response.text)

        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            content='<div>#{{1}}#</div>' + response.request.meta['content'],
            media=response.request.meta['media'],
            videos={'1': {'src': video_url}},
            srcLink=response.meta.get('news_url')
        )

