# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider, otherurl_meta
from news_all.tools.time_translater import Pubtime


class HangZhouAllSpider(NewsRCSpider):
    """杭州网"""
    name = 'hangzhou_all'
    
    mystart_urls = {
        
        'http://it.hangzhou.com.cn/jrjd/yjnews/': 1301422,  # 杭州网-业界新闻-列表
        'http://auto.hangzhou.com.cn/dghq/node_71978.htm': 1301425,  # 杭州网-业界资讯
        'http://health.hangzhou.com.cn/node_141997.htm': 1301418,  # 杭州网-保健
        'http://health.hangzhou.com.cn/regimen/index.htm': 1301421,  # 杭州网-养生列表
        'http://hznews.hangzhou.com.cn/chengshi/index.htm': 1301426,  # 杭州网-城市新闻列表
        'http://auto.hangzhou.com.cn/zxcw/node_71956.htm': 1301424,  # 杭州网-新车资讯列表
        'http://travel.hangzhou.com.cn/lyzx/index.htm': 1301423,  # 杭州网-旅游资讯-左侧列表
        'http://hznews.hangzhou.com.cn/xinzheng/yaolan/node_15890.htm': 1301428,  # 杭州网-时政-列表
        'http://health.hangzhou.com.cn/expose/index.htm': 1301419,  # 杭州网-曝光
        'http://health.hangzhou.com.cn/hot/index.htm': 1301420,  # 杭州网-热点关注列表和右侧热门推荐
        'http://money.hangzhou.com.cn/management/index.htm': 1301417,  # 杭州网-理财推荐-左侧列表
        'http://hznews.hangzhou.com.cn/jingji/index.htm': 1301416,  # 杭州网-经济新闻列表
        'http://money.hangzhou.com.cn/news/index.htm': 1301415,  # 杭州网-财经新闻
    }
    
    # https://it.hangzhou.com.cn/jrjd/yjnews/content/2019-06/21/content_7214597.htm
    # https://health.hangzhou.com.cn/content/2019-07/23/content_7231132.htm
    rules = (
        Rule(LinkExtractor(
            allow=r'hangzhou.com.cn.*?/content/%s/\d{2}/content_\d+.htm' % datetime.today().strftime('%Y-%m'),
            deny='video', ), callback='parse_item',
            follow=False),
        # https://it.hangzhou.com.cn/content/content_5458376.htm  图集
        # https://it.hangzhou.com.cn/content/content_5310978.htm
        Rule(LinkExtractor(allow=r'hangzhou.com.cn/content/content_\d+.htm', ), callback='parse_item', follow=False),
        Rule(LinkExtractor(
            allow=r'hangzhou.com.cn.*?\d+.htm',
            deny=(
                r'/201[0-8]', r'content/2019-0[1-8]', 'video', r'/index_\d+.htm', r'/node_\d+', r'xiaofei.hangzhou.com',
                r'bbs.hangzhou.com'), ),
            process_request=otherurl_meta,
            follow=False),
    )
    
    custom_settings = {
        'DEPTH_LIMIT': 3,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    def parse_item(self, response):
        # https://sports.dbw.cn/system/2019/06/17/058217425.shtml
        
        meta_new = deepcopy(response.meta)
        xp = response.xpath
        try:
            title = meta_new.get("link_text")
            if not title:
                title0 = self.get_page_title(response).split('_')[0]
                title = title0 if title0.find('-') < 0 else title0.split('-')[0]
            
            cvs = xp('//div[@class="fontsz14"]') or xp('//td[@class="wz14"]') or xp(
                '//td[@class="hzwRP_lname06"]') or xp('//div[@class="zhengwen"]') or xp('//td[@class="xwzx_wname02"]')
            if cvs:
                content_div = cvs[0]
            else:
                content_div = xp('//td[@class="xz_bcolor01"]/p')
                content_div[0]  # 故意拦截[] 捕获异常
            
            ps = xp('//div[@class="le_12black"]/text()') or xp('//div[@class="tit1"]') or xp(
                '//div[@class="le_12black"]/text()') or xp(
                '//table[@class="wz"]/tbody/tr[1]/td/table/tbody/tr[6]/td')
            pss = ps[0].extract() if ps else xp('/html/head/meta[@name="publishdate"]/@content').extract_first('')
            pubtime = Pubtime(pss)
            origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first('')
        except Exception as e:
            return self.produce_debugitem(response, 'xpath error')
        
        page_all_a = xp('//ul[@class="pages"]/li[@class="page-all"]/a')
        if page_all_a:
            return response.follow(page_all_a[0], callback=self.parse_page_all,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         })

        content, media, videos, video_cover = self.content_clean(content_div)
        
        return self.produce_item(response=response,
                                 title=title,
                                 origin_name=origin_name,
                                 pubtime=pubtime,
                                 content=content,
                                 media=media,
                                 )
    
    def parse_page_all(self, response):
        xp = response.xpath
        try:
            cvs = xp('//div[@class="fontsz14"]') or xp('//td[@class="wz14"]') or xp(
                '//td[@class="hzwRP_lname06"]') or xp('//div[@class="zhengwen"]') or xp('//td[@class="xwzx_wname02"]')

            if cvs:
                content_div = cvs[0]
            else:
                content_div = xp('//td[@class="xz_bcolor01"]/p')
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, 'xpath error')

        return self.produce_item(response=response,
                                 title=response.meta.get('title'),
                                 pubtime=response.meta.get('pubtime'),
                                 origin_name=response.meta.get('origin_name'),
                                 content=content,
                                 media=media,
                                 )
