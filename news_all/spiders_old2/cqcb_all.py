# -*- coding: utf-8 -*-


from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class CqcbAllSpider(NewsRCSpider):
    """重庆晨报"""
    name = 'cqcb_all'
    mystart_urls = {
        'http://www.cqcb.com/headline/': 1301314,  # 重庆晨报-头条
        'http://www.cqcb.com/entertainment/': 1301315,  # 重庆晨报-娱乐
        'http://www.cqcb.com/jiaoyu/': 1301310,  # 重庆晨报-教育
        'http://www.cqcb.com/travel/': 1301312,  # 重庆晨报-旅游
        'http://www.cqcb.com/qiche/': 1301313,  # 重庆晨报-汽车
        'http://www.cqcb.com/science/': 1301311,  # 重庆晨报-科普
        'http://www.cqcb.com/highlights/': 1301643,  # 重庆晨报-要闻-左列表
        'http://www.cqcb.com/hot/': 1301309,  # 重庆晨报-重庆
        'http://www.cqcb.com/finance/': 1301308,  # 重庆晨报-金融
    }

    # start_headers = {
    #     'Host': 'www.dbw.cn',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    # }
    # https://www.cqcb.com/xindiaocha/redian/2019-06-24/1702461_pc.html    https://www.cqcb.com/headline/2019-06-24/1703121_pc.html
    rules = (
        Rule(LinkExtractor(allow=r'www.cqcb.com/.*?/%s-\d{2}/\d+_pc.html' % datetime.today().strftime('%Y-%m'),
                           deny='video', ), callback='parse_item',
             follow=False),
    )

    custom_settings = {
        # 'DEPTH_LIMIT': 3,  # 翻页需要设置深度为0 或者 >1
        # 'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//div[@class="tile"]/text()').extract()[0]
            content_div = xp('//div[@class="content"]')[0]
            source_div = xp('//div[@class="post"]')[0]
            pubtime = source_div.re(r'\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}')[0]
            origin_name = "".join(source_div.re(r'[\u4e00-\u9fa5]+'))
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

