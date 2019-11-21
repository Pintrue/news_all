# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class msweeklySpider(NewsRCSpider):
    """民生周刊（民生网）"""
    name = 'msweekly'
    mystart_urls = {
        'http://www.msweekly.com/category.html?catid=70': 565,  # 时政
        'http://www.msweekly.com/category.html?catid=166': 566,  # 财经
        'http://www.msweekly.com/category.html?catid=153': 567,  # 评论
        'http://www.msweekly.com/category.html?catid=82': 568,  #环保
        # spiders_all 新增的
        'http://www.msweekly.com/category.html?catid=103': 6276,  # 旅游-民生网-人民日报社《民生周刊》杂志官网
        'http://www.msweekly.com/category.html?catid=221': 6270,  # 文化教育强国论坛-民生网-人民日报社《民生周刊》杂志官网
        'http://www.msweekly.com/category.html?catid=156': 6272,  # 扶贫-民生网-人民日报社《民生周刊》杂志官网
        'http://www.msweekly.com/category.html?catid=94': 6273,  # 公益-民生网-人民日报社《民生周刊》杂志官网
        'http://www.msweekly.com/category.html?catid=83': 6278,  # 健康-民生网-人民日报社《民生周刊》杂志官网
        'http://www.msweekly.com/category.html?catid=183': 6283,  # 袭古创今-民生网-人民日报社《民生周刊》杂志官网
        
        # 老爬虫的
        'http://www.msweekly.com/category.html?catid=154': 1301026,  # 民生周刊-人民旅游
    }
    #http://www.msweekly.com/show.html?id=107658
    rules = (Rule(LinkExtractor(allow=(r'msweekly.com/.*?\?id=\d{1,}',), ), callback='parse_item', follow=False),)

    def parse_item(self, response):
        try:
            pubtime = response.xpath('//p[@class="text"]/span[2]/text()').extract_first("")
            title = response.xpath('//h1/text()')[0].extract().strip()
            content_div = response.xpath('//div[@class="con_left_con"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        head_div = response.xpath('//p[@class="text"]/span[1]')[0]
        if head_div is None:
            head_div = response.xpath('//div[@class="show_text"]/div/span[2]')[0]
        source_re = head_div.re('来源：(\w{2,})')
        origin_name = source_re[0] if source_re else ''
        content, media, videos, cover = self.content_clean(content_div, kill_xpaths=[])

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )