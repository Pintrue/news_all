# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.tools.others import to_list
from news_all.spider_models import NewsRCSpider


class GmwSpider(NewsRCSpider):
    """光明网"""
    name = 'gmw'
    mystart_urls = {
        'http://news.gmw.cn/node_4108.htm': 175,  # '光明导读',
        'http://legal.gmw.cn/': 176,  # '法治',
        'http://world.gmw.cn/': 177,  # '国际',
        # 'http://world.gmw.cn/node_24178.htm': 0,  # '测试图集',
    }
    
    custom_settings = {
        'DEPTH_LIMIT': 0,
        # 禁止重定向
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    # http://politics.gmw.cn/2019-01/20/content_32379481.htm
    rules = (Rule(LinkExtractor(
        allow=(r'(?:news|legal|world).gmw.cn/%s/\d{2}/content_\d+\.htm' % datetime.today().strftime('%Y-%m'),)),
        callback='parse_item', follow=False),
    )
    
    def parse_item(self, response):
        if "页面没有找到" in self.get_page_title(response):
            return self.produce_debugitem(response, '网页报错: 页面没有找到')
        
        xp = response.xpath
        try:
            # news_div = response.xpath('.//div[@class="contentWrapper"]/div[@class="contentLeft"]')[0]
            source_div = xp('//div[@id="contentMsg" or @class="text-right ysp_msg"]')[0]
            content_div = xp('//div[@id="contentMain"]')[0]
            pubtime = source_div.xpath('./span[@id="pubTime"]/text()')[0].extract().strip()
        except:
            return self.parse_item_2(response)

        origin_name = source_div.xpath('./span[@id="source"]/a/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean_gmw(content_div)
        
        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('_')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_2(self, response):
        xp = response.xpath
        try:
            head_div = xp('.//div[@class="m-title-box"]')[0]
            source_div = head_div.xpath('./div[@class="m-con-info"]')[0]
            pubtime = source_div.xpath('./span[@class="m-con-time"]/text()').extract()[0].strip()
            content_div = xp('.//div[@id="articleBox"]/div[@id="article_inbox"]')[0]
        except:
            return self.parse_images(response)

        # title = ''.join(i.strip() for i in head_div.xpath('.//h1[@class="u-title"]/text()').extract())
        origin_name = source_div.xpath('./span[@class="m-con-source"]/a/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean_gmw(content_div)
        
        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('_')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_images(self, response):
        # http://world.gmw.cn/2019-01/04/content_32298832.htm
        # http://world.gmw.cn/2019-02/11/content_32481254.htm
        xp = response.xpath
        try:
            # title = xp('//h1[@class="u-title"]/text()').extract()[0].strip()
            origin_name = xp('//div[@class="g-tips"]/span/a/text()').extract()[0]
            content_div = xp('//div[@class="h-contentMain"]')[0]
            pubtime = xp('//span[@class="u-time"]/text()').extract_first('').strip()
        except:
            return self.parse_item_4(response)
            
        content, media, videos, video_cover = self.content_clean_gmw(content_div)
        
        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('_')[0],
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media
        )

    def parse_item_4(self, response):
        xp = response.xpath
        try:
            pubtime = xp('//span[@class="m-con-time"]/text()')[0].extract().strip()
            title = xp('//h1[@class="u-title"]/text()').extract_first('').strip()
            og = xp('//*[@class="m-con-source"]/a/text()').extract_first('') or xp(
                '//*[@class="m-con-source"]/text()').extract_first('')
            origin_name = og.replace("来源：", "").strip()
            content_div = xp('//div[@class="u-mainText"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        next_a = xp('//div[@id="displaypagenum"]//a[text()="下一页"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'origin_name': origin_name,
                                         'content': content_div.extract(), 'title': title,
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         })
        content, media, videos, video_cover = self.content_clean_gmw(content_div)

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('_')[0],
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media
        )
    
    def parse_page(self, response):
        meta_new = deepcopy(response.meta)
        xp = response.xpath
        try:
            content_div = xp('//div[@class="u-mainText"]')[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        
        meta_new['content'] += content_div.extract()
        
        next_a = xp('//div[@id="displaypagenum"]//a[text()="下一页"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
        
        content, media, videos, video_cover = self.content_clean_gmw(meta_new['content'],
                                                                 kill_xpaths=r'//div[@class="m-zbTool liability"]')
        
        return self.produce_item(
            response=response,
            title=meta_new.get('title') or re.sub(r'(.*?)\(\d+\)$', r'\1', self.get_page_title(response).split('_')[0]),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),

            content=content,
            media=media
        )
    
    def content_clean_gmw(self, content_div, need_video=False, kill_xpaths=None):  #
        kill_xpaths = to_list(kill_xpaths) + [r'//img[@src="https://img.gmw.cn/pic/content_logo.png"]',
                                              r'//div[@class="pageNum"]',
                                              r'//div[@id="displaypagenum"]'
                                              ]
        return self.content_clean(content_div, need_video=need_video, kill_xpaths=kill_xpaths)


class GmwHomeSpider(GmwSpider):
    """光明网"""
    name = 'gmw_home'
    # allowed_domains = ['gmw.cn']
    mystart_urls = {
        'http://news.gmw.cn/': 174,  # '新闻',
    }
    # http://politics.gmw.cn/2019-01/20/content_32379481.htm
    rules = (Rule(LinkExtractor(
        allow=(r'(?:politics|world).gmw.cn/%s/\d{2}/content_\d+\.htm' % datetime.today().strftime('%Y-%m'),)),
                  callback='parse_item', follow=False),)
    
    custom_settings = deepcopy(GmwSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % GmwSpider.name,}
    )