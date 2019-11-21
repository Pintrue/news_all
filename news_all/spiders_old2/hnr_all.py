# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider


class HnrAllSpider(NewsRCSpider):
    """映象网"""
    name = 'hnr_all'

    mystart_urls = {
        'http://finance.hnr.cn/lcjz/': 1301542,  # 映象网-产业资讯-左侧列表
        'http://finance.hnr.cn/bx/': 1301541,  # 映象网-保险资讯-左侧列表
        'http://edu.hnr.cn/gx/xwsd/': 1301546,  # 映象网-教育速递
        'http://travel.hnr.cn/zhlyzx/': 1301547,  # 映象网-旅游资讯-左侧列表
        'http://news.hnr.cn/djn/': 1301548,  # 映象网-独家-列表
        'http://finance.hnr.cn/zcj/': 1301543,  # 映象网-观察-左侧列表
        'http://finance.hnr.cn/drw/': 1301544,  # 映象网-财经人物-左侧列表
        'http://finance.hnr.cn/yh/': 1301545,  # 映象网-银行资讯-左侧列表
    }

    # start_headers = {
    #     'Host': 'www.dbw.cn',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    # }
    # http://travel.hnr.cn/201906/21/1725.html    http://finance.hnr.cn/201906/21/7837.html
    rules = (
        Rule(LinkExtractor(allow=r'hnr.cn/%s/\d+/\d+.html'% datetime.today().strftime('%Y%m'),
                           deny='video', ), callback='parse_item',
             follow=False),
    )

    custom_settings = {
        # 'DEPTH_LIMIT': 3,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    # http://n.cztv.com/news/13215981.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//h2/text()').extract()[0]
            content_div = xp('//div[@id="text_content"]/div[@id="text_fix"]')[0]
            source_div = xp('//div[@id="share_right"]/p[@class="left"]')[0]
            ps = source_div.re(r'\d{2,4}年\d{1,2}月\d{1,2}日') or source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}')
            pubtime = ps[0]
            og = source_div.re('来源：\w+')
            origin_name = og[0] if og else ""
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,
        )

