# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider
import re


class TswSpider(NewsRCSpider):
    """天山网"""
    name = 'tsw'
    mystart_urls = {
        'http://news.ts.cn/tp/index.shtml': 1301253,  # 天山网 新闻中心-图片新闻-左侧列表
    }
    rules = (
        #http://news.ts.cn/system/2019/06/03/035719250.shtml
        Rule(LinkExtractor(allow=(r'news.ts.cn.*?/%s/\d{2}/\d+.shtml' % datetime.today().strftime('%Y/%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='active-title']/text()").extract_first()
            source = xp("//p[@class='active-info2']")[0]
            content_div = xp("//div[@class='hy-active']")[0]

            pubtime = source.re(r'\d{2,4}年\d{1,2}月\d{1,2}日')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            origin_name_div =xp('//p[@class="active-info2"]/text()').extract_first('')
            origin_name = re.findall(".*来源：(.*).*", origin_name_div)[0]
        except:
            return self.produce_debugitem(response, "xpath error")

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
