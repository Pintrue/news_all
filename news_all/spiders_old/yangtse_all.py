# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider


class YangtseAllSpider(NewsRCSpider):
    """扬子晚报"""
    name = 'yangtse_all'

    # mystart_urls = {
    #     'http://www.yangtse.com/app/zhongguo/': 1301538,  # 扬子晚报-中国-左侧列表
    #     'http://www.yangtse.com/app/health/': 1301533,  # 扬子晚报-名医团
    #     'http://www.yangtse.com/app/fashion/': 1301534,  # 扬子晚报-汽车-左侧列表
    #     'http://www.yangtse.com/app/world/': 1301536,  # 扬子晚报-环球-左侧列表
    #     'http://www.yangtse.com/app/qinggan/': 1301535,  # 扬子晚报-社会-左侧列表
    #     'http://www.yangtse.com/app/internet/': 1301539,  # 扬子晚报-科技-左侧列表
    #     'http://www.yangtse.com/app/politics/': 1301537,  # 扬子晚报-要闻-左侧列表
    #     'http://www.yangtse.com/jiankang/': 18327,  # 扬子晚报网-健康
    #     'http://www.yangtse.com/nanjing/': 18317,  # 扬子晚报网-南京
    #     'http://www.yangtse.com/guonei/': 18321,  # 扬子晚报网-国内
    #     'http://www.yangtse.com/jiaoyu/': 18325,  # 扬子晚报网-教育
    #     'http://www.yangtse.com/wenyu/': 18319,  # 扬子晚报网-文娱
    #     'http://www.yangtse.com/shiping/': 18326,  # 扬子晚报网-时评-需要确定采集区域
    #     'http://www.yangtse.com/jiangsu/': 18316,  # 扬子晚报网-江苏
    #     'http://www.yangtse.com/shehui/': 18318,  # 扬子晚报网-社会
    #     'http://www.yangtse.com/yaowen/': 18315,  # 扬子晚报网-要闻
    #
    # }

    mystart_urls = {
        'http://www.yangtse.com/': 1,
        'http://www.yangtse.com/app/livelihood/': 2,
        'http://www.yangtse.com/app/zhengzai/': 3,
        'http://www.yangtse.com/app/jiangsu/kanjiangsu/': 4,
        'http://www.yangtse.com/app/jiangsu/nanjing/': 5,
        'https://news.yangtse.com/clist/suzhou.html': 6,
        'http://www.yangtse.com/app/politics/': 7,
        'http://www.yangtse.com/shiping/': 8,
        'http://www.yangtse.com/app/qinggan/': 9,
        'http://www.yangtse.com/app/finance/': 10,
        'http://www.yangtse.com/app/health/': 11,
        'http://www.yangtse.com/app/education/': 12,
        'http://www.yangtse.com/app/ent/': 13,
        'http://www.yangtse.com/app/bzxc/': 14,
        'http://www.yangtse.com/app/sports/': 15,
        'http://www.yangtse.com/app/automobile/': 16,
        'http://www.yangtse.com/app/internet/': 17,
        'http://house.yangtse.com/index.html': 18,
        'http://house.yangtse.com/fczx/lpsdindex.html#pg=1': 19,
        'http://house.yangtse.com/fczx/zxzxindex.html#pg=1': 20,
        'http://house.yangtse.com/fczx/jrttindex.html#pg=1': 21,
        'http://house.yangtse.com/newsalecomm/loupanlist1.html#pg=1': 22,
        'http://www.yangtse.com/app/qianyan/': 23,
        'http://www.yangtse.com/app/zhongguo/': 24,
        'http://www.yangtse.com/app/world/': 25,
        'http://news.yangtse.com/clist/community.html': 26,
        'http://sz.yangtse.com/': 27,
        'http://www.yangtse.com/yaowen/': 28,
    }

    # http://www.yangtse.com/app/zhongguo/2019-06-21/720530.html
    # http://www.yangtse.com/app/zhongguo/2019-06-21/720522.html
    rules = (
        Rule(LinkExtractor(allow=r'yangtse.com.*?/%s-\d{2}/\d+.html' % datetime.today().strftime('%Y-%m'),
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
            title = xp('//div[@class="text-title"]/text() | //div[@class="nr_bt"]/h5/text()').extract()[0]
            content_div = xp('//div[@id="content"] | //div[@class="nr_text"]')[0]
            source_div = xp('//div[@class="text-time"] | //div[@class="nr_bt"]/h6')[0]
            pubtime = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}')[0]
            origin_name = "".join(source_div.re(r'[\u4e00-\u9fa5]+'))
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True)
                
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

