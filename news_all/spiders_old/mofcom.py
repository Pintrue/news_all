# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.conf import settings
from news_all.spider_models import NewsRSpider
import re


class MofcomSpider(NewsRSpider):
    """商务预报-动态"""
    name = 'mofcom'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        'http://cif.mofcom.gov.cn/cif/getListByNodeId.fhtml?nodeId=6&num=1': 1302079,
    }

    def parse(self, response):
        # rs = json.loads(response.text)
        # print(rs)
        res = response.text
        # http://cif.mofcom.gov.cn/cif/html/app/mobile_hgjj/2019/4/1554273761016.html
        datas = re.findall('http://cif\.mofcom\.gov\.cn/cif/html/app/mobile_hgjj/.*?\.html', res)
        for data in datas:
            yield Request(data, callback=self.parse_item, meta={'source_id': response.meta.get('source_id'), })

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//div[@class="content_item_article_title"]/text()').extract()[0].strip()
            # 2019-4-1 21:55
            pubtime = xp('//div[@class="content_item_article_auth"]/span[1]/text()').extract()[0].strip()
            
            
            cv = xp('//div[@class="content_item_article_desc"]')[0]
            content, media, video, cover = self.content_clean(cv)
            origin_name = xp('//div[@class="content_item_article_auth"]/span[2]').re('来源:([\w-]+)')[0]
        except:
            # return self.parse_item_2(response)
            return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media,
        )
