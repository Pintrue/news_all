# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from news_all.tools.others import to_list

from news_all.spider_models import NewsRCSpider, NewsSpider, NewsCrawlSpider


class ZgqxjSpider(NewsRCSpider):
    '''中国气象局'''
    name = 'zgqxj'
    mystart_urls = {'http://www.cma.gov.cn/2011xwzx/2011xqxxw/2011xzytq/': 1302263,   #  中国气象局
    }
    rules = (
        # todo
        # http://www.cma.gov.cn/2011xwzx/2011xqxxw/2011xzytq/201906/t20190611_526856.html
        Rule(LinkExtractor(allow=(r'cma.gov.cn/2011xwzx/2011xqxxw/2011xzytq/%s/\S+.html' % datetime.today().strftime('%Y%m'),),), callback='parse_item',
             follow=False),
    )
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//div[@class="news_text"]/h1/text()').extract_first()
            # title = self.get_full_title(title_div, response)
            # todo
            content_div = xp('//div[@class="TRS_Editor"]')[0]
            # 过滤视频

            # if self.video_filter(content_div) or self.page_turn_filter(content_div):
            #     return
            pubtime = xp('//div[@class="news_textspan"]/div[1]/span[2]/text()').extract_first().replace('发布时间：','').strip()
            # 
            #     return
            
                
            origin_name = xp('//div[@class="news_textspan"]/div[1]/span[1]/text()').extract_first().replace('来源：','').strip()

        except:
            return self.produce_debugitem(response, "xpath error")
            # return self.parse_item_2(response)
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
