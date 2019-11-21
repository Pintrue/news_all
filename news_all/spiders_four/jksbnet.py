# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class JianKangSBSpider(NewsRCSpider):
    """健康时报_第四批"""
    name = 'jksbnet'
    mystart_urls = {
        'http://www.jksb.com.cn/html/news/': 518,  # 首页
        'http://www.jksb.com.cn/html/life/': 524,  # 首页
        'http://www.jksb.com.cn/html/diseases/': 531,  # 首页
        'http://www.jksb.com.cn/html/supervision/': 536,  # 首页
    }
    #http://www.jksb.com.cn/html/news/policy/2019/0228/134013.html
    rules = (Rule(LinkExtractor(allow=(r'jksb.com.cn/.*?\d+.html',
                                       ), deny=(r'jksb.com.cn/html/life/baby.*?\d+.html',
                                                r'jksb.com.cn/html/news/policy.*?\d+.html',
                                                r'jksb.com.cn/html/news/industry.*?\d+.html',
                                                r'jksb.com.cn/html/news/academic.*?\d+.html',
                                                r'jksb.com.cn/html/news/knowledge.*?\d+.html',) ), callback='parse_item', follow=False),)

    def parse_item(self, response):
        try:
            title = response.xpath('//h1/text()')[0].extract().strip()
            content_div = response.xpath('//div[@class="content"]')[0]
            pubtime = response.xpath('//div[@class="info"]/span[1]/text()').extract_first("")
        except:
            return self.produce_debugitem(response, "xpath error")

        head_div = response.xpath('//div[@class="info"]/span[2]')[0]
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


class JianKangSBBabySpider(JianKangSBSpider):
    """健康时报_婴儿"""
    name = 'jksbnetbaby'
    mystart_urls = {
        'http://www.jksb.com.cn/html/life/': 121,  # 529 # 首页

    }
    # http://www.jksb.com.cn/html/life/baby/2019/0303/134081.html
    rules = (Rule(LinkExtractor(allow=(r'jksb.com.cn/html/life/baby.*?\d+.html',
                                       ) ), callback='parse_item', follow=False),)

    custom_settings = {
        # 和父spider一起去重
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % JianKangSBSpider.name,
    }
