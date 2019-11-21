# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class huanqiushipinSpider(NewsRCSpider):
    """环球视频"""
    name = 'huanqiushipin'
    mystart_urls = {
        'http://v.huanqiu.com/observation/': 3774,
        'http://mil.huanqiu.com/milmovie/': 3775,
        'http://v.huanqiu.com/guoji/': 3776,
        'http://v.huanqiu.com/shehui/': 3777,
        'http://v.huanqiu.com/jiong/': 3778,
        'http://v.huanqiu.com/luoli/': 3779,
        'http://v.huanqiu.com/yule/': 3780,
        'http://v.huanqiu.com/douba/': 3781,
        'http://v.huanqiu.com/saidJapan/': 3782,
        'http://v.huanqiu.com/celebrity/': 3783,
        'http://v.huanqiu.com/VisitJapan/': 3784,
        'http://v.huanqiu.com/Global-500/': 3785,
        'http://v.huanqiu.com/fzzg/': 3786,
        'http://v.huanqiu.com/Triphibious/': 3787,
        'http://tech.huanqiu.com/video/': 3788,
    }
    
    rules = (
        Rule(LinkExtractor(allow=(r'v.huanqiu.com/.*?/%s/\d+.html') % datetime.today().strftime('%Y-%m'), deny=[]),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'mil.huanqiu.com/.*?/%s/\d+.html') % datetime.today().strftime('%Y-%m'), deny=[]),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'tech.huanqiu.com/.*?/%s/\d+.html') % datetime.today().strftime('%Y-%m'),
                           deny=r'666n.com/html'),
             callback='parse_item', follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//div[@class="l_a"]/h1/text()').extract_first('') or self.get_page_title(response).split('_')[0]
            pubtime = xp('//span[@class="la_t_a"]/text()').extract()[0]
            origin_name = xp('//span[@class="la_t_b"]/text()').extract_first('')
            cv = xp('//div[@class="la_con"]').extract()[0]
            content, media, videos, _ = self.content_clean(cv, need_video=True)
        except:
            return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,  # must
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media,
            videos=videos,
        )
