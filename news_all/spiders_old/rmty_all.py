# -*- coding: utf-8 -*-

import json
from datetime import datetime
from scrapy import Request
from news_all.spider_models import NewsRSpider


class RmtySpider(NewsRSpider):

    name = 'rmty' #人民体育客户端

    mystart_urls = {
        'http://newsapi.people.cn/sports/content/getcontentlist?categoryid=36&categorytype=normal&systype=cms&timestamp=0&maxid=&sinceid=&adcode=&isoCC=cn&city=%E5%8C%97%E4%BA%AC&device_product=Xiaomi&province=%E5%8C%97%E4%BA%AC&userid=1005030&network_state=wifi&MNC=07&client_ver=1.0.2&client_code=3&udid=869718026725165&MCC=460&visit_id=1531883457599&device_os=7.0&longitude=&sp=&visit_start_time=1531883457599&ctime=1531883457592&sessionId=2051ed02df0c4d8db45b5a4787570c78tTaGiCnq&platform=android&app_key=10_2016_12_89&device_size=1080.0x1920.0&district=&securitykey=5f959b725f44ac12f7519c2cf0fc7d95&device_model=Xiaomi-MI5s&latitude=&channel_num=xiaomi&citycode=': 1301120,
        # 人民体育客户端
    }

    def parse(self, response):
        rj = json.loads(response.text)
        result = rj.get('data', [])
        if not result:
            return self.produce_debugitem(response, 'json error')
        for i in result:
            link = i.get('group_data')
            for j in link:
                url = j.get("share_url")
                title = j.get("title")
                origin_name = ""
                pubtime = j.get("news_datetime")

                yield Request(
                    url=url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,'origin_name':origin_name,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )

    def parse_item(self, response):
        try:
            origin_name = response.xpath("//p[@class='info']/span[@class='source']/text()").extract_first()
            content_div = response.xpath('.//div[@class="news-d-main"]/div[@class="TRS_Editor"]')[0]
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

    def parse_item_2(self, response):
        # http://dsimg.people.cn/data/rmtyimg/2019/06/12/cms_3253096666235904.html
        try:
            origin_name = response.xpath("//span[@class='source']/text()").extract_first()
            content_div = response.xpath('//div[@class="article"]')[0]
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

    def parse_item_3(self, response):
        # http://dsimg.people.cn/data/rmtyimg/2019/06/10/cms_3250203358184448.html
        try:
            origin_name = response.xpath("//span[@class='source']/text()").extract_first()
            content_div = response.xpath('//div[@class="img_slide_block"]')[0]
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