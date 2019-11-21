# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Haikouwb_allSpider(NewsRCSpider):
    """海口晚报"""
    name = 'hkwb'
    mystart_urls = {
        'http://www.hkwb.net/news/haikou_zj.html': 1301184,  # 海口晚报-原创-左侧列表
        # 'http://www.hkwb.net/zhuanti/node_25600.htm': 1301183,  # 海口晚报-城市更新-底部列表采集
    }
    rules = (
        #http://www.hkwb.net/news/content/2019-06/20/content_3737948.htm
        Rule(LinkExtractor(allow=(r'hkwb.net/news/content/%s/\d{2}/content_\d+.htm' % datetime.today().strftime('%Y-%m'), ),
                           ), callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='newsContent_title']/h1/text()").extract_first()
            source = xp("//div[@class='newsContent_Source']")[0]
            content_div = xp("//div[@class='newsContent_Detailed']")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            og = xp("//div[@class='newsContent_Source']/a/text()").extract_first('').split()
            origin_name = og[0].strip() if og else ""
            content, media, _, _ = self.content_clean(content_div,
                                                      kill_xpaths='//img[contains(@src,"/54e1adffdd131e811d0d46.jpg")]')
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
