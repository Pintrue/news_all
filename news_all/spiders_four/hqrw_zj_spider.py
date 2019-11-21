# -*- coding: utf-8 -*-
# @Time   : 2019/3/5 上午10:28
# @Author : NewmanZhou
# @Project : news_all
# @FileName: hqrw_zj_spider.py

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class HqrwZJSpipder(NewsRCSpider):
    name = 'hqrw_zj_spider'

    # 环球人物 ==》 主角
    mystart_urls = {
        'http://www.hqrw.com.cn/figure/': 557,  # '主角'
        'http://www.hqrw.com.cn/politics/': 558,  # '政面孔'
    }
    # http://www.hqrw.com.cn/2018/1112/82215.shtml
    rules = (Rule(LinkExtractor(allow=r'hqrw.com.cn/.*?\d+.s?htm', deny=('video', 'audio'),
                                restrict_xpaths='//div[@class="list-wrap row"]'),
                  callback='parse_item', follow=False),
             )

    def parse_item(self, response):
        try:
            xp = response.xpath
            title = xp('//div[@class="row"]/div[2]/h3/text()').extract()[0]
            pubtime = xp('//li[@class="time"]/text()').extract()[0]
            origin_name = xp('//li[@class="source"]/span/text()').extract()[0]
            cv = xp("//div[@class='passage-content  contenth article-content fontSizeSmall BSHARE_POP']")[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, video, cover = self.content_clean(cv, need_video=False)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )


class HqrwSYSpipder(HqrwZJSpipder):
    name = 'hqrw_sy_spider'

    # 环球人物 ==》 首页
    mystart_urls = {
        'http://www.globalpeople.com.cn/': 124,  # 559,  # '首页'
    }
    # http://www.hqrw.com.cn/2018/1112/82215.shtml
    rules = (Rule(LinkExtractor(allow=r'hqrw.com.cn/.*?\d+.s?htm', deny=('video', 'audio'),
                                restrict_xpaths='//div[@class="flexslider banner small"]'),
                  callback='parse_item', follow=False),
             )
    custom_settings = {
        # 和父spider一起去重
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % HqrwZJSpipder.name,
    }