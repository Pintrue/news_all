# -*- coding: utf-8 -*-

import json
from datetime import datetime
from scrapy import Request
from news_all.spider_models import NewsRSpider


class XizangribaoSpider(NewsRSpider):

    name = 'xzrb_app' #西藏日报

    mystart_urls = {
        'http://vapi.xzrbapp.com/content/getcontentlist?categoryId=2&count=20&platform=android&log_debug=false&clientVersionCode=5&pjCode=xzrbc_10_201705&deviceOs=7.0&clientVersion=1.2.1&deviceModel=Xiaomi-MiNote2&udid=0f607264fc6318a92b9e13c65db7cd3c&channel=xiaomi': 1301853,
    # 西藏日报-头条
        'http://vapi.xzrbapp.com/content/getcontentlist?categoryId=11&count=20&platform=android&log_debug=false&clientVersionCode=5&pjCode=xzrbc_10_201705&deviceOs=7.0&clientVersion=1.2.1&deviceModel=Xiaomi-MiNote2&udid=0f607264fc6318a92b9e13c65db7cd3c&channel=xiaomi': 1301854,
    # 西藏日报-政务
        'http://vapi.xzrbapp.com/content/getcontentlist?categoryId=15&count=20&platform=android&log_debug=false&clientVersionCode=5&pjCode=xzrbc_10_201705&deviceOs=7.0&clientVersion=1.2.1&deviceModel=Xiaomi-MiNote2&udid=0f607264fc6318a92b9e13c65db7cd3c&channel=xiaomi': 1301855,
    # 西藏日报-旅游

    }

    def parse(self, response):
        rj = json.loads(response.text)
        result = rj.get('data')
        # result = data.get("group_data")
        # result = r.get('content')
        print(result)
        for i in result:
            detail = i.get("group_data")
            print(detail)
            for j in detail:
                url = j.get("shareUrl")

                title = j.get("listTitle")
                origin_name = j.get("source")
                pubtime = j.get("date")

                yield Request(
                    url=url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,"origin_name":origin_name,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )

    def parse_item(self, response):
        try:
            content_div = response.xpath('//div[@class="textDec"]')[0]
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

    """
        def parse(self, response):
        rj = json.loads(response.text)
        data = rj.get("data")
        for i in data:
            group_data = i.get("group_data")
            for j in group_data:
                articleId = j.get("articleId")
                title = j.get("listTitle")
                origin_name = j.get("source")
                base_url = 'http://vapi.xzrbapp.com/content/detail?clientVersion=1.0.0&pjCode=xzrbc_10_201705&device_size=1920x411&articleId='+articleId+'&categoryId=2&sysCode=article'
                yield Request(
                    url=base_url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title,'origin_name':origin_name,
                          
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )




    def parse_item(self, response):
        rj = json.loads(response.text)
        result = rj.get("result")
        code = result.get("code")
        if(code==0):
            data = rj.get("data")
            content_div = data.get("content")
            if content_div.strip() == '':
                return
            timestamp = data.get("date")
            pubtime = datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S')

            content, media, videos, video_cover = self.content_clean(content_div)
            return self.produce_item(
                response=response,
                title=response.request.meta['title'],
                pubtime=pubtime,
                origin_name=response.request.meta['origin_name'],
                
                content=content,
                media=media,
                videos=videos,
            )

    """