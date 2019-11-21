# -*- coding: utf-8 -*-
import logging
from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider, NewsCrawlSpider

import time


class CvnewsSpider(NewsRCSpider):
    """商用车新网"""
    name = 'cvnews'
    mystart_urls = {
        'http://www.cvnews.com.cn/portal.php?mod=list&catid=5': 1301042,
        'http://www.cvnews.com.cn/portal.php?mod=list&catid=4': 1301041,
        'http://www.cvnews.com.cn/portal.php?mod=list&catid=3': 1301037,
        'http://www.cvnews.com.cn/portal.php?mod=list&catid=2': 1301036,
        'http://www.cvnews.com.cn/portal.php?mod=list&catid=35': 1301043,
        'http://www.cvnews.com.cn/portal.php?mod=list&catid=18': 1301040,
        'http://www.cvnews.com.cn/portal.php?mod=list&catid=6': 1301038,
        'http://www.cvnews.com.cn/portal.php?mod=list&catid=12': 1301039,
    }
    # http://www.cvnews.com.cn/portal.php?mod=view&mobile=yes&aid=62890&$page=
    # http://www.cvnews.com.cn/portal.php?mod=view&mobile=yes&aid=60228&$page=
    # http://www.cvnews.com.cn/zt/201410-iaa/ 舍弃
    rules = (
        Rule(LinkExtractor(allow=r'cvnews\.com\.cn/.*?\d{5}.*?',
                           deny=('video', 'audio', 'search.php', 'zt'),
                           ),
             callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//title/text()').extract()[0]
            # 2019-4-1 21:55
            pubtime = xp('//p[@class="xg1"]').re('\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}')[0]
            
                
            cv = xp('//td[@id="article_content"]')[0]
            content, media, video, cover = self.content_clean(cv)
            origin_name = xp('//p[@class="xg1"]').re('来自：(\w+)')[0]
        except:
            # return self.parse_item_2(response)
            return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media,
        )
