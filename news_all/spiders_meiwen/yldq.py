# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.spider_models import NewsRCSpider


class YldqSpider(NewsRCSpider):
    '''语录大全'''
    name = 'yldq'
    mystart_urls = {
        "http://www.yuluju.com/": 2396, # 网站-商业网站-语录大全
        "http://www.yuluju.com/lizhimingyan/": 2398, # 网站-商业网站-语录大全-励志语录
        "http://www.yuluju.com/aiqingyulu/": 2400, # 网站-商业网站-语录大全-爱情语录
        "http://www.yuluju.com/gaoxiaoyulu/": 2401, # 网站-商业网站-语录大全-搞笑语录
        "http://www.yuluju.com/renshenggeyan/": 2402, # 网站-商业网站-语录大全-人生语录
        "http://www.yuluju.com/qingganyulu/": 2403, # 网站-商业网站-语录大全-情感语录
        "http://www.yuluju.com/jingdianyulu/": 2405, # 网站-商业网站-语录大全-经典语录
        "http://www.yuluju.com/shangganyulu/": 2407, # 网站-商业网站-语录大全-伤感语录
        "http://www.yuluju.com/xinqingyulu/": 2408, # 网站-商业网站-语录大全-心情语录
        "http://www.yuluju.com/mingrenmingyan/": 2410, # 网站-商业网站-语录大全-名人语录
    }
    rules = (
        # http://www.yuluju.com/lizhimingyan/11568.html
        Rule(LinkExtractor(allow=(r'yuluju.com/[a-z]+/\d+\.html',),
                           ), callback='parse_item',
             follow=False),
    )
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='title']/h2/text()").extract_first() or self.get_page_title(response)
            # pubtime = xp("//div[@class='info']").re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')[0]
            # # pubtime = Pubtime(pubtime_div.extract())
            #
            #
            origin_name = xp("//div[@class='info']/a/text()").extract_first()
            content_div = xp("//div[@class='content']")[0]

        except:
            return self.produce_debugitem(response, 'xpath error')

        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=datetime.now(),
            origin_name=origin_name,
            content=content,
            media=media
        )
