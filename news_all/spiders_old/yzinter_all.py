# -*- coding: utf-8 -*-

import json
from datetime import datetime
from scrapy import Request
from news_all.spider_models import NewsRCSpider


class YzinterSpider(NewsRCSpider):
    # 扬子扬眼
    name = 'yzinter_all'

    mystart_urls = {
        'http://t.yzinter.com/index.php?m=Toutiao&a=newslist&classid=141&page=0': 1301830,  # 扬子扬眼-中国
        'http://t.yzinter.com/index.php?m=Toutiao&a=newslist&classid=45&page=0': 1301840,  # 扬子扬眼-名医团
        'http://t.yzinter.com/index.php?m=Toutiao&a=newslist&classid=36&page=0': 1301839,  # 扬子扬眼-娱无双
        'http://t.yzinter.com/index.php?m=Toutiao&a=newslist&classid=47&page=0': 1301833,  # 扬子扬眼-房产
        'http://t.yzinter.com/index.php?m=Toutiao&a=newslist&classid=122&page=0': 1301828,  # 扬子扬眼-推荐
        'http://t.yzinter.com/index.php?m=Toutiao&a=newslist&classid=235&page=0': 1301841,  # 扬子扬眼-江苏
        'http://t.yzinter.com/index.php?m=Toutiao&a=newslist&classid=44&page=0': 1301836,  # 扬子扬眼-汽车
        'http://t.yzinter.com/index.php?m=Toutiao&a=newslist&classid=35&page=0': 1301831,  # 扬子扬眼-环球
        'http://t.yzinter.com/index.php?m=Toutiao&a=newslist&classid=125&page=0': 1301838,  # 扬子扬眼-社会
        'http://t.yzinter.com/index.php?m=Toutiao&a=newslist&classid=49&page=0': 1301835,  # 扬子扬眼-科技
        'http://t.yzinter.com/index.php?m=Toutiao&a=newslist&classid=41&page=0': 1301829,  # 扬子扬眼-紫牛新闻
        'http://t.yzinter.com/index.php?m=Toutiao&a=newslist&classid=38&page=0': 1301832,  # 扬子扬眼-要闻
        'http://t.yzinter.com/index.php?m=Toutiao&a=newslist&classid=39&page=0': 1301834,  # 扬子扬眼-财汇
    }

    def parse(self, response):
        rj = json.loads(response.text)
        for i in rj:
            url = i.get("titleurl")
            title = i.get("title")
            yield Request(
                url=url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title,
                      
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )

    def parse_item(self, response):
        try:
            content_div = response.xpath('//div[@id="content"]')[0]
            source_div = response.xpath('//div[@class="text-time"]')[0]
            pubtime = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}')[0]
            
            
        except:
            return self.produce_debugitem(response, "xpath error")
        origin_name = "".join(source_div.re(r'[\u4e00-\u9fa5]+'))
        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media,
            videos=videos,
        )

