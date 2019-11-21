# -*- coding: utf-8 -*-
# @Time   : 2019/11/7 下午4:25
# @Author : mez
# @Project : news_all
# @FileName: bjd_spider.py
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from news_all.tools.time_translater import Pubtime


class Bjd(NewsRCSpider):
    name = 'bjd'

    # 北京日报 ==》 补充全站采集
    mystart_urls = {
        "http://www.bjd.com.cn/": 1
    }

    rules = (

        # http://www.bjd.com.cn/a/201911/08/WS5dc4c152e4b0621d5c14cfb2.html
        Rule(LinkExtractor(allow=r'.bjd.com.cn/\w+/%s/\d{2}/\w+\.html' % datetime.today().strftime('%Y%m'),),
             callback='parse_item',
             follow=True),

        Rule(LinkExtractor(allow=r'bjd.com.cn/.*?\.html', deny=(r'/201[0-8]', r'/20190[1-9]', r'/20191[0]'),),
             process_request=otherurl_meta,
             follow=False),
    )


    def parse_item(self, response):
        # http://www.bjd.com.cn/a/201911/08/WS5dc4c152e4b0621d5c14cfb2.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//span[@class='span1']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//span[@class='span31']/text()").extract_first())
            content_div = xp("//div[@class='contentnews21']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True)  # str  list
            origin_name = xp("//span[@class='span32']/text()").extract_first()# None  不要用[0]
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,

        )