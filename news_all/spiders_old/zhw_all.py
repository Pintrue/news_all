# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from news_all.tools.others import to_list

from news_all.spider_models import NewsRCSpider, NewsSpider, NewsCrawlSpider




class ZhwSpider(NewsRCSpider):
    """中华网"""
    name = 'zhw'
    mystart_urls = {
        'http://military.china.com/news/index.html': 18962,  # 中华网-军事-中国军情
        'http://military.china.com/jswh/': 18965,  # 中华网-军事-军事文化动态-左侧列表采集
        'http://military.china.com/important/': 18961,  # 中华网-军事-军事要闻
        # 'http://military.china.com/news/index.html': 18963,  # 中华网-军事-国际军情 #重复
        'http://ent.china.com/tv/index.html': 18959,  # 中华网-娱乐-影视
        'https://ent.china.com/star/news/': 18957,  # 中华网-娱乐-明星
        'http://ent.china.com/movie/index.html': 18958,  # 中华网-娱乐-电影
        'http://money.china.com/': 1200899,  # 中华网-投资-需要确定采集区域
        'http://culture.china.com/expo/': 18992,  # 中华网-文化-博览-左侧列表抓取
        'http://culture.china.com/art/': 18991,  # 中华网-文化-艺文-左侧列表采集
        'http://auto.china.com/zhuanzai/newcar/': 1200734,  # 中华网-新车
        'http://auto.china.com/15yuanchuang/': 18966,  # 中华网-汽车-原创-左侧列表采集
        # 'http://auto.china.com/zhuanzai/newcar/': 18970,  # 中华网-汽车-新车  重复
        'http://auto.china.com/zhuanzai/hangye/': 1200735,  # 中华网-汽车资讯-原创行业新车导购四块
        'http://economy.china.com/industrial/': 18974,  # 中华网-经济-产经商贸
        'http://economy.china.com/domestic/': 18972,  # 中华网-经济-国内宏观
        'http://economy.china.com/consume/': 18975,  # 中华网-经济-时尚消费-左侧列表采集
        'http://economy.china.com/global/': 18973,  # 中华网-经济-海外经济-抓取不到
        # 'http://military.china.com/news/index.html': 1200319,  # 中华网军事-中国军情  重复
        'http://military.china.com/photo/1': 1200292,  # 中华网军事-军事图片-左侧列表
        # 'http://military.china.com/jswh/': 1200293,  # 中华网军事-自媒体-全部抓取  #重复

    }
    rules = (
        # https://military.china.com/news/568/20190609/36357095.html
        #https://military.china.com/jswh/figure/11163298/20190608/36354564.html
        #https://military.china.com/important/11132797/20190612/36381445.html
        #https://ent.china.com/movie/tv/11015529/20190612/36382362.html
        #https://ent.china.com/star/news/11052670/20190612/36383637.html
        #https://ent.china.com/movie/news/205/20190612/36382020.html
        #https://money.china.com/toutiao/2019/0612/13329.html
        #https://culture.china.com/expo/11171063/20190611/36373370.html
        #https://culture.china.com/art/11159887/20190612/36381396.html
        #https://auto.china.com/new/11294.html
        #https://economy.china.com/industrial/11173306/20190612/36386194.html
        #https://economy.china.com/domestic/11173294/20190612/36385763.html
        #https://economy.china.com/consume/11173302/20190611/36371915.html
        #https://economy.china.com/global/11173292/20190611/36374785.html
        #https://military.china.com/jctp/tuku/11172988/20190531/36308184.html  --图集  未解




        # todo
        Rule(LinkExtractor(allow=(r'china.com.*?/\d+.html'),
                           ), callback='parse_item',
             follow=False),
    )

    # todo
    #https://military.china.com/jswh/figure/11163298/20190608/36354564.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='article-main-title']/text()").extract_first()
            # source = xp("//div[@class='time-source']")[0]
            content_div = xp("//div[@id='chan_newsDetail']")[0]

            pubtime = xp("//div[@class='time-source']/span[@class='time']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            print("========="+pubtime)
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            # 
            #     return
            
                
            origin_name = xp('//span[@class="source"]/a/text()').extract_first('')
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

    #https://ent.china.com/movie/tv/11015529/20190612/36382362.html
    def parse_item_2(self, response):
        
        xp = response.xpath
        try:
            title = xp("//h1[@id='chan_newsTitle']/text()").extract_first()
            # source = xp("//div[@class='chan_newsInfo_source']")[0]
            content_div = xp("//div[@id='chan_newsDetail']")[0]

            pubtime = xp("//div[@class='chan_newsInfo_source']/span[@class='time']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            print("=========="+pubtime)
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            # 
            #     return
            
                
            origin_name = xp('//span[@class="source"]/a/text()').extract_first('')
        except:

            return self.parse_item_3(response)

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

    #https://money.china.com/toutiao/2019/0612/13329.html
    def parse_item_3(self, response):
        
        xp = response.xpath
        try:
            title = xp("//h1[@id='chan_newsTitle']/text()").extract_first()
            # source = xp("//div[@id='chan_newsInfo']")[0]
            content_div = xp("//div[@id='chan_newsDetail']")[0]

            pubtime = xp("//div[@id='chan_newsInfo']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            # 
            #     return
            
                
            origin_name = xp('//div[@id="chan_newsInfo"]/a/text()').extract_first('')
        except:

            return self.parse_item_4(response)

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

    #https://auto.china.com/new/11294.html
    def parse_item_4(self, response):
        
        xp = response.xpath
        try:
            title = xp("//h1[@id='arti-title']/text()").extract_first()
            # source = xp("//div[@id='chan_newsInfo']")[0]
            content_div = xp("//div[@id='js-arti-detail']")[0]

            pubtime = xp("//div[@class='arti-info']/span[@class='time']/text()").extract_first()
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            # 
            #     return
            
                
            origin_name = xp('//span[@class="source"]/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")
            # return self.parse_item_4(response)

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

