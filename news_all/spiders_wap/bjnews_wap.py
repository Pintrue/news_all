# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2019/5/20 15:29
# # @Author  : wjq
# # @File    : bjnews_wap.py
#
# from datetime import datetime
# import json
# from scrapy import Request
# from scrapy.conf import settings
# from news_all.spider_models import NewsRSpider
# import re
#
#
# img_pattern = re.compile(r'\{\{IMG_(\d+)\}\}')  # {{IMG_0}}
#
#
# class BjnewsWapSpider(NewsRSpider):
#     chinese_name = """新京报app"""
#     name = 'bjnews_app'
#     custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
#
#     mystart_urls = {
#         # 'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=90': 3677,  # 视频暂不抓
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=2': 3678,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=3': 3679,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=5': 3680,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=6': 3681,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=92': 3682,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=8': 3683,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=7': 3684,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=9': 3685,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=10': 3686,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=11': 3687,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=12': 3688,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=13': 3689,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=14': 3690,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=16': 3691,
#         'https://api.bjnews.com.cn/api/v101/news/news_list.php?page=1&channel_id=93': 3692
#     }
#
#     def parse(self, response):
#         rs = json.loads(response.text)
#         if rs.get('code') != 0:
#             return self.produce_debugitem(response, 'json error')
#
#         data = rs.get('data')
#         for i in data:
#             # https://api.bjnews.com.cn/api/v101/news/manuscript_detail.php?uuid=155848734114872&time=1558490257&sign=0b6a39d0a91173c38160b9791557d0d7
#             uuid = i.get('uuid')
#             news_url = 'https://api.bjnews.com.cn/api/v101/news/manuscript_detail.php?uuid=' + uuid
#
#             row = i.get('row')
#             if not row:
#                 print('have no row')
#                 continue
#             # 实际视频地址未解析出来 https://media.bjnews.com.cn/video/2019/05/22/4795197907579963268.mp4
#             ext_data = row.get('ext_data', {})
#             if ext_data:
#                 if ext_data.get('video_url'):  # 排除视频  不论有无视频i.get("has_video") = "0"
#                     continue
#             title = row.get('title')
#             pubtime = row.get('publish_time')
#
#                 yield self.produce_debugitem(response, 'pubtime 24 hours after', srcLink=news_url)
#                 continue
#             # http://m.house.sina.com.cn/m.leju.com/?id=6536508484366938288&city=bj&site=tg&ctl=SinaApp&act=info&source=m_sina_appnews&source_ext=sina_app&fromsinago=1
#             if not pubtime:
#                 pubtime = datetime.now()
#
#             yield Request(
#                 url=news_url,
#                 callback=self.parse_item,
#                 meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
#                       'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
#             )
#
#     def parse_item(self, response):
#         rs = json.loads(response.text)
#         if rs.get('code') != 0:
#             logger_hive.error(JsonNoMsg(response, self.source_id_meta_dict[response.meta['source_id']]).info)
#             return
#         data = rs.get('data')
#         if data.get('video_urls'):
#             return  # 排除视频
#         origin_name = data.get('head_author').split('|')[0]
#
#         content_div = data.get('content')
#         if '{{IMG_0}}' in content_div:
#             img_list = data.get('image_urls', [])
#             media = {}
#             if img_list:
#                 for i, j in enumerate(img_list):
#                     media.setdefault("images", {})
#                     media['images'][str(i+1)] = {"src": j}
#                 content_div, img_count = self.image_clean(content_div)
#                 if img_count != len(img_list):
#                     self.log('图片数量不符!')
#             content = self.parser.cleaner.clean_html(content_div)  # 再去不要的dom 和 属性
#         else:
#             content, media, _, _ = self.content_clean(content_div)
#
#         return self.produce_item(
#             response=response,
#             title=response.request.meta['title'],
#             pubtime=response.request.meta['pubtime'],
#             origin_name=origin_name,
#             content=content,
#             media=media
#         )
#
#     def image_clean(self, content):
#         # {{IMG_0}}
#         fr = re.finditer(img_pattern, content)
#         new_content = ''
#         img_count = 0
#         for i, j in enumerate(fr):
#             st = content.find(j.group())
#             end = st + len(j.group())
#             new_content += content[:st] + '${{%s}}$' % (i + 1)
#             content = content[end:]
#             img_count += 1
#
#         new_content += content
#         new_content.replace('$$', '$<br>$')  # 连续2图片加换行
#         return new_content, img_count