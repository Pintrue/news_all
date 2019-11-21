# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class guizhou_allSpider(NewsRCSpider):
    """贵州&贵阳日报"""
    name = 'gzrb'
    mystart_urls = {
        'http://comment.gywb.cn/': 1301168,  # 贵州日报 甲秀评论-中间列表
        'http://www.gywb.cn/gynews/node_694.htm': 1301397,  # 贵阳日报_本地新闻

    }
    rules = (
        #http://www.gywb.cn/content/2019-05/31/content_6134092.htm
        #http://www.gywb.cn/system/2019/06/24/030077990.shtml
        Rule(LinkExtractor(allow=(r'gywb.cn.*?/%s/\d{2}/content_\d+.htm' % datetime.today().strftime('%Y-%m'), ),
                           ), callback='parse_item',
             follow=False),

        Rule(LinkExtractor(allow=(r'gywb.cn.*?/%s/\d{2}/\d+.shtml' % datetime.today().strftime('%Y/%m'),),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='g-content-t text-center']/text()").extract_first()
            content_div = xp("//div[@class='g-content-c']")
            pubtime = xp("//span[@id='pubtime_baidu']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//span[@id='source_baidu']/text()").extract_first('')
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

    #http://www.gywb.cn/system/2019/06/18/030070939.shtml
    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='textTitle']/h2/text()").extract_first()
            content_div = xp("//div[@class='textCon']")[0]
            pubtime = xp("//div[@class='textTitle']/span[1]").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            origin_name = xp("//div[@class='textTitle']/span[2]/text()").extract_first('')
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
