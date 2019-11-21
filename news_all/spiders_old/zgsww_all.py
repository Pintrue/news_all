# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Zgsww_allSpider(NewsRCSpider):
    """中国税务网"""
    name = 'zgsww'
    dd = deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES'))
    dd['news_all.middlewares.ProxyRdMiddleware'] = 100
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': dd,
        'RETRY_TIMES': 5,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1
    }
    mystart_urls = {
        'http://www.ctax.org.cn/lb/csyw/': 1301632,  # 中国税务网-首页-税务要闻-页面右侧两个板块
    }

    rules = (
        #http://www.ctax.org.cn/csyw/201906/t20190615_1088051.shtml
        Rule(LinkExtractor(allow=(r'ctax.org.cn.*?/%s/t\d{8}_\d+.shtml' % datetime.today().strftime('%Y%m'),),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='zhw']/h2/text()").extract_first()
            source = xp("//div[@class='date']")[0]
            content_div = xp("//div[@class='TRS_Editor']")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name =xp('//div[@class="date"]/text()').extract_first('')
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
