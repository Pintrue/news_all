# -*- coding: utf-8 -*-
import json
from scrapy import Request
from news_all.spider_models import NewsRCSpider


class DdgzSpider(NewsRCSpider):
    '''当代贵州'''
    name = 'ddgz'
    mystart_urls = {
        'http://www.ddcpc.cn/index.php?siteid=8&m=phone&a=get_content_list&siteid=8&sourcesiteid=1&order=asc&catid=581&start_index=0&num=10': 1301884,
    # 当代贵州-健康
        'http://www.ddcpc.cn/index.php?siteid=8&m=phone&a=get_position&siteid=8&sourcesiteid=1&posid=38&order=desc&num=10&start_index=0': 1301875,
    # 当代贵州-头条
        'http://www.ddcpc.cn/index.php?siteid=8&m=phone&a=get_content_list&siteid=8&sourcesiteid=1&order=asc&catid=649&start_index=0&num=10': 1301883,
    # 当代贵州-娱乐
        'http://www.ddcpc.cn/index.php?siteid=8&m=phone&a=get_content_list&siteid=8&sourcesiteid=1&order=asc&catid=585&start_index=0&num=10': 1301880,
    # 当代贵州-教育
        'http://www.ddcpc.cn/index.php?siteid=8&m=phone&a=get_content_list&siteid=8&sourcesiteid=1&order=asc&catid=591&start_index=0&num=10': 1301881,
    # 当代贵州-旅游
        'http://www.ddcpc.cn/index.php?siteid=8&m=phone&a=get_content_list&siteid=8&sourcesiteid=1&order=asc&catid=592&start_index=0&num=10': 1301885,
    # 当代贵州-时尚
        'http://www.ddcpc.cn/index.php?siteid=8&m=phone&a=get_content_list&siteid=8&sourcesiteid=1&&order=asc&catid=619&start_index=0&num=10': 1301882,
    # 当代贵州-社会
        'http://www.ddcpc.cn/index.php?siteid=8&m=phone&a=get_content_list&siteid=8&sourcesiteid=1&&order=asc&catid=617&start_index=0&num=10': 1301877,
    # 当代贵州-经济
    }

    def parse(self, response):
        rj = json.loads(response.text)
        data = rj.get('data')
        for item in data:
            url = item.get("url")
            title = item.get("title")
            origin_name = item.get("copyfrom")
            pubtime = item.get("inputtime")
            yield Request(
                url=url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,"origin_name":origin_name,
                      
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )

    def parse_item(self, response):
        xp = response.xpath
        try:
            content_div = xp("//div[@class='content']")[0]  # \
                          # or xp('//div[@class="cnt_bd"]')[0] \
                          # or xp('//div[@class="main-text-container"]/section')[0]
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            content=content,
            media=media,
            videos=videos,
        )
