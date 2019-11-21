# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class GcdxwSpider(NewsRCSpider):
    '''共产党新闻网'''
    name = 'gcdxw'
    mystart_urls = {
        'http://cpc.people.com.cn/GB/64093/64094/': 1302174,  # 共产党新闻网-高层动态
    }
    rules = (
        # http://cpc.people.com.cn/n1/2019/0611/c64094-31130216.html
        Rule(LinkExtractor(allow=(r'cpc.people.com.cn/n1/%s/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m%d'),),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//div[@class="text_c"]/h1/text()').extract_first()
            content_div = xp('//div[@class="show_text"]')[0]
            pubtime = xp('//p[@class="sou"]/text()').re(r'\d{4}年\d{2}月\d{2}日\d{2}:\d{2}')[0]
            origin_name = xp('//p[@class="sou"]/a/text()').extract_first()
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
