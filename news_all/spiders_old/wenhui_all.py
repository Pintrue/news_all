# -*- coding: utf-8 -*-

import json
from datetime import datetime
from scrapy import Request
from news_all.spider_models import NewsRSpider


# 文汇报
class WenhuiSpider(NewsRSpider):
    name = 'wenhui_all'
    
    mystart_urls = {
        
        'https://wenhui.whb.cn/whbApi/content/findContents.action?page=1&_dc=-5112965907406044313&channelId=587': 1301766,
        # 文汇报-医疗
        'https://wenhui.whb.cn/whbApi/content/findContents.action?page=1&_dc=-6016078941643780330&channelId=3091': 1301767,
        # 文汇报-城事
        'https://wenhui.whb.cn/whbApi/content/findContents.action?page=1&_dc=6923359774722444227&channelId=97': 1301764,
        # 文汇报-影视
        'https://wenhui.whb.cn/whbApi/content/findContents.action?page=1&_dc=-4404888589278558643&channelId=73': 1301762,
        # 文汇报-文汇教育
        'https://wenhui.whb.cn/whbApi/content/findContents.action?page=1&_dc=707309426246369956&channelId=1390': 1301759,
        # 文汇报-时政
        'https://wenhui.whb.cn/whbApi/content/findContents.action?page=1&_dc=2940967003524253715&channelId=1391': 1301763,
        # 文汇报-民生
        'https://wenhui.whb.cn/whbApi/content/findContents.action?page=1&_dc=-8144827624429368981&channelId=70': 1301765,
        # 文汇报-汇演
        'https://wenhui.whb.cn/whbApi/content/findContents.action?page=1&_dc=8543721203183471403&channelId=588': 1301760,
        # 文汇报-环球
        'https://wenhui.whb.cn/whbApi/content/findContents.action?page=1&_dc=-6602424863965753419&channelId=1395': 1301761,
        # 文汇报-要闻
        
    }
    
    def parse(self, response):
        rj = json.loads(response.text)
        dataList = rj.get("dataList")
        for i in dataList:
            list = i.get("list")[0]
            url = list.get("contentUrl")

            title = list.get("title")
            pubtime = list.get("publishTime")

            yield Request(
                url=url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                      
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )
    
    def parse_item(self, response):
        rj = json.loads(response.text)
        content_div = rj.get("html")
        imgs = rj.get("images")
        img_urls = []
        for i in imgs:
            img_url = i.get("imageUrl")
            img_urls.append(img_url)
        if img_urls is None:
            print("无图新闻")
        else:
            if len(img_urls):
                count = len(img_urls)
                x = list(range(0, count))
                for (i, j) in zip(img_urls, x):
                    content_div = content_div.replace("<!--IMG#" + str(j) + "-->", "<img src='" + i + "' /><br>")
        content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[
            '//*[contains(text(), "文汇独家稿件，转载请注明出处")]'])
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            # origin_name=origin_name,
            
            content=content,
            media=media,
            videos=videos,
        )
