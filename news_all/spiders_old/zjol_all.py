# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
import logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider


class ZjolAllSpider(NewsRCSpider):
    """浙江在线"""
    name = 'zjol_all'

    mystart_urls = {
        'http://zjtyol.zjol.com.cn/tyjsb/': 1301572,  # 浙江在线-体育即时报-左侧列表
        'http://health.zjol.com.cn/jkxw/': 1301562,  # 浙江在线-健康新闻-左侧列表
        'http://health.zjol.com.cn/ycxw/': 1301564,  # 浙江在线-健康网原创新闻-
        'http://zjtyol.zjol.com.cn/dsww/': 1301571,  # 浙江在线-地市网闻-列表
        'http://edu.zjol.com.cn/jyjsb/ye/': 1301566,  # 浙江在线-幼儿-左侧列表
        'http://edu.zjol.com.cn/jyjsb/jyfb/': 1301565,  # 浙江在线-教育发布-左侧列表
        'http://gotrip.zjol.com.cn/xw14873/lyjsb/': 1301569,  # 浙江在线-旅游即时报列表
        'http://gotrip.zjol.com.cn/xw14873/ycll14875/': 1301570,  # 浙江在线-旅游原创
        'http://zjtyol.zjol.com.cn/zjrd/': 1301573,  # 浙江在线-浙江热点列表
        'http://gotrip.zjol.com.cn/xw14873/cytx/': 1301568,  # 浙江在线-潮游天下
        'http://health.zjol.com.cn/nnb/': 1301563,  # 浙江在线-牛牛掰-左侧列表
        'http://edu.zjol.com.cn/jyjsb/zh/': 1301567,  # 浙江在线-综合-列表
        'http://zjtyol.zjol.com.cn/zhzx/': 1301574,  # 浙江在线-综合资讯-左侧列表

    }

    # start_headers = {
    #     'Host': 'www.dbw.cn',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    # }
    # http://zjtyol.zjol.com.cn/tyjsb/201906/t20190624_10400197.shtml    http://zjtyol.zjol.com.cn/tyjsb/201906/t20190619_10371900.shtml
    rules = (
        Rule(LinkExtractor(allow=r'zjtyol.zjol.com.cn/.*?/%s/t\d+_\d+.shtml' % datetime.today().strftime('%Y%m'),
                           deny='video', ), callback='parse_item',
             follow=False),
    )

    custom_settings = {
        # 'DEPTH_LIMIT': 3,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//div[@class="contTit"]/text()').extract()[0]
            content_div = xp('//div[@class="contTxt"]')[0]
            source_div = xp('//div[@class="time"]')[0]
            pubtime = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}')[0]
            
            
        except:
            return self.produce_debugitem(response, "xpath error")
        origin_name = source_div.xpath('./span[@id="source_baidu"]/text()').extract_first('').replace('来源', '').strip()
        # origin_name = "".join(source_div.re(r'[\u4e00-\u9fa5]+')).replace('来源', '').strip()
        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media,
            videos=videos,
        )

