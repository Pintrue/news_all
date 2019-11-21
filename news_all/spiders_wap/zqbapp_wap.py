# -*- coding: utf-8 -*-

import json
import re
from scrapy import Request
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings
import jsonpath


img_pattern = re.compile(r'''<img.*?data-original=['"](.*?)['"].*?>''')


class ZqbappSpider(NewsRSpider):
    """中国青年报 app"""
    name = 'zqbapp_app'
    
    mystart_urls = {
        'https://zqbapp.cyol.com/zqzxapi/api.php?s=/News/getNewsListCache': [3720, 3722, 3723, 3724, 3725, 3726, 3727,
                                                                             3728, 3729, 3730, 3731, 3732, 3733, 3734,
                                                                             3735, 3736, 3737, 3738, 3739, 3740, 3741,
                                                                             3742, 3743, 3744, 3745, 3746, 3747, 3754,
                                                                             3755, 3756, 3721, ],
        'https://zqbapp.cyol.com/zqzxapi/api.php?s=/Think/getColumnNews': [3748, 3749, 3750, 3751, 3752, 3753, ]
    }
    
    custom_settings = {
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')
    }
    start_formdata_map = {
        3720: ("APP端-中央媒体移动端-中国青年报网-新闻-推荐", {'tid': '-1'}),
        3722: ("APP端-中央媒体移动端-中国青年报网-新闻-学习", {'tid': '767'}),
        3723: ("APP端-中央媒体移动端-中国青年报网-新闻-时政", {'tid': '548'}),
        3724: ("APP端-中央媒体移动端-中国青年报网-新闻-冰点", {'tid': '771'}),
        3725: ("APP端-中央媒体移动端-中国青年报网-新闻-评论", {'tid': '777'}),
        3726: ("APP端-中央媒体移动端-中国青年报网-新闻-微信精选", {'tid': '885'}),
        3727: ("APP端-中央媒体移动端-中国青年报网-新闻-青年眼", {'tid': '895'}),
        3728: ("APP端-中央媒体移动端-中国青年报网-新闻-传承的力量", {'tid': '886'}),
        3729: ("APP端-中央媒体移动端-中国青年报网-新闻-教育", {'tid': '785'}),
        3730: ("APP端-中央媒体移动端-中国青年报网-新闻-校园", {'tid': '797'}),
        3731: ("APP端-中央媒体移动端-中国青年报网-新闻-视频", {'tid': '551'}),
        3732: ("APP端-中央媒体移动端-中国青年报网-新闻-国际", {'tid': '803'}),
        3733: ("APP端-中央媒体移动端-中国青年报网-新闻-财经", {'tid': '804'}),
        3734: ("APP端-中央媒体移动端-中国青年报网-新闻-法治", {'tid': '811'}),
        3735: ("APP端-中央媒体移动端-中国青年报网-新闻-社会", {'tid': '812'}),
        3736: ("APP端-中央媒体移动端-中国青年报网-新闻-体育", {'tid': '814'}),
        3737: ("APP端-中央媒体移动端-中国青年报网-新闻-文化", {'tid': '818'}),
        3738: ("APP端-中央媒体移动端-中国青年报网-新闻-军事", {'tid': '826'}),
        3739: ("APP端-中央媒体移动端-中国青年报网-新闻-科技", {'tid': '834'}),
        3740: ("APP端-中央媒体移动端-中国青年报网-新闻-汽车", {'tid': '837'}),
        3741: ("APP端-中央媒体移动端-中国青年报网-新闻-创业", {'tid': '842'}),
        3742: ("APP端-中央媒体移动端-中国青年报网-新闻-生活", {'tid': '550'}),
        3743: ("APP端-中央媒体移动端-中国青年报网-新闻-视觉", {'tid': '848'}),
        3744: ("APP端-中央媒体移动端-中国青年报网-新闻-中青号", {'tid': '849'}),
        3745: ("APP端-中央媒体移动端-中国青年报网-新闻-榜样阅读", {'tid': '668'}),
        3746: ("APP端-中央媒体移动端-中国青年报网-新闻-活动", {'tid': '875'}),
        3747: ("APP端-中央媒体移动端-中国青年报网-新闻-两会", {'tid': '875'}),
        
        3748: ("APP端-中央媒体移动端-中国青年报网-思想者-青·学习", {'tid': '645'}),
        3749: ("APP端-中央媒体移动端-中国青年报网-思想者-青·理论", {'tid': '603'}),
        3750: ("APP端-中央媒体移动端-中国青年报网-思想者-青·声音", {'tid': '605'}),
        3751: ("APP端-中央媒体移动端-中国青年报网-思想者-青·体验", {'tid': '606'}),
        3752: ("APP端-中央媒体移动端-中国青年报网-思想者-青·视野", {'tid': '607'}),
        3753: ("APP端-中央媒体移动端-中国青年报网-思想者-青·研究", {'tid': '604'}),
        
        3754: ("APP端-中央媒体移动端-中国青年报网-共青团-联播", {'tid': '688'}),
        3755: ("APP端-中央媒体移动端-中国青年报网-共青团-各地", {'tid': '689'}),
        3756: ("APP端-中央媒体移动端-中国青年报网-共青团-青学习", {'tid': '716'}),
        3721: ("APP端-中央媒体移动端-中国青年报网-共青团-订阅", {'tid': '0'}),
    }
    
    start_method = 'POST'
    
    def parse(self, response):
        rj = json.loads(response.text)
        code = rj.get("code")
        if code == "200":
            # "https://zqbapp.cyol.com/zqzxapi/api.php?s=/News/getNewsListCache"
            # 新闻列表为该url的   json中新闻数据位于data字典下面
            data = rj.get("data")
            # https://zqbapp.cyol.com/zqzxapi/api.php?s=/Think/getColumnNews     新闻列表为该url的   json中的新闻数据位于data下面的columnnews 下面
            # https://zqbapp.cyol.com/zqzxapi//api.php?s=/Subject/getSubjectNewsh5/flag/2/nid/281050
            columnnews = jsonpath.jsonpath(rj, '$..columnnews')

            if columnnews:
                data = columnnews

            for i in data:
                title = i.get("title")
                news_url = i.get("newsurl")
                pubtime = i.get("update_time")

                # https://zqbapp.cyol.com/zqzxapi//cyolbnbt/share/jiankong.php?v_id=12538
                # 排除m3u8视频
                if 'share/jiankong.php' in news_url:
                    continue
                if 'Video/video' in news_url:
                    video_url = self.parse_videourl(i)
                    if not video_url:
                        continue

                if '/api.php?s=' in news_url:
                    yield Request(
                        url=news_url,
                        callback=self.parse,
                        meta={'source_id': response.meta['source_id'],
                              'start_url_time': response.meta.get('start_url_time'),
                              'schedule_time': response.meta.get('schedule_time')}
                    )
                    continue

                yield Request(
                    url=news_url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )

    def parse_videourl(self, articlejson):
        video_url = articlejson.get('video', {}).get('src')
        if video_url[-5:] != ".m3u8":
            return video_url

    def parse_item(self, response):
        try:
            content_div = response.xpath('//div[@class="section-main"]')[0]
            origin_name = response.xpath('//span[@id="copyfrom"]/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div, img_re=img_pattern, need_video=True)
            # 排除m3u8视频
            if videos and videos['1']['src'][-5:] == ".m3u8":
                return
        except BaseException:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(response=response,
                                 title=response.meta.get('title'),
                                 pubtime=response.meta.get('pubtime'),
                                 origin_name=origin_name,
                                 content=content,
                                 media=media,
                                 videos=videos
                                 )
