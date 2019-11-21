# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2019/8/21 15:42
# # @Author  : wjq
#
# from datetime import datetime
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import Rule
# from news_all.spider_models import NewsRCSpider, otherurl_meta
#
#
# class CnenergynewsVSpider(NewsRCSpider):
#     """中国能源网 视频"""
#     name = 'cnenergynews_video'
#     mystart_urls = {
#         'http://www.cnenergynews.cn/shipin/': 3789
#     }
#
#     # http://www.cnenergynews.cn/yq/trq/201511/t20151119_246951.html
#     # http://www.cnenergynews.cn/yw/201903/t20190305_753313.html
#     # todo
#     rules = (
#         Rule(LinkExtractor(allow=(r'cnenergynews.cn.*?/%s/t\d+_\d+.html') % datetime.today().strftime('%Y%m'),
#                            restrict_xpaths="//div[@class='main4_left_m1']"),
#              callback='parse_item', follow=False),
#         Rule(LinkExtractor(allow=(r'cnenergynews.cn.*?\d+.htm'),
#                            deny=(r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/'),),
#              process_request=otherurl_meta,
#              follow=False),
#     )
#
#     def parse_item(self, response):
#         print('-'*50, response.url)
#         xp = response.xpath
