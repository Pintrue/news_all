# -*- coding: utf-8 -*-

import json
from datetime import datetime
from scrapy import Request
from news_all.spider_models import NewsRCSpider


class YzinterSpider(NewsRCSpider):
    """新福建"""
    name = 'fjdaily_all'

    mystart_urls = {
        'http://api.fjdaily.com/content/getcontentlist?categoryid=8&categorytype=normal&systype=cms&timestamp=0&maxid=&sinceid=&device_product=HUAWEI&MNC=&device_size=1440.0x2560.0&device_model=HUAWEI-ALP-AL00&city=%E5%8C%97%E4%BA%AC%E5%B8%82&latitude=39.919258&userid=3249292&visit_start_time=1533104022786&platform=android&client_ver=2.0.12&province=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&channel_num=baidu&isoCC=&ctime=1533104022782&udid=867779038264868&sp=&longitude=116.471552&adcode=110105&sessionId=55023df5f1d64ceb9eb067b18690e566ao0WCtWx&MCC=&device_os=8.0.0&app_key=2_2016_04_21&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&network_state=wifi&visit_id=1533104022786&securitykey=ad24c4b71f401896f55616b9418df7e6&client_code=269': 1302137,
    # 新福建 台海
        'http://api.fjdaily.com/content/getcontentlist?categoryid=56&categorytype=normal&systype=cms&timestamp=48fe402ca9374b91d13158fe7c475748675b7eeb34939560e8295487b619eecf&maxid=&sinceid=&device_product=HUAWEI&MNC=&device_size=1440.0x2560.0&device_model=HUAWEI-ALP-AL00&city=%E5%8C%97%E4%BA%AC%E5%B8%82&latitude=39.919258&userid=3249292&visit_start_time=1533104482396&platform=android&client_ver=2.0.12&province=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&channel_num=baidu&isoCC=&ctime=1533104482374&udid=867779038264868&sp=&longitude=116.471552&adcode=110105&sessionId=55023df5f1d64ceb9eb067b18690e566ao0WCtWx&MCC=&device_os=8.0.0&app_key=2_2016_04_21&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&network_state=wifi&visit_id=1533104482396&securitykey=1077d5a3c9454e68d37791cc31f2594f&client_code=269': 1302136,
    # 新福建-听政
        'http://api.fjdaily.com/content/getcontentlist?categoryid=59&categorytype=normal&systype=cms&timestamp=1fdfa383c0e10788e1168ccab027c7f0c8e943cac8231f321e9fb29f0a6f216a&maxid=&sinceid=&device_product=HUAWEI&MNC=&device_size=1440.0x2560.0&device_model=HUAWEI-ALP-AL00&city=%E5%8C%97%E4%BA%AC%E5%B8%82&latitude=39.919258&userid=3249292&visit_start_time=1533104326805&platform=android&client_ver=2.0.12&province=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&channel_num=baidu&isoCC=&ctime=1533104326800&udid=867779038264868&sp=&longitude=116.471552&adcode=110105&sessionId=55023df5f1d64ceb9eb067b18690e566ao0WCtWx&MCC=&device_os=8.0.0&app_key=2_2016_04_21&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&network_state=wifi&visit_id=1533104326805&securitykey=2cd3a089fa7e79e871a93412f0cd6a46&client_code=269': 1302138,
    # 新福建-天下
        'http://api.fjdaily.com/content/getcontentlist?categoryid=3&categorytype=normal&systype=cms&timestamp=0&maxid=&sinceid=&device_product=HUAWEI&MNC=&device_size=1440.0x2560.0&device_model=HUAWEI-ALP-AL00&city=%E5%8C%97%E4%BA%AC%E5%B8%82&latitude=39.919258&userid=3249292&visit_start_time=1533104479847&platform=android&client_ver=2.0.12&province=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&channel_num=baidu&isoCC=&ctime=1533104479844&udid=867779038264868&sp=&longitude=116.471552&adcode=110105&sessionId=55023df5f1d64ceb9eb067b18690e566ao0WCtWx&MCC=&device_os=8.0.0&app_key=2_2016_04_21&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&network_state=wifi&visit_id=1533104479847&securitykey=199a5934dfef743f2abdf75faef09708&client_code=269': 1302135,
    # 新福建-头条

    }

    def parse(self, response):
        rj = json.loads(response.text)
        data = rj.get("data")
        for i in data:
            group_data = i.get("group_data")
            for j in group_data:
                title = j.get("title")
                origin_name = j.get("copyfrom")
                share_url = j.get("share_url")
                pubtime = j.get("news_datetime")
                
                yield Request(
                    url=share_url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title,'origin_name':origin_name,'pubtime':pubtime,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )


    def parse_item(self, response):
        try:
            content_div = response.xpath('//div[@class="article_body"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths='//p[@id="htmlLove"]')
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            
            content=content,
            media=media,
            videos=videos,
        )

