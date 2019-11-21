# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from news_all.spider_models import NewsRCSpider


class Zgzzrs_allSpider(NewsRCSpider):
    """中国组织人事报"""
    name = 'zgzzrsb'
    mystart_urls = {
        'http://www.zuzhirenshi.com/innerpage/29624': 1301642,  # 中国组织人事报-视觉新闻
    }
    rules = (
        #http://www.zuzhirenshi.com/showinfo/8677ef24-0c65-4005-a6df-51ae3731684e
        Rule(LinkExtractor(allow=(r'zuzhirenshi.com/showinfo/\w+.*?'),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='innertop']/text()").extract_first()
            source = xp("//div[@class='innertop']/div[4]")[0]
            content_div = xp("//div[@class='innercontent']")[0]

            pubtime = source.re(r'\d{2,4}年\d{1,2}月\d{1,2}日')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            

            
            # origin_name =xp('//div[@class="daty_con"]/em[@class="e e1"]/text()').extract_first('')
            origin_name = ""
        except:
            return self.produce_debugitem(response, "xpath error")
            # return self.parse_item_2(response)

        # 过滤视频
        # if self.video_filter(content_div) or self.page_turn_filter(content_div):
        #     return

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name="",
            
            content=content,
            media=media
        )
