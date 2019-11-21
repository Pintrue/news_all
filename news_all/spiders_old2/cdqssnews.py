# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class CdqssnewsSpider(NewsRCSpider):
    '''成都全搜索新闻网'''
    name = 'cdqssnews'
    mystart_urls = {
        'http://ly.chengdu.cn/lypd/lyzx/': 1301347,  # 成都全搜索新闻网 首页-旅游资讯列表
        'http://auto.chengdu.cn/qcpd/xwzx/': 1301136,  # 成都全搜索新闻网-首页-汽车频道-左侧列表
        'http://fb.chengdu.cn/mspd/mszx/': 1301135,  # 成都全搜索新闻网-首页-美食资讯-左侧列表
    }
    rules = (
        # http://ly.chengdu.cn/2019/0521/2051006.shtml
        # http://auto.chengdu.cn/2019/0624/2056848.shtml
        # http://fb.chengdu.cn/2019/0618/2055738.shtml
        Rule(LinkExtractor(allow=(r'chengdu.cn/\d{4}/\d{4}/\d+\.s?html'),
                           deny=(r'http://auto.chengdu.cn/2018/0810/1994208.shtml',
                                 r'http://auto.chengdu.cn/2018/1024/2009133.shtml',
                                 r'http://auto.chengdu.cn/2018/1108/2012579.shtml',
                                 r'http://auto.chengdu.cn/2019/0327/2033405.shtml')
                           ), callback='parse_item',
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='arc-box']/h1/text()").extract_first()
            content_div = xp("//div[@class='arc-body font14']")[0]
            pubtime = xp("//div[@class='tag f-st']/text()").re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')[0].strip()
            origin_name = xp("//div[@class='tag f-st']/text()").extract_first().split('来自：')[1] \
                          or xp("//div[@class='tag f-st']/a/text()").extract_first() \
                          or ''
        except:
            return self.parse_item_2(response)

        content, media, _, _ = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp("//h2[@class='f-ot24 cent']/text()").extract_first()
            content_div = xp("//div[@class='body']")[0]
            pubtime = xp("//div[@class='tag sl']/text()").re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')[0].strip()
            origin_name = xp("//div[@class='tag sl']/text()").extract_first().split('来自：')[1].strip() \
                          or xp("//div[@class='tag sl']/a/text()").extract_first().strip() \
                          or ''
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