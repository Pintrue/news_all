# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class YdylpeopleSpider(NewsRCSpider):
    '''一带一路全媒体平台--人民网'''
    name = 'ydylpeople'
    mystart_urls = {
        "http://ydyl.people.com.cn/GB/411941/412084/index.html": 7598,
        "http://ydyl.people.com.cn/GB/411937/index.html": 7599,
        "http://ydyl.people.com.cn/GB/413605/index.html": 7600,
        "http://ydyl.people.com.cn/GB/412092/412093/index.html": 7601,
    }
    rules = (
        # http://ydyl.people.com.cn/n1/2019/0618/c411837-31165595.html
        Rule(LinkExtractor(allow=(r'ydyl.people.com.cn/n1/\d{4}/\d{4}/c\d+-\d+\.html',),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='clearfix w1000_320 text_title']/h1/text()").extract_first()
            content_div = xp("//div[@id='rwb_zw']")[0]
            pubtime = xp("//div[@class='box01']/div[@class='fl']/text()").extract_first().replace('\xa0\xa0来源：','').strip()
            origin_name = xp("//div[@class='box01']/div[@class='fl']/a/text()").extract_first()
        except:
            return self.produce_debugitem(response, "xpath error")
        # 过滤视频


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
