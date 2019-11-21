#!/usr/bin/env python
# -*- coding:utf-8 _*-
# Time: 2019/08/15
# Author: zcy

from scrapy import Request
from urllib.parse import urljoin
from news_all.spider_models import NewsRSpider


class CnautonewsSpider(NewsRSpider):
    """中国汽车报 视频"""
    name = 'cnautonews_videos'
    
    mystart_urls = {
        'http://www.cnautonews.com/xsp/2019sptj/': 3759,  # 最新推荐
        'http://www.cnautonews.com/xsp/jthc/': 3760,  # 金台话车
        'http://www.cnautonews.com/xsp/2019spgcdys/': 3761,  # 购车嘚云社
        'http://www.cnautonews.com/xsp/2019spgcdys32/': 3762,  # 车闻巴士
        'http://www.cnautonews.com/xsp/2019splj90j/': 3763,  # 金台路2号评车
        'http://www.cnautonews.com/xsp/cwmdm/': 3764,  # 车闻面对面
        'http://www.cnautonews.com/xsp/gdsp1/': 3765,  # 更多
    }
    
    def parse(self, response):
        xp = response.xpath
        video_list = xp('//div[@class="cCon-video"]/a/@href').extract()
        for video in video_list:
            if video.endswith('m3u8'):
                continue
            elif video.startswith('.'):
                video = urljoin(response.url, video)
            yield Request(
                url=video,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'],
                      'start_url_time': response.meta.get('start_url_time'),
                      'schedule_time': response.meta.get('schedule_time')
                      }
            )
    
    def parse_item(self, response):
        try:
            title = response.xpath('//div[@class="news-d-title"]/text()').extract_first() or self.get_page_title(
                response).replace('-中国汽车报', '')
            item_info = response.xpath('//div[@class="news-d-other"]')
            pubtime = item_info.xpath('//div[@class="news-d-other"]/span[2]/text()').extract_first().strip()
            video_url = response.xpath('//div[@class="news-d-main"]/video/@src').extract_first()  # 只有视频没有文字
        except:
            self.produce_debugitem(response, 'xpath error')
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name='中国汽车报',
            content='<div>#{{1}}#</div>',
            videos={'1': {'src': video_url}}
        )
