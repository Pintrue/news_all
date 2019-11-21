# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class DywSpider(NewsRCSpider):
    """大洋网"""
    name = 'dyw'
    mystart_urls = {
        'http://life.dayoo.com/health/': 98330,   #  大洋网
    }
    rules = (
        # http://life.dayoo.com/health/201905/05/154597_52561946.htm
        Rule(LinkExtractor(allow=(r'life.dayoo.com/health/%s/\d{2}/\d+_\d+.htm' % datetime.today().strftime('%Y%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='article-hd']/h1/text()").extract_first() or self.get_page_title(response).split('_')[0]
            # source = xp("//h3[@class='daty']")[0]
            content_div = xp("//div[@id='text_content']")[0]

            pubtime = xp("//div[@class='article-time-source']/span[@class='time']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            

                
            origin_name =xp('//div[@class="article-time-source"]/span[@class="source"]/text()').extract_first('')
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
            origin_name=origin_name,
            
            content=content,
            media=media
        )
