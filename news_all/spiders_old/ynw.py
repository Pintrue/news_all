# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class YnwSpider(NewsRCSpider):
    '''云南网'''
    # DNS lookup failed: no results for hostname lookup: gongyi.yunnan.cn.
    name = 'ynw'
    mystart_urls = {
        'http://society.yunnan.cn/ynkd/': 1301288,  # 云南网-云南看点
        'http://gongyi.yunnan.cn/gyyw/': 1301284,  # 云南网-公益要闻
        'http://society.yunnan.cn/jctp/': 1301287,  # 云南网-图解百态
        'http://minzu.yunnan.cn/xwjj/index.shtml': 1301549,  # 云南网-新闻聚焦
        'http://society.yunnan.cn/nxw/': 1301285,  # 云南网-暖新闻
        'http://society.yunnan.cn/shrd/': 1301286,  # 云南网-社会热点
    }
    rules = (
        # http://society.yunnan.cn/system/2019/06/09/030296548.shtml
        # http://minzu.yunnan.cn/system/2019/06/26/030308945.shtml
        # http://gongyi.yunnan.cn/system/2019/06/27/030309791.shtml
        # http://comment.yunnan.cn/system/2019/07/01/030312924.shtml
        Rule(LinkExtractor(allow=(r'yunnan.cn/system/%s/\d{2}/\d+.s?html' % datetime.today().strftime('%Y/%m'),),
                           deny='http://www.jinbifun.com'),
             callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=(r'yunnan.cn.*?\d+.s?htm',), deny=(r'/201[0-8]', r'/2019/0[1-9]', r'/node_\d+.htm')
                           ), process_request=otherurl_meta,
             follow=False),
    )
    
    custom_settings = {
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    def parse_item(self, response):
        if response.url.startswith('http://www.jinbifun.com/'):
            return
        
        xp = response.xpath
        try:
            title = xp("//span[@id='layer213']/text()").extract_first() or self.get_page_title(response).split('_')[0]
            content_div = xp("//div[@id='layer216']")[0]
            pubtime = xp('//span[@class="xt2 yh fl"]/span[1]/text()')[0].extract()
            origin_name = xp('//span[@class="xt2 yh fl"]/span[2]/text()').extract_first('')
        except Exception as e:
            if xp('//div[@id="imgContent"]'):
                return self.parse_images(response)
            return self.produce_debugitem(response, "xpath error")
        
        content, media, _, _ = self.content_clean(content_div, kill_xpaths=['//img[@src="/002324a0abac1ca029c122.jpg"]',
                                                                            r'//*[contains(text(), "欢迎关注彩云网评")]/parent::p'])
        
        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )
    
    def parse_images(self, response):
        # http://society.yunnan.cn/system/2019/07/01/030313000.shtml
        xp = response.xpath
        try:
            pubtime = xp('//div[@class="layer31"').re(r'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}(?:\:\d{2})?')[0]
            og = xp('//div[@class="layer31"]').re('来源：\w+')
            origin_name = og[0] if og else ""
            title = xp("//span[@id='layer213']/text()").extract_first('') or self.get_page_title(response).split('_')[0]
            content_div = xp('//div[@id="imgContent"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        
        next_a = xp('//div[@id="news_more_page_div_id"]/a[text()="下一页"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')})
        
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
    
    def parse_page(self, response):
        xp = response.xpath
        meta_new = deepcopy(response.meta)
        try:
            content_div = xp('//div[@id="imgContent"]')[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()
        
        next_a = xp('//div[@id="news_more_page_div_id"]/a[text()="下一页"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
        
        content, media, videos, video_cover = self.content_clean(meta_new['content'])
        
        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),
            
            content=content,
            media=media
        )
