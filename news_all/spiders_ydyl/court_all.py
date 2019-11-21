# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Court_allSpider(NewsRCSpider):
    """中华人民共和国最高人民法院"""
    name = 'court'
    mystart_urls = {
        'http://www.court.gov.cn/xinshidai-gengduo-762.html': 7646,  # 中华人们共和国最高人民法院
        'http://www.court.gov.cn/zixun-gengduo-23.html': 7647,  # 中华人们共和国最高人民法院
    }
    rules = (
        # http://www.court.gov.cn/zixun-xiangqing-166472.html
        # http://www.court.gov.cn/xinshidai-xiangqing-166452.html
        
        Rule(LinkExtractor(allow=(r'court.gov.cn/\w+-\w+-\d{6}.html'),
                           ), callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title1 = xp('.//div[@class="title"]/p[1]/text()').extract_first('').strip()
            sub_title = xp('.//div[@class="title"]/p[2]/text()').extract_first('').strip()
            title1 = join_titles(title1, sub_title)
            title_total = xp("//div[@class='title']/text()").extract()
            title2 = ''
            for i in range(len(title_total)):
                title2 = title2 + title_total[i]
            print(title2)
            
            title = title1 or title2
            # source = xp("//span[@class='detail-span']")[0]
            content_div = xp("//div[@id='zoom']")[0]
            pubtime = xp("//li[@class='fl'][2]").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//li[@class='fl'][1]/text()").extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )


def join_titles(title1, sub_title):
    if sub_title:
        if sub_title.startswith("——"):
            title1 += sub_title
        else:
            title1 += "——" + sub_title
    return title1
