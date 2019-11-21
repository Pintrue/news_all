# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Duocai_allSpider(NewsRCSpider):
    """多彩贵州网"""
    name = 'dcgzw'
    mystart_urls = {
        'http://ent.gog.cn/dianyds/zonghys/': 1301154,   #  多彩贵州网 娱乐-影视-左侧列表
        'http://travel.gog.cn/lvydt/': 1301383,   #  多彩贵州网 旅游-旅游资讯列表
        'http://travel.gog.cn/yousj/': 1301384,   #  多彩贵州网 旅游-游世界-左侧列表
        'http://gongyi.gog.cn/gyxw/': 1301157,   #  多彩贵州网-公益新闻-左侧列表
    }
    rules = (
        #http://gongyi.gog.cn/system/2019/06/14/017274003.shtml
        #http://travel.gog.cn/system/2018/09/13/016804307.shtml
        #http://ent.gog.cn/system/2019/06/17/017275958.shtml
        Rule(LinkExtractor(allow=(r'(?:ent|travel|gongyi).gog.cn/system/%s/\d{2}/\d+.shtml' % datetime.today().strftime('%Y/%m'),),
                           ), callback='parse_item',
             follow=False),

    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='heading']/h1/text()").extract_first() or self.get_page_title(response).replace('多彩贵州网 -', '')
            source = xp("//div[@class='info']")[0]
            content_div = xp("//div[@class='content']")[0]

            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            
            
            origin_name =xp('//div[@class="info"]/text()').extract_first('')
        except:
            return self.parse_item_2(response)

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
            title = xp("//div[@class='title']/h1/text()").extract_first() or self.get_page_title(response).replace('多彩贵州网 -', '')
            # source = xp("//div[@class='info']")[0]
            content_div = xp("//div[@class='text mt20']")[0]

            pubtime = xp("//h4/span[1]").re(r'\d{2,4}/\d{1,2}/\d{1,2}')[0]
            
            
            origin_name = xp('//h4/span[2]/text()').extract_first('')
        except:
            return self.parse_item_3(response)

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

    def parse_item_3(self, response):
        
        xp = response.xpath
        try:
            title = xp("//span[@class='articletitle_p22']/text()").extract_first() or self.get_page_title(response).replace('多彩贵州网 -', '')
            source = xp("//span[@class='p12 LightGray2']")[0]
            content_div = xp("//td[@class='p16']")[0]

            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            
            
            origin_name = xp('//span[@class="p12 LightGray2"]/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

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
