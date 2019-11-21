# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.spider_models import NewsRCSpider


class YlwzwSpider(NewsRCSpider):
    '''雨露文章网'''
    name = 'ylwzw'
    mystart_urls = {
        "https://www.vipyl.com/article/1/": 2694, # 网站-商业网站-雨露文章网-人生感悟
        "https://www.vipyl.com/article/379/": 2701, # 网站-商业网站-雨露文章网-早安心语
        "https://www.vipyl.com/article/35/": 2705, # 网站-商业网站-雨露文章网-伤感日志
        "https://www.vipyl.com/article/80/": 2707, # 网站-商业网站-雨露文章网-心情日记
        "https://www.vipyl.com/article/33/": 2715, # 网站-商业网站-雨露文章网-经典美文
        "https://www.vipyl.com/article/139/": 2719, # 网站-商业网站-雨露文章网-经典语录
        "https://www.vipyl.com/article/171/": 2721, # 网站-商业网站-雨露文章网-说说大全
        "https://www.vipyl.com/article/170/": 2724, # 网站-商业网站-雨露文章网-心情短语
        "https://www.vipyl.com/article/172/": 2728, # 网站-商业网站-雨露文章网-经典语句
    }
    rules = (
        # https://www.vipyl.com/article/146/419185.html
        Rule(LinkExtractor(allow=(r'vipyl.com/article/\d+/\d+\.html',),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='Article_title']/h1/text()").extract_first() or self.get_page_title(response).split('_')[0]
            # pubtime = xp("//div[@class='titlexia1']").re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')[0] or xp("//div[@class='titlexia1']").re(r'\d{4}-\d{2}-\d{2}')[0]
            # # pubtime = Pubtime(pubtime_div.extract())
            #
            #
            origin_name = xp("//div[@class='titlexia1']/a/text()").extract_first()
            content_div = xp("//div[@id='changeBodyFont']")[0]

        except:
            return self.parse_item2(response)

        content, media, videos, video_cover = self.content_clean(content_div,kill_xpaths="//div[@id='changeBodyFont']/div")
        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=datetime.now(),
            origin_name=origin_name,
            
            content=content,
            media=media
        )
    def parse_item2(self, response):
        
        xp = response.xpath
        try:
            title = xp("//div[@class='Article_title']/h1/text()").extract_first() or self.get_page_title(response).split('_')[0]
            # pubtime = xp("//div[@class='titlexia1']").re(r'\d{4}-\d{2}-\d{2}')[0]
            # # pubtime = Pubtime(pubtime_div.extract())
            #
            #
            origin_name = xp("//div[@class='titlexia1']/a/text()").extract_first()
            content_div = xp("//div[@id='changeBodyFont']")[0]
        except:
            return self.produce_debugitem(response, 'xpath error')

        content, media, videos, video_cover = self.content_clean(content_div,kill_xpaths="//div[@id='changeBodyFont']/div")
        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=datetime.now(),
            origin_name=origin_name,
            content=content,
            media=media
        )
