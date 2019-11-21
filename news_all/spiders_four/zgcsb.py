#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.conf import settings
from copy import deepcopy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider

this_year = datetime.now().year


class ZgcsbSpider(NewsRCSpider):
    """中国城市网"""
    name = 'zgcsb'

    mystart_urls = {
        # 'http://www.zgcsb.org.cn/': [588, 589],  # 588:轮播图+右侧列表, 589:特别推荐
        'http://www.zgcsb.org.cn/': 588,
        # 老爬虫的
        'http://www.zgcsb.org.cn/yaowen/csyw/': 1301056,  # 中国城市报-城市要闻
        'http://www.zgcsb.org.cn/yaowen/szyw/': 1301054,  # 中国城市报-时政要闻-左侧列表
        'http://www.zgcsb.org.cn/yaowen/xxtp/': 1301052,  # 中国城市报-要闻-新闻图片
        'http://www.zgcsb.org.cn/yaowen/jryw/': 1301053,  # 中国城市报-要闻精选
    }

    from scrapy.conf import settings
    from copy import deepcopy
    custom_settings = {
        'DEPTH_LIMIT': 0,  # 若翻页则需要设置深度为0
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))  # 禁止重定向
    }
    rules = (
        Rule(LinkExtractor(allow=(r'zgcsb.com/.*?/%s\-\d{2}\-\d{2}/\d{4,}\.html' % datetime.today().year,),
                           restrict_xpaths=r'//div[@class="banner"]/ul'),
             callback='parse_item',
             follow=False),  # , process_request=identity_shouye
        Rule(LinkExtractor(allow=(r'zgcsb.com/.*?/%s\-\d{2}\-\d{2}/\d{4,}\.html' % datetime.today().year, ),
                           restrict_xpaths=r'//div[@class="focusList fr"]'), callback='parse_item',
             follow=False),  # , process_request=identity_tuijian
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            source_div = xp('.//div[@id="artical_sth"]')[0]
            pubtime = source_div.xpath('.//*[@itemprop="datePublished"]/text()').extract_first('').strip()
            content_div = xp(".//div[@id='main_content']")[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        title1 = response.request.meta.get('link_text', '').strip()
        title = response.xpath('.//h1[@id="artical_topic"]/text()').extract_first('').strip() or title1

        origin_name = source_div.xpath('.//span[@class="ss03"]//text()').extract_first('')

        next_a = xp('//*[@class="pageLink"]//a[contains(text(), "下一页")]')
        if next_a:
            content_div = content_div.xpath('.//*[@class="pageLink"]/preceding-sibling::*')
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         })

        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )

    def parse_page(self, response):
        xp = response.xpath
        meta_new = deepcopy(response.meta)

        try:
            content_div = xp(".//div[@id='main_content']")[0]
            content_div = content_div.xpath('.//*[@class="pageLink"]/preceding-sibling::*')
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()

        # todo 代码简化
        next_a = xp('//*[@class="pageLink"]//a[contains(text(), "下一页")]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
        """
        # 或者 
        next_url = xp('//*[@class="pageLink"]//a[contains(text(), "下一页")]/@href').extract_first()
        if next_url:
            yield response.follow(next_url, callback=self.parse_page)
        """
        content, media, videos, video_cover = self.content_clean(meta_new['content'])

        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),
            content=content,
            media=media
        )


class ZgcsbHotsSpider(ZgcsbSpider):
    """中国城市网 分栏"""
    name = 'zgcsb_hots'

    mystart_urls = {
        'http://www.zgcsb.org.cn/yaowen/': 590,  # 要闻
        'http://www.zgcsb.org.cn/2-nav/csgclm/': 591,  # 城市
        'http://www.zgcsb.org.cn/sd/': 592,  # 深度

        'http://www.zgcsb.org.cn/benbao/': 594,  # 本报原创
        'http://www.zgcsb.org.cn/tupian/': 595,  # 智慧城市
        'http://zh.zgcsb.org.cn/tupian/': 596,  # 经济

        'http://zh.zgcsb.org.cn/keji/': 598,  # 科技
    }

    # http://www.zgcsb.com/yaowen/szyw/2019-03-06/89374.html
    rules = (
        Rule(LinkExtractor(allow=(r'zgcsb\.com/.*?\d+\.html',), restrict_xpaths='//div[@class="page01L_list"]'),
             callback='parse_item',
             follow=False),)
    custom_settings = {
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % ZgcsbSpider.name,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    

class ZgcsbSpSpider(ZgcsbSpider):
    """中国城市网 社评"""
    name = 'zgcsb_sp'

    mystart_urls = {
        'http://www.zgcsb.com/sd/sp/': 593,  # 社评
    }

    # http://www.zgcsb.com/sd/sp/2019-02-28/88711.html
    rules = (
        Rule(LinkExtractor(allow=(r'zgcsb.com/sd/sp/%s-\d{2}-\d{2}/\d+\.html' % this_year,),
                           restrict_xpaths="//div[@class='col_L']//h2"), callback='parse_item',
             follow=False),)
    custom_settings = {
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % ZgcsbSpider.name,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    

class ZgcsbQySpider(ZgcsbSpider):
    """中国城市网 环保"""
    name = 'zgcsb_qiye'

    mystart_urls = {
        'http://www.zgcsb.org.cn/qiye/': 597,  # 环保
    }

    # http://www.zgcsb.com/qiye/csmq/2019-02-18/87656.html
    rules = (
        Rule(LinkExtractor(allow=(r'zgcsb.com/qiye/[a-z]+/%s-\d{2}-\d{2}/\d+\.html' % this_year,)
                           ), callback='parse_item', follow=False),
    )
    custom_settings = {
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % ZgcsbSpider.name,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }