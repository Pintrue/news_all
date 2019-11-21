# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class DajiangwSpider(NewsRCSpider):
    """大江网"""
    name = 'djw'
    mystart_urls = {
        'http://2008.jxnews.com.cn/soccer/': 1301354,  # 大江网 足球-足球列表

    }
    rules = (
        #http://sports.jxnews.com.cn/system/2019/06/20/017538088.shtml
        #http://sports.jxnews.com.cn/system/2019/06/20/017538073.shtml
        Rule(LinkExtractor(allow=(r'sports.jxnews.com.cn.*?/%s/\d{2}/\d+.shtml' % datetime.today().strftime('%Y/%m'), ),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='BiaoTi']/text()").extract_first()
            # source = xp("//div[@class='time_source mt20']")[0]
            content_div = xp("//div[@class='Content']")[0]
            pubtime = xp("//span[@id='pubtime_baidu']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            origin_name = xp('//div[7]/a[@class="deepred"]/text()').extract_first('')
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
