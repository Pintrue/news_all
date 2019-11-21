# -*- coding: utf-8 -*-
# @Time   : 2019/10/22 下午4:25
# @Author : mez
# @Project : news_all
# @FileName: hsw_spider.py
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from news_all.tools.time_translater import Pubtime


class Hsw(NewsRCSpider):
    name = 'hsw'

    # 华商网==》 补充全站采集
    mystart_urls = {
        "http://www.hsw.cn/": 1,
    }

    rules = (
        # http://news.hsw.cn/system/2019/1105/1127171.shtml
        Rule(LinkExtractor(allow=r'.hsw.cn/system/%s\d{2}/\d+\.s?html' % datetime.today().strftime('%Y/%m'),),
             callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=r'.hsw.cn/.*?\.s?html', deny=(r'/201[0-8]', r'/2019/0[1-9]', r'/2019/1[0]', r'-\d',
                                                               r'bbs', r'biz'),),
             process_request=otherurl_meta,
             follow=False),
    )


    def parse_item(self, response):
        # http://news.hsw.cn/system/2019/1105/1127130.shtml
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='hd']/h1/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//span[@class='article-time']/text()").extract_first())
            try:
                content_div = xp("//div[@id='artibody']")[0]
            except:
                content_div = xp("//div[@class='bd']/div[@class='contentBox cf']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)  # str  list
            origin_name = xp("//span[@class='ly-name']/text()").extract_first()# None  不要用[0]
        except Exception as e:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_2(self, response):
        # http://news.hsw.cn/system/2019/1105/1127149.shtml
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='hd']/h1/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//span[@id='pubtime_baidu']/text()").extract_first())
            content_div = xp("//div[@class='photoarea']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)  # str  list
            origin_name = xp("//span[@id='source_baidu']/text()").extract_first()# None  不要用[0]
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



