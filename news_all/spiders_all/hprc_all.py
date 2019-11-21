# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class HprcAllSpider(NewsRCSpider):
    """中华人民共和国国史网"""
    name = 'hprc_all'
    mystart_urls = {
        'http://www.hprc.org.cn/gsgl/zyxw/': 2028,
        'http://www.hprc.org.cn/leidaxinxi/': 2029
    }

    # http://www.hprc.org.cn/gsgl/zyxw/201904/t20190416_4864730.html    http://www.hprc.org.cn/gsgl/zyxw/201904/t20190416_4864737.html

    rules = (
        Rule(LinkExtractor(allow=(r'hprc.org.cn/.*?/%s.*?\d+.html'%datetime.today().year), ),
                           callback='parse_item', follow=False),
    )

    # http://www.hprc.org.cn/gsgl/zyxw/201904/t20190416_4864737.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            source_div = xp('.//td[@class="huang12_h"]')[0]
            time_re = source_div.re(r'\d{2,4}\/\d{1,2}\/\d{1,2}')
            if len(time_re):
                pubtime = time_re[0]
            else:
                time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}')
                pubtime = time_re[0]
            content_div = xp('.//div[@class="TRS_Editor"]')[0]
            title = xp('.//span[@class="huang16c"]/text()')[0].extract()
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media
        )