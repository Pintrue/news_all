# # -*- coding: utf-8 -*-
#
# from datetime import datetime
# from scrapy.spiders import Rule
# from scrapy.linkextractors import LinkExtractor
# from news_all.spider_models import NewsRCSpider
#
#
# class DwxSpider(NewsRCSpider):
#     '''短文学'''
#     name = 'dwx'
#     mystart_urls = {
#         "https://www.duanwenxue.com/": 2816,  # 网站-商业网站-短文学-首页
#         "https://www.duanwenxue.com/shanggan/": 2820,  # 网站-商业网站-短文学-伤感文章
#         "https://www.duanwenxue.com/qinggan/": 2822,  # 网站-商业网站-短文学-情感日志
#         "https://www.duanwenxue.com/diary/": 2824,  # 网站-商业网站-短文学-心情日记
#         "https://www.duanwenxue.com/sanwen/": 2827,  # 网站-商业网站-短文学-散文精选
#         "https://www.duanwenxue.com/shige/": 2829,  # 网站-商业网站-短文学-诗歌大全
#         # "https://www.duanwenxue.com/yuju/": 2831, # 网站-商业网站-短文学-经典语句
#         "https://www.duanwenxue.com/sanwen/suibi/": 2833,  # 网站-商业网站-短文学-散文随笔
#         "https://www.duanwenxue.com/qinggan/meiwen/": 2835,  # 网站-商业网站-短文学-美文欣赏
#         # "https://www.duanwenxue.com/yuju/shanggan/": 2837, # 网站-商业网站-短文学-伤感的句子
#         # "https://www.duanwenxue.com/yuju/youmei/": 2839, # 网站-商业网站-短文学-优美的句子
#         # "https://www.duanwenxue.com/yuju/weimei/": 2840, # 网站-商业网站-短文学-唯美的句子
#         # "https://www.duanwenxue.com/yuju/shangxin/": 2841, # 网站-商业网站-短文学-伤心的句子
#         "https://www.duanwenxue.com/duanwen/mingyan/": 2842,  # 网站-商业网站-短文学-名言名句
#         "https://www.duanwenxue.com/yuju/xiangnian/": 2843,  # 网站-商业网站-短文学-想念的句子
#         "https://www.duanwenxue.com/duanwen/lizhi/": 2847,  # 网站-商业网站-短文学-励志签名
#         "https://www.duanwenxue.com/duanwen/gerenqianming/": 2848,  # 网站-商业网站-短文学-个人签名
#         # "https://www.duanwenxue.com/huayu/ganren/": 2849, # 网站-商业网站-短文学-感人的话
#         "https://www.duanwenxue.com/yulu/aiqing/": 2850,  # 网站-商业网站-短文学-爱情语录
#         "https://www.duanwenxue.com/huayu/biaobai/": 2852,  # 网站-商业网站-短文学-表白的话
#         "https://www.duanwenxue.com/juzi/beishang/": 2853,  # 网站-商业网站-短文学-悲伤的句子
#         "https://www.duanwenxue.com/yulu/gaoxiao/": 2854,  # 网站-商业网站-短文学-搞笑语录
#         "https://www.duanwenxue.com/yulu/aiqingxuanyan/": 2855,  # 网站-商业网站-短文学-爱情宣言
#         # "https://www.duanwenxue.com/juzi/biaobai/": 2856, # 网站-商业网站-短文学-表白的句子
#         # "https://www.duanwenxue.com/duanwen/geyan/": 2857, # 网站-商业网站-短文学-人生格言
#         "https://www.duanwenxue.com/yulu/yijuhua/": 2858,  # 网站-商业网站-短文学-一句话经典
#         "https://www.duanwenxue.com/huayu/lizhi/": 2861,  # 网站-商业网站-短文学-励志的话
#         "https://www.duanwenxue.com/yulu/shangxinqianming/": 2863,  # 网站-商业网站-短文学-伤心的个性
#         "https://www.duanwenxue.com/huayu/zheli/": 2865,  # 网站-商业网站-短文学-有哲理的话
#     }
#     rules = (
#         # https://www.duanwenxue.com/article/4845194.html
#         Rule(LinkExtractor(allow=(r'duanwenxue.com/article/\d+\.html',),
#                            ), callback='parse_item',
#              follow=False),
#     )
#
#     def parse_item(self, response):
#         
#         xp = response.xpath
#         try:
#             title = xp("//div[@class='row-article']/h1/text()").extract_first()
#             # pubtime = xp("//div[@class='text']").re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')[0]
#             # # pubtime = Pubtime(pubtime_div.extract())
#             #
#             #
#             origin_name = xp("//div[@class='text']/text()[2]").extract_first().replace('次', '')
#             content_div = xp("//div[@class='article-content']")[0]
#
#         except:
#             return self.parse_item2(response)
#
#         content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[
#             "//div[@class='article-content']/div[@class='article-content-ad-1']",
#             "//div[@class='article-content']/p[last()]",
#             "//div[@class='wxh']",
#             "//div[@id='shangDiv']",
#             "//div[@class='guide']",
#             ])
#         return self.produce_item(
#             response=response,
#             title=title,
#             # self.get_page_title(response).split('_')[0]
#             pubtime=datetime.now(),  # pubtime,
#             origin_name=origin_name,
#             content=content,
#             media=media
#         )
#
#     def parse_item2(self, response):
#         
#         xp = response.xpath
#         try:
#             title = xp("//div[@class='row-article']/h1/text()").extract_first()
#             # pubtime = xp("//div[@class='text']").re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')[0]
#             # pubtime = Pubtime(pubtime_div.extract())
#             #
#             #
#             origin_name = xp("//div[@class='text']/text()[2]").extract_first().replace('次', '')
#             content_div = xp("//div[@class='article-content article-content-sige']")[0]
#
#         except:
#             return self.produce_debugitem(response, 'xpath error')
#
#         content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[
#             "//div[@class='article-content article-content-sige']/div[@class='article-content-ad-1']",
#             "//div[@class='article-content article-content-sige']/p[last()]",
#             "//div[@class='wxh']",
#             "//div[@id='shangDiv']",
#             "//div[@class='guide']",
#             ])
#         return self.produce_item(
#             response=response,
#             title=title,
#             # self.get_page_title(response).split('_')[0]
#             pubtime=datetime.now(),  # pubtime,
#             origin_name=origin_name,
#             content=content,
#             media=media
#         )
