# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class chnfundSpider(NewsRCSpider):
    """中国基金报_第四批"""
    name = 'chnfund'
    mystart_urls = {
                'http://www.chnfund.com/': 578,   #  首页
                'http://www.chnfund.com/bank': 580,   #  银行
                'http://www.chnfund.com/kx': 581,   #  股市
                # spiders_all 新增的
                'http://www.chnfund.com/company': 6299,  # 公司
                'http://www.chnfund.com/trust': 6300,  # 信托
                'http://www.chnfund.com/fund': 6302,  # 基金
                'http://www.chnfund.com/security': 6303,  # 券商
    }
    #http://www.chnfund.com/article/AR2019022609132430367649
    rules = (Rule(LinkExtractor(allow=(r'chnfund.com/article.*?',), ), callback='parse_item', follow=False),)

    def parse_item(self, response):
        try:
            title = response.xpath('//h2[@class="article-title"]/text()')[0].extract().strip()
            content_div = response.xpath('//div[@class="article-content"]')[0]
            pubtime = response.xpath('//span[@class="publish-time"]/text()').extract_first("")
        except:
            return self.produce_debugitem(response, "xpath error")

        source_re = response.xpath('//span[@class="article-source"]/text()')[0].extract().strip()
        origin_name = source_re if source_re else ''
        content, media, videos, cover = self.content_clean(content_div, kill_xpaths=[])

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

