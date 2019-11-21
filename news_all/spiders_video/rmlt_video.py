# -*- coding: utf-8 -*-
# @Time   : 2019/8/26 下午5:34
# @Author : NewmanZhou
# @Project : news_all
# @FileName: rmlt_video.py

from news_all.spider_models import NewsRSpider
from scrapy import Request
import re, json


class RMLTVideoSpider(NewsRSpider):
    """人民论坛 视频"""
    name = 'rmlt_video'

    mystart_urls = {
        'http://video.rmlt.com.cn/dajiangtang/': 3875,  # 大讲堂
        'http://video.rmlt.com.cn/shipinxinwen/': 3876,  # 新闻
        'http://video.rmlt.com.cn/jilupian/': 3877,  # 纪录片
        'http://video.rmlt.com.cn/podcast/': 3878,  # 播客
    }

    custom_settings = {
        'DEPTH_LIMIT': 2,  # 翻页需要设置深度为0 或者 >1
    }

    def parse(self, response):
        try:
            xp = response.xpath
            listItems = xp('//div[@class="list"]/ul/li')
            for item in listItems:
                url = item.xpath('a/@href').extract_first('')
                if url:
                    yield Request(
                        url=url,
                        callback=self.parse_item,
                        meta={'source_id': response.meta['source_id'],
                              'start_url_time': response.meta.get('start_url_time'),
                              'schedule_time': response.meta.get('schedule_time')
                              }
                    )
        except:
            return self.produce_debugitem(response, "xpath error")

    def parse_item(self, response):
        xp = response.xpath
        try:
            src = xp('//script[@class="cmstopVideo"]/@src').extract_first()
            if src:
                title = xp('//h2[@class="videoshow-title"]/text()').extract_first()
                pubtime = xp('//span[@class="date f-l"]/text()').extract_first()
                origin_name = xp('//span[@class="editors f-l"]/text()').extract_first()
                yield Request(
                    url=src,
                    callback=self.parse_item_one,
                    meta={'source_id': response.meta['source_id'],
                          'start_url_time': response.meta.get('start_url_time'),
                          'schedule_time': response.meta.get('schedule_time'),
                          'title': title,
                          'pubtime': pubtime,
                          'origin_name': origin_name,
                          'news_url': response.url
                          }
                )
            else:
                baseUrl = 'http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid='
                src = xp('//embed[@id="v_player_cctv"]/@flashvars').extract()[0]
                videoCenterId = re.findall('videoCenterId=(\w+)', src)[0]
                reqUrl = baseUrl + videoCenterId
                title = xp('//h1[@class="article-title"]/text()').extract_first()
                pubtime = xp('//span[@class="date"]/text()').extract_first()
                origin_name = xp('//span[@class="source"]/text()').extract_first()
                cv = xp('//div[@class="article-content fontSizeSmall BSHARE_POP"]').extract_first()
                content, media, _, _ = self.content_clean(cv, need_video=False,
                                                          kill_xpaths='//span[@class="ifengLogo"]')
                yield Request(
                    url=reqUrl,
                    callback=self.parse_item_two,
                    meta={'source_id': response.meta['source_id'],
                          'start_url_time': response.meta.get('start_url_time'),
                          'schedule_time': response.meta.get('schedule_time'),
                          'title': title,
                          'pubtime': pubtime,
                          'origin_name': origin_name,
                          'content': content,
                          'media': media,
                          'news_url': response.url
                          }
                )
        except:
            return self.produce_debugitem(response, "xpath error")
            # 加密地址处理
            # return self.parse_item_two(response)

    def parse_item_one(self, response):
        try:
            xp = response.xpath
            video_url = xp('//video/source/@src').extract_first()
            title = response.meta.get('title')
            pubtime = response.meta.get('pubtime')
            origin_name = response.meta.get('origin_name')

            return self.produce_item(
                response=response,  # must
                title=title,
                pubtime=pubtime,
                origin_name=origin_name,
                content='<p>#{{1}}#</p>',
                videos={'1': {'src': video_url}},
                srcLink=response.meta.get('news_url')
            )
        except:
            return self.produce_debugitem(response, "xpath error")

    def parse_item_two(self, response):
        try:
            data = json.loads(response.text)
            video_url = data['video']['lowChapters'][0]['url']
            title = response.meta.get('title')
            pubtime = response.meta.get('pubtime')
            origin_name = response.meta.get('origin_name')
            content = response.meta.get('content')
            media = response.meta.get('media')
            return self.produce_item(
                response=response,  # must
                title=title,
                pubtime=pubtime,
                origin_name=origin_name,
                media=media,
                content='<div>#{{1}}#</div>' + content,
                videos={'1': {'src': video_url}},
                srcLink=response.meta.get('news_url')
            )
        except:
            return self.produce_debugitem(response, "xpath error")
