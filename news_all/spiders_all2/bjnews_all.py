# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2019/5/23 16:39
# # @Author  : wjq
# # @File    : bjnews_all.py
#
#
# import logging
# from datetime import datetime
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import Rule
# from news_all.tools.spider_error import XpathError
#
# from news_all.spider_models import NewsRCSpider, isStartUrl_meta, otherurl_meta
#
#
# class BjnewsAllSpider(NewsRCSpider):
#     chinese_name = """新京报网站"""
#     name = 'bjnews_all'
#     mystart_urls = {
#         'http://www.bjnews.com.cn/ent/': 2681,
#         'http://www.bjnews.com.cn/world/': 2686,
#         'http://www.bjnews.com.cn/news/': 2687,
#     }
#     # http://www.bjnews.com.cn/news/2019/05/23/582397.html
#     rules = (
#         Rule(LinkExtractor(allow=(r'bjnews.com.cn/.*?/%s/\d{2}/\d+.html' % datetime.today().strftime('%Y/%m')),
#                            restrict_xpaths=r'//*[@id="news_ul"]'),
#              callback='parse_item', follow=False),
#         Rule(LinkExtractor(allow=(r'bjnews.com.cn/.*?/?page=[1-8]'),  # 注意这里?前不要转义斜杠
#                            restrict_xpaths=r'//*[@id="page"]/a[@class="next"]'),
#              follow=True, process_request=isStartUrl_meta),
#         Rule(LinkExtractor(allow=(r'bjnews.com.cn.*?\d+.html'), deny=(r'/201[0-8]', r'/20190[1-9]/',),
#                            restrict_xpaths=r'//*[@id="news_ul"]'),
#              process_request=otherurl_meta, follow=False),
#     )
#
#     custom_settings = {
#         'DEPTH_LIMIT': 7,
#     }
#
#     def parse_item(self, response):
#
#         xp = response.xpath
#         try:
#             pubtime = xp('//div[@class="fl ntit_l"]/*[@class="date"]/text()')[0].extract()
#
#                 
#             og = xp('//div[@class="fl ntit_l"]/*[@class="author"]//text()').extract()
#             if og:  # ['   ']
#                 og = og[0].split()
#             origin_name = og[0].split()[0] if og else '新京报'
#             content_div = xp('//div[@class="content"]')[0]
#         except:
#             return self.produce_debugitem(response, 'xpath error')
#
#         if self.video_filter(content_div):
#             return self.produce_debugitem(response, 'video filter')
#         content, media, videos, video_cover = self.content_clean(content_div)
#
#         return self.produce_item(
#             response=response,
#             title=self.get_page_title(response).split('-')[0],  # 北京西三环苏州桥发生交通事故 目前道路已恢复通行 - 国内 - 新京报网
#             pubtime=pubtime,
#             origin_name=origin_name,
#
#             content=content,
#             media=media
#         )