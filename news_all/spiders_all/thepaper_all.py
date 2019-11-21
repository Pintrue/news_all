#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 18:54
# @Author  : wjq
# @File    : kr36_all.py
from copy import deepcopy
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class ThepaperAllSpider(NewsRCSpider):
    chinese_name = """澎湃网站"""
    name = 'thepaper_all'
    mystart_urls = {
        'https://www.thepaper.cn/channel_25951': 2595,
        'https://www.thepaper.cn/list_27234': 2596,

        # 老爬虫的
        'http://www.thepaper.cn/list_25429': 1201005,  # 澎湃-国际
        'http://www.thepaper.cn/list_25448': 1200012,  # 澎湃-生活-有戏
        'http://www.thepaper.cn/list_25428': 1201006,  # 澎湃-直击现场
        'http://www.thepaper.cn/list_26878': 81023,  # 澎湃新闻-思想-上海书评
        'http://www.thepaper.cn/list_25536': 81034,  # 澎湃新闻-思想-专栏
        'http://www.thepaper.cn/list_26937': 81028,  # 澎湃新闻-思想-古代艺术
        'http://www.thepaper.cn/list_25456': 81032,  # 澎湃新闻-思想-市政厅
        'http://www.thepaper.cn/list_26506': 81035,  # 澎湃新闻-思想-异次元
        'http://www.thepaper.cn/list_25483': 81024,  # 澎湃新闻-思想-思想市场
        'http://www.thepaper.cn/list_26525': 81022,  # 澎湃新闻-思想-思想湃
        'http://www.thepaper.cn/list_25450': 81029,  # 澎湃新闻-思想-文化课
        'http://www.thepaper.cn/list_25445': 81031,  # 澎湃新闻-思想-澎湃研究所
        'http://www.thepaper.cn/list_25444': 81021,  # 澎湃新闻-思想-社论
        'http://www.thepaper.cn/list_25457': 81025,  # 澎湃新闻-思想-私家历史
        'http://www.thepaper.cn/list_25574': 81026,  # 澎湃新闻-思想-翻书党
        'http://www.thepaper.cn/list_25455': 81027,  # 澎湃新闻-思想-艺术评论
        'http://www.thepaper.cn/list_25446': 81033,  # 澎湃新闻-思想-请讲
        'http://www.thepaper.cn/list_25482': 81030,  # 澎湃新闻-思想-逝者
        'http://www.thepaper.cn/channel_25950': 300,  # 澎湃新闻-时事
        'http://www.thepaper.cn/channel_25953': 10057,  # 澎湃新闻-生活
        'http://www.thepaper.cn/list_25434': 81013,  # 澎湃新闻-生活-100%公司
        'http://www.thepaper.cn/list_26202': 81007,  # 澎湃新闻-生活-亲子学堂
        'http://www.thepaper.cn/list_26609': 81009,  # 澎湃新闻-生活-文艺范
        'http://www.thepaper.cn/list_26862': 81010,  # 澎湃新闻-生活-楼市
        'http://www.thepaper.cn/list_26490': 81011,  # 澎湃新闻-生活-汽车圈
        'http://www.thepaper.cn/list_25769': 81005,  # 澎湃新闻-生活-生活方式
        'http://www.thepaper.cn/list_26015': 81003,  # 澎湃新闻-生活-私·奔
        'http://www.thepaper.cn/list_25842': 81004,  # 澎湃新闻-生活-私家地理
        'http://www.thepaper.cn/list_26404': 81008,  # 澎湃新闻-生活-赢家
        'http://www.thepaper.cn/list_25599': 81002,  # 澎湃新闻-生活-运动家
        'http://www.thepaper.cn/': 10056,  # 澎湃新闻-精选
        'http://www.thepaper.cn/list_26173': 304,  # 澎湃新闻-视界
        'http://www.thepaper.cn/channel_25951': 301,  # 澎湃新闻-财经
        'http://www.thepaper.cn/list_25433': 81015,  # 澎湃新闻-财经-地产界
        'http://www.thepaper.cn/list_25485': 81019,  # 澎湃新闻-财经-澎湃商学院
        'http://www.thepaper.cn/list_25437': 81018,  # 澎湃新闻-财经-牛市点线面
        'http://www.thepaper.cn/list_25436': 81014,  # 澎湃新闻-财经-能见度
        'http://www.thepaper.cn/list_25432': 81020,  # 澎湃新闻-财经-自贸区连线
        'http://www.thepaper.cn/list_25438': 81016,  # 澎湃新闻-财经-财经上下游
        'http://www.thepaper.cn/list_25435': 81017,  # 澎湃新闻-财经-金改实验室
        'http://www.thepaper.cn/list_25942': 305,  # 澎湃新闻-身体
    }

    # https://www.thepaper.cn/newsDetail_forward_3541395
    rules = (
        # https://h5.thepaper.cn/html/interactive/2019/05/ke_chuang_5th/index.html
        Rule(LinkExtractor(allow=(r'thepaper.cn/.*?_\d{5,}'),
                           deny=(r'h5.thepaper.cn/', r'/channel_\d+', r'/list_\d+', r'/asktopic', r'/interactive/',),
                           restrict_xpaths=r'//div[@id="indexMasonry"]'
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'thepaper.cn'),
                           deny=(r'/201[0-8]', r'/20190[1-9]/', r'h5.thepaper.cn/', r'/channel_\d+', r'/list_\d+',
                                 r'/asktopic', r'/interactive/'),
                           restrict_xpaths=r'//div[@id="indexMasonry"]'),
             process_request=otherurl_meta, follow=False),
    )
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    def parse_item(self, response):
        xp = response.xpath
        try:
            ps = xp('//div[@class="news_about"]') or xp('//div[@class="about_news"]')
            ps = ps.re('\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}')  # 2019-05-27 18:13 来源：澎湃新闻
            pubtime = ps[0]
            og = xp('//div[@class="news_about"]').re(r'来源：\w{2+}')  # news_about
            if og:  # ['   ']
                og = og[0].split()
            origin_name = og[0].split()[0] if og else '澎湃新闻'
            # https://m.thepaper.cn/newsDetail_forward_3558771
            content_div = xp('//div[@class="news_txt"]') or xp('//div[@class="news_part news_part_limit"]')
            title = xp('//*[@class="news_title"]/text()').extract_first('') or self.get_page_title(response).split('-')[
                0]
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.parse_item2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item2(self, response):
        xp = response.xpath
        try:
            pubtime = xp('//div[@class="video_info_left"]/span[1]/text()').extract_first('')
            content_div = xp('//video[re:match(@id,"^video\d+$")]').extract() + xp('//div[@class="video_txt_l"]/p').extract()
            title = xp('//div[@class="video_txt_t"]/h2/text()').extract_first('') or self.get_page_title(response).split('_')[
                0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media,
            videos=videos
        )