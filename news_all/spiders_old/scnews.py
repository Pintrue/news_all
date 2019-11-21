# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider
import time
from news_all.tools.others import to_list


class ScnewsSpider(NewsRCSpider):
    """四川新闻网"""
    name = 'scnews'
    mystart_urls = {
        'http://sports.newssc.org/zxzx/index.shtml': 1301244,
        # 'http://scnews.newssc.org/2009bwyc/': 1301489,   # 重复
        'http://scnews.newssc.org/2009bwyc/': 1301246,
        # 'http://scnews.newssc.org/2009bwyc/': 1301488,  # 重复
        'http://scnews.newssc.org/2009mlsh/': 1301243,
        'http://china.newssc.org/zxbd/': 1301247,
        'http://finance.newssc.org/2015gn/': 1301487,
    }
    # http://finance.newssc.org/system/20190619/002695829.html
    # http://sports.newssc.org/system/20190520/000966399.htm
    rules = (
        Rule(LinkExtractor(allow=r'newssc\.org/system/%s/\d+\.s?html?' % time.strftime("%Y%m%d"),
                           deny=('video', 'audio'),
                           ),
             callback='parse_item',
             follow=False),
    )
            
    def parse_item(self, response):
        xp = response.xpath
        try:
            # title = xp('//div[@class="content_main_cs_tit"]/h3/text()').extract()[0]
            title = xp('//div[@class="col-xs-12 left"]/h1/text()').extract()[0]
            # 2019-05-20 10:49
            # pubtime = xp('//span[@class="fl content_main_cs_text1"]').re('\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}')[0]
            pubtime = xp('//span[@id="pubtime_baidu "]/text()').extract()[0]
            
                

            cv = xp('//div[@class="content"]/p')
            content, media, video, cover = self.content_clean(cv)
            origin_name = xp('//div[@id="source_baidu "]/a/text()').extract_first('')
        except Exception as e:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media,
        )

    def parse_item_2(self, response):
        
        xp = response.xpath
        try:
            # title = xp('//div[@class="content_main_cs_tit"]/h3/text()').extract()[0]
            title = xp('//div[@class="col-xs-12 col-md-8 left"]/h1/text()').extract()[0]
            # 2019-05-20 10:49
            # pubtime = xp('//span[@class="fl content_main_cs_text1"]').re('\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}')[0]
            pubtime = xp('//span[@id="pubtime_baidu "]/text()').extract()[0]
            
                

            cv = xp('//div[@class="content"]/p')
            content, media, video, cover = self.content_clean(cv)
            origin_name = xp('//div[@id="source_baidu "]/a/text()').extract_first('')
        except Exception as e:
            return self.parse_item_3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media,
        )

    def parse_item_3(self, response):
        
        xp = response.xpath
        try:
            # title = xp('//div[@class="content_main_cs_tit"]/h3/text()').extract()[0]
            title = xp('//div[@class="content_main_cs_tit"]/h3/text()').extract()[0]
            # 2019-05-20 10:49
            pubtime = xp('//span[@class="fl content_main_cs_text1"]').re('\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}')[0]
            # pubtime = xp('//span[@id="pubtime_baidu "]/text()').extract()[0]
            
                

            cv = xp('//div[@class="content"]')[0]
            content, media, video, cover = self.content_clean(cv)
            origin_name = xp('//div[@id="source_baidu "]/a/text()').extract_first('')
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media,
        )
    
    def content_clean(self, content_div, need_video=False, kill_xpaths=None):
        kill_xpaths = to_list(kill_xpaths) + ['//*[starts-with(text(), "本网（平台）所刊载内容之知识产权为四川新闻网传媒")]']
        return super(ScnewsSpider, self).content_clean(content_div, need_video=need_video, kill_xpaths=kill_xpaths)