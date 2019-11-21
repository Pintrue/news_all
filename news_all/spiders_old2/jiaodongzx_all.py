# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Jdzx_allSpider(NewsRCSpider):
    """胶东在线"""
    name = 'jdzx'
    mystart_urls = {
        'http://www.jiaodong.net/ytsports/news/': 1301197,  # 胶东在线-体育动态
        'http://health.jiaodong.net/yangsheng/': 1301439,  # 胶东在线-养生保健
        'http://health.jiaodong.net/news/': 1301438,  # 胶东在线-国内外健康新闻
        'http://www.jiaodong.net/ent/yingshi/': 1301441,  # 胶东在线-影视
        'http://www.jiaodong.net/edu/ytnews/': 1301196,  # 胶东在线-教育要闻-左侧列表
        'http://www.jiaodong.net/travel/news/': 1301440,  # 胶东在线-旅游综合资讯
        'http://health.jiaodong.net/bdyldt/': 1301195,  # 胶东在线-烟台健康资讯

    }
    rules = (
        #http://www.jiaodong.net/ytsports/system/2019/06/19/013888723.shtml
        #http://health.jiaodong.net/system/2019/06/20/013889061.shtml
        #http://www.jiaodong.net/ent/system/2019/06/19/013888575.shtml
        #http://www.jiaodong.net/travel/system/2019/06/20/013889347.shtml

        Rule(LinkExtractor(allow=(r'jiaodong.net.*?/%s/\d{2}/\d+.shtml' % datetime.today().strftime('%Y/%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    #http://www.jiaodong.net/ytsports/system/2019/06/19/013888723.shtml
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@id='content']/h1/text()").extract_first()
            source = xp("//div[@class='source']")[0]
            content_div = xp("//div[@class='f14 lh26']")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            og = xp("//div[@class='source']").re('来源：\s*\w+')
            origin_name = og[0] if og else ""
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    #http://health.jiaodong.net/system/2019/06/20/013889061.shtml
    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='millia']/h1/text()").extract_first()
            source = xp("//div[@class='source f14']")[0]
            content_div = xp("//div[@id='content']")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            og = xp("//div[@class='source f14']").re('来源：\s*\w+')
            origin_name = og[0] if og else ""
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    #http://www.jiaodong.net/ent/system/2019/06/19/013888575.shtml
    def parse_item_3(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='title tc']/text()").extract_first()
            source = xp("//p[@class='sourc tc']")[0]
            content_div = xp("//div[@id='newcontent']")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            og = xp("//p[@class='sourc tc']").re('来源：\s*\w+')
            origin_name = og[0] if og else ""
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_4(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    #http://www.jiaodong.net/travel/system/2019/06/20/013889347.shtml
    def parse_item_4(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@id='content']/h1/text()").extract_first()
            siv = xp("//div[@class='fl pl50 pt5 pr20']") or xp("//div[@class='source f12 tc lh20']")
            source = siv[0]
            content_div = xp("//div[@class='content f14 lh28 pt30']")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            og = xp("//div[@class='fl pl50 pt5 pr20']").re('来源：\s*\w+')
            origin_name = og[0] if og else ""
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_5(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    #http://www.jiaodong.net/edu/system/2019/06/18/013888359.shtml
    def parse_item_5(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='clearfix sysmt20']/h1/text()").extract_first()
            source = xp("//div[@class='source f14 mb30']")[0]
            content_div = xp("//div[@id='content']")[0]
            pubtime = source.re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            og = xp("//div[@class='source f14 mb30']").re('来源：\s*\w+')
            origin_name = og[0] if og else ""
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
