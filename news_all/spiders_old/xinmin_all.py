# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider
from news_all.tools.others import to_list


class XinminAllSpider(NewsRCSpider):
    """新民网"""
    name = 'xinmin_all'
    
    mystart_urls = {
        'http://ish.xinmin.cn/xnjx/': 2713,  # 新民网-侬好上海-小侬精选
        'http://newsxmwb.xinmin.cn/shenti/pc/': 2704,  # 新民网-健康-健康列表
        'http://newsxmwb.xinmin.cn/junshi/pc/': 2706,  # 新民网-军事列表
        'http://shanghai.xinmin.cn/latest/': 98118,  # 新民网-左下列表
        'http://auto.xinmin.cn/xinche/': 2709,  # 新民网-汽车-新车-列表
        'http://auto.xinmin.cn/cheshi/': 2708,  # 新民网-汽车-车市
        'http://newsxmwb.xinmin.cn/world/pc/': 2703,  # 新民网-环球-环球列表
        'http://shanghai.xinmin.cn/xmsq/': 2711,  # 新民网-社会
        'http://newsxmwb.xinmin.cn/kejiao/pc/': 2717,  # 新民网-科教-教育列表
        'http://newsxmwb.xinmin.cn/caijing/pc/': 2714,  # 新民网-财经
        
    }

    # http://ish.xinmin.cn/xnjx/2019/06/19/31546261.html    http://newsxmwb.xinmin.cn/shenti/2019/06/20/31546788.html
    rules = (
        Rule(LinkExtractor(allow=r'xinmin.cn/.*?/%s/.*?/\d+.html' % datetime.today().strftime('%Y'),
                           deny='video', ), callback='parse_item',
             follow=False),
    )
    
    custom_settings = {
        # 'DEPTH_LIMIT': 3,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    def parse_item(self, response):
        # https://sports.dbw.cn/system/2019/06/17/058217425.shtml
        xp = response.xpath
        try:
            title = xp('//h1').extract()[0]
            content_div = xp('//div[@class="a_content"]')[0]
            source_div = xp('//div[@class="info"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
            origin_name = source_div.xpath('./span[1]/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.parse_item2(response)

        return self.produce_item(response=response,  # 一定要写response=response, 不能是response
                                 title=title,
                                 pubtime=pubtime,
                                 origin_name=origin_name,
                                 content=content,
                                 media=media,
                                 )
    
    def parse_item2(self, response):
        # https://sports.dbw.cn/system/2019/06/17/058217425.shtml
        xp = response.xpath
        try:
            title = xp('//h3[@class="content_title"]').extract()[0]
            content_div = xp('//div[@id="MP_article"]')[0]
            source_div = xp('//div[@class="content_info"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
            origin_name = source_div.xpath('./span[@class="page_from"]/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div)
        except :
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(response=response,  # 一定要写response=response, 不能是response
                                 title=title,
                                 pubtime=pubtime,
                                 origin_name=origin_name,
                                 content=content,
                                 
                                 media=media,
                                 )
    
    def content_clean(self, content_div, need_video=False, kill_xpaths=None):
        # 都过滤
        kill_xpaths = to_list(kill_xpaths) + ['//*[contains(text(), "扫一扫关注微信公众号")]',
                                              '//img[contains(@src,"http://image.xinmin.cn")]',
                                              '//div[@class="copyright"]', '//*[contains(text(),"未经授权不得转载")]/parent::*']
        return super(XinminAllSpider, self).content_clean(content_div, need_video=need_video, kill_xpaths=kill_xpaths)