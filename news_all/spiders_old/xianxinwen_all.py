# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class XianxinwenSpider(NewsRCSpider):
    """西安新闻网"""
    name = 'xian_news'
    mystart_urls = {
        'http://news.xiancn.com/node_2049.htm': 1301513,  # 西安新闻网 体育健身
        'http://news.xiancn.com/node_2048.htm': 1301514,  # 西安新闻网 文化娱乐
        'http://news.xiancn.com/node_10490.htm': 1301509,  # 西安新闻网 本地新闻-左侧列表采集
        'http://news.xiancn.com/node_2046.htm': 1301511,  # 西安新闻网 科技教育-左侧列表
        'http://news.xiancn.com/node_10299.htm': 1301510,  # 西安新闻网 速新闻-左侧列表

    }
    rules = (
        #http://news.xiancn.com/content/2019-06/24/content_3468298.htm
        #http://news.xiancn.com/content/2019-06/24/content_3468270.htm
        Rule(LinkExtractor(allow=(r'news.xiancn.com/content/%s/\d{2}/content_\d+.htm' % datetime.today().strftime('%Y-%m'), ),
                           ), callback='parse_item',
             follow=False),
        Rule(LinkExtractor(
            allow=(r'xiancn.com.*?\d+.htm',), deny=(r'/201[0-8]', r'/2019-0[1-9]', r'xiancn.com/node_\d+')
            ), process_request=otherurl_meta,
             follow=False),
    )
    
    custom_settings = {
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='biaoti']/text()").extract_first()
            content_div = xp("//div[@class|@id='content']")[0]
            pubtime = xp("//div[@class='mess']").re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{2}:\d{2}')[0]
            og = xp("//div[@class='mess']").re('来源(?:|：)\w+')  # '2019-07-01 13:14　　来源：中国新闻网　　　 　/ 　编辑：雷莹'
            origin_name = og[0] if og else ""
        except:
            return self.parse_item_2(response)
        
        next_a = xp('//div[@id="displaypagenum"]/center/a[text()="下一页"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')})
        # 懒加载图片"src" : "http://img.news18a.com/image/auto/170410/lazyload660.jpg"
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_page(self, response):
        xp = response.xpath
        meta_new = deepcopy(response.meta)
        
        try:
            content_div = xp("//div[@class|@id='content']")[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()
        
        next_a = xp('//div[@id="displaypagenum"]/center/a[text()="下一页"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
        
        content, media, videos, video_cover = self.content_clean(meta_new['content'],
                                                                 kill_xpaths=['//div[@id="displaypagenum"]',
                                                                              '//div[@class="text"]'])
        
        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),
            content=content,
            media=media
        )
    
    # http://news.xiancn.com/content/2019-06/23/content_3468106.htm
    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='biaoti']/text()").extract_first()
            content_div = xp("//div[@id='content']")[0]
            pubtime = xp("//div[@class='mess']").re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{2}:\d{2}')[0]
            og = xp("//div[@class='mess']").re('来源(?:|：)\w+')  # 来源:：
            origin_name = og[0] if og else ""
        except:
            return self.produce_debugitem(response, "xpath error")

        next_a = xp('//div[@id="displaypagenum"]/center/a[text()="下一页"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         })
        
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
