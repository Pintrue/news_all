# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Changjiangwang_allSpider(NewsRCSpider):
    """长江网"""
    name = "cjw"
    mystart_urls = {
        'http://news.cjn.cn/gnxw/': 1301561,  # 长江网-天下博览-左侧列表
        'http://news.cjn.cn/sywh/': 1301560,  # 长江网-武汉-左侧列表
        'http://news.cjn.cn/shxw/': 1301559,  # 长江网-社会-左侧列表

    }
    rules = (
        #http://news.cjn.cn/gnxw/201906/t3418076.htm?spm=zm1066-001.0.0.1.BrE3ua
        # http://news.cjn.cn/sywh/201907/t3429617.htm?spm=zm1066-001.0.0.1.dlMspP
        #http://news.cjn.cn/gnxw/201906/t3418047.htm
        #http://news.cjn.cn/shxw/201904/t3386973.htm
        #http://news.cjn.cn/sywh/201906/t3418130.htm
        Rule(LinkExtractor(allow=(r'news.cjn.cn.*?/%s/t\d+.htm' % datetime.today().strftime('%Y%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='art-title']/text()").extract_first() or self.get_page_title(response).split('_')[0]
            cvs = xp("//div[@class='TRS_Editor']") or xp("//article/div[@class='art-main']")
            content_div = cvs[0]
            pubtime = xp("//span[@class='pub-time']").re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{2}:\d{2}')[0]
            
            
            origin_name = xp("//span[@class='sour']/text()").extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

        # 过滤视频
        # if self.video_filter(content_div) or self.page_turn_filter(content_div):
        #     return

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )
