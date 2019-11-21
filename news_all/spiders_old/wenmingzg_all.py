# -*- coding: utf-8 -*-

import json
from datetime import datetime
from scrapy import Request
from news_all.spider_models import NewsRSpider


class Wenmingzhongguo_allSpider(NewsRSpider):

    name = 'wmzg' #文明中国

    mystart_urls = {
        'http://wmwapi.people.cn/gov/home?refresh_type=0&device_size=1080.75x1922.25': 1301770,  # 文明中国-城市
        'http://wmwapi.people.cn/content/getcontentlist?categoryid=2&categorytype=0&systype=&timestamp=null&maxid=2805711381447680_cms_2805711381447680&sinceid=': 1301769,
    # 文明中国-活动
        'http://wmwapi.people.cn/content/getcontentlist?categoryid=7&categorytype=0&systype=&timestamp=3cf0ad0f66a2f5ef4125c5f8bf0c8194dda207dbaaa10c2b9762e9ec1dff9a75&maxid=&sinceid=': 1301768,
    # 文明中国-资讯

    }

    def parse(self, response):
        rj = json.loads(response.text)
        data = rj.get('data')
        try:
            result = data.get("articles", [])
            print(result)
            for i in result:
                    detail = i.get("articles")
                    print(detail)
                    for j in detail:
                        url = j.get("wap_url")

                        title = j.get("title")
                        origin_name = ""
                        pubtime = j.get("timestamp")

                        yield Request(
                            url=url,
                            callback=self.parse_item,
                            meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                                  "origin_name": origin_name,
                                  'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                        )
        except:
            for l in data:
                new = l.get("group_data")
                print(new)
                for k in new:
                    url = k.get("share_url")
                    title = k.get("title")
                    origin_name = ""
                    pubtime = k.get("news_datetime")

                    yield Request(
                        url=url,
                        callback=self.parse_item,
                        meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                              "origin_name": origin_name,
                              'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                    )

    def parse_item(self, response):
        try:
            content_div = response.xpath('//div[@class="detail tj"]')[0]
            origin_name = response.xpath("//span[@class='source']/text()").extract_first()
        except:
            return self.parse_item_2(response)

        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            content=content,
            media=media,
            videos=videos,
        )

    #http://www.wenming.cn/wmpl_pd/kyky/201906/t20190611_5146420.shtml
    def parse_item_2(self, response):
        try:
            content_div = response.xpath('//div[@class="Custom_UnionStyle"]')[0]
            origin_name = response.xpath("//div[@class='kyky-cp']/text()").extract_first()
        except:
            return self.parse_item_3(response)

        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            
            content=content,
            media=media,
            videos=videos,
        )


    #http://www.wenming.cn/bwzx/jj/201906/t20190624_5159834.shtml
    def parse_item_3(self, response):
        try:
            content_div = response.xpath('//div[@class="Custom_UnionStyle"]')[0]
            origin_name = response.xpath("//div[@id='time_tex']/text()").extract_first()
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            
            content=content,
            media=media,
            videos=videos,
        )
