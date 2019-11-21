# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class DhwSpider(NewsRCSpider):
    """大河网"""
    name = 'dhw'
    mystart_urls = {
        'https://jr.dahe.cn/cjxw/': 1301348,  # 大河网 产经
        'https://edu.dahe.cn/2jyyw/': 1301350,  # 大河网 教育要闻
        'https://hnwj.dahe.cn/5xw/': 1301349,  # 大河网 新闻
        'https://tour.dahe.cn/': 1301352,  # 大河网 旅游-左侧列表
        'https://edu.dahe.cn/2xyxw/': 1301351,  # 大河网 校园新闻-列表新闻
        'https://auto.dahe.cn/': 1301353,  # 大河网-汽车-列表部分

    }
    rules = (
        #https://hnwj.dahe.cn/2019/06-17/498919.html
        #https://edu.dahe.cn/2019/06-13/499226.html
        #https://tour.dahe.cn/2019/06-17/499178.html
        Rule(LinkExtractor(allow=(r'(?:jr|edu|hnwj|tour|edu|auto).dahe.cn/%s-\d{2}/\d+.html'
                                  % datetime.today().strftime('%Y/%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//*[@id='4g_title']/text()").extract_first() or self.get_page_title(response).split('-')[0]
            source = xp("//div[@class='time_source mt20']")[0]
            content_div = xp("//div[@id='mainCon']")[0]

            pubtime = source.re(r'\d{2,4}年\d{1,2}月\d{1,2}日')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            
            
            origin_name =xp('//p[@id="source_baidu"]/text()').extract_first('')
        except:
            return self.parse_item_2(response)

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

    def parse_item_2(self, response):
        
        xp = response.xpath
        try:
            title = xp("//div[@class='xinwen-ttl']/p/text()").extract_first() or self.get_page_title(response).split('-')[0]
            # source = xp("//div[@class='xinwen-ttl']/p")[0]
            content_div = xp("//div[@id='mainCon']")[0]

            pubtime = xp("//i[@id='pubtime_baidu']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            
            
            origin_name =xp('//span[@id="source_baidu"]/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

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

