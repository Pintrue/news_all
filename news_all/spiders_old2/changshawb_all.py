# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Cswb_allSpider(NewsRCSpider):
    """长沙晚报"""
    name = 'cswb'
    mystart_urls = {
        'https://www.icswb.com/channel-list-channel-204.html': 1301291,  # 长沙晚报-健康
        'https://www.icswb.com/channel-list-channel-151.html': 1301294,  # 长沙晚报-民生追踪
        'https://www.icswb.com/channel-list-channel-158.html': 1301295,  # 长沙晚报-民生追踪-左侧列表
        'https://www.icswb.com/channel-list-channel-100104.html': 1301292,  # 长沙晚报-科教文卫
        'https://www.icswb.com/channel-list-channel-168.html': 1301290,  # 长沙晚报-经济
        'https://www.icswb.com/channel-list-channel-152.html': 1301293,  # 长沙晚报-都市

    }
    rules = (
        #https://www.icswb.com/h/161/20190621/609292.html
        #https://www.icswb.com/h/100104/20190624/609659.html
        Rule(LinkExtractor(allow=(r'icswb.com/h/\d+/%s\d{2}/\d+.html' % datetime.today().strftime('%Y%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='am-article-title']/text()").extract_first()
            source = xp("//p[@class='am-article-meta']")[0]
            content_div = xp("//div[@class='am-article-bd']/div[3]")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            
            
            origin_name = xp("//p[@class='am-article-meta']/text()").extract_first('').replace('稿源：', '')
        except:
            return self.self.produce_debugitem(response, "xpath error")

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )
