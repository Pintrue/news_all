# -*- coding: utf-8 -*-

from datetime import datetime
import logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class CnwestAllSpider(NewsRCSpider):
    """西部网"""
    name = 'cnwest_all'

    mystart_urls = {
        'http://news.cnwest.com/node_4139.htm': 1301516,  # 西部网 新闻频道-陕西-时事
        'http://news.cnwest.com/4949.shtml': 1301515,  # 西部网 本网原创
        'http://health.cnwest.com/node_41302.htm': 1301259,  # 西部网-健康生活
        'http://health.cnwest.com/node_63206.htm': 1301260,  # 西部网-养生管家-中部列表采集
        'http://health.cnwest.com/node_41300.htm': 1301261,  # 西部网-医疗动态
        'http://ent.cnwest.com/node_57466.htm': 1301264,  # 西部网-忒别致
        'http://travel.cnwest.com/node_5244.htm': 1301263,  # 西部网-旅游资讯
        'http://auto.cnwest.com/node_33726.htm': 1301267,  # 西部网-汽车资讯
        'http://hct.cnwest.com/node_90549.htm': 1301262,  # 西部网-硬科技
        'http://eat.cnwest.com/node_54991.htm': 1301265,  # 西部网-美食厨房
        'http://eat.cnwest.com/node_56234.htm': 1301266,  # 西部网-美食资讯
        'http://sports.cnwest.com/node_33146.htm': 1301268,  # 西部网-陕西体育

    }

    # start_headers = {
    #     'Host': 'www.dbw.cn',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    # }
    # http://news.cnwest.com/szyw/a/2019/06/24/17850592.html    http://news.cnwest.com/szyw/a/2019/06/24/17850391.html

    rules = (
        Rule(LinkExtractor(allow=r'news.cnwest.com.*?/%s/\d{2}/\d+.htm' % datetime.today().strftime('%Y/%m'),
                           deny='video', ), callback='parse_item',
             follow=False),
    )

    custom_settings = {
        # 'DEPTH_LIMIT': 3,  # 翻页需要设置深度为0 或者 >1
        # 'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//div[@class="layout"][2]/h1/text()').extract()[0]
            cvs = xp('//div[@id="conCon"]') or xp('//div[@class="picBox"]')
            content_div = cvs[0]
            source_div = xp('//div[@class="layout-left"]/p')[0]
            pubtime = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}')[0]
            
                
        except:
            return self.produce_debugitem(response, 'xpath error')
        origin_name = "".join(source_div.re(r'[\u4e00-\u9fa5]+')).replace('时间来源', '').strip()
        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media,
            videos=videos,
        )

