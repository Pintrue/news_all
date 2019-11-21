# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Dzw_allSpider(NewsRCSpider):
    """大众网"""
    name = 'dzw'
    mystart_urls = {
        'http://www.dzwww.com/': 98359,  # 大众网-头条下部要闻
    }
    rules = (
        # https://www.dzwww.com/xinwen/guoneixinwen/201906/t20190617_18836717.htm
        # https://www.dzwww.com/2019/ys/zb/201906/t20190617_18838520.htm
        # https://sd.dzwww.com/sdnews/201906/t20190617_18838591.htm
        Rule(LinkExtractor(allow=(r'dzwww.com.*?/%s/t\d{8}_\d{8}.htm' % datetime.today().strftime('%Y%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    # http://zhongbo.dzwww.com/dszb/dq/201911/t20191101_19314828.htm
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("/html/head/title/text()").extract_first().split('_')[0]
            content_div = xp("//div[@class='TRS_Editor']")[0]
            pubtime = xp("//div[@class='layout']/div[@class='left']").re(r'\d{2,4}-\d{1,2}-\d{1,2}\s*(?:\d{2}:*)*')[0]
            origin_name = xp('/html/head/meta[@name="source"]/@content').extract()[0]
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

    # http://elec.dzwww.com/ttxw/201906/t20190618_18841449.htm
    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp("//h1/text()").extract_first()
            content_div = xp("//div[@class='TRS_Editor']")[0]
            try:
                pubtime = xp("//div[@class='left']/span[1]").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
                origin_name = xp("//div[@class='left']/span[2]/text()").extract_first('')
            except IndexError as _:
                pubtime = xp("//div[@id='headline']/i/text()").extract()[0]
                origin_name = xp('/html/head/meta[@name="source"]/@content').extract()[0]
        except:
            return self.parse_item_3(response)

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    #http://yuqing.dzwww.com/wxphb/sdzwyxlbd/zw/201906/t20190617_18839258.html
    def parse_item_3(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='top']/h1/text()").extract_first()
            # source = xp("//h3[@class='daty']")[0]
            content_div = xp("//div[@class='con']")[0]
            pubtime = xp("//div[@class='top']/p").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp('//div[@class="top"]/p/text()').extract_first('')
        except:
            return self.parse_item_4(response)

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://www.dzwww.com/special/ts/jtz/201906/t20190611_18815924.htm
    def parse_item_4(self, response):
        xp = response.xpath
        try:
            title = xp("//h2/text()").extract_first()
            # source = xp("//h3[@class='daty']")[0]
            # content_div = xp("//div[@class='TRS_Editor']")[0]
            content_div = xp("//div[@id='news-body' or @class='TRS_Editor']")[0]
            try:
                pubtime = xp("//div[@class='txt' or @class='pic-head']/p/span[1]")\
                    .re(r'\d{2,4}[年-]\d{1,2}[月-]\d{1,2}日*\s*(?:\d{2}:*)*')[0]
                origin_name = xp("//div[@class='txt' or @class='pic-head']/p/span[2]/text()").extract_first('')
            except IndexError as _:
                # https://sd.dzwww.com/sdnews/201911/t20191107_19332887.htm
                """
                    ^^ 特殊的pubtime格式，其他attributes格式大概相同
                """
                pubtime = xp("normalize-space(//div[@class='date'])").extract_first()\
                    .replace(' ', '/', 1).replace('//', '/')
                origin_name = xp("//div[@id='news-side']/div[@class='text']/p/text()").extract_first()
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
