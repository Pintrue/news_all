# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class peopleweeklySpider(NewsRCSpider):
    """人民周刊（人民周刊网）_第四批"""
    name = 'peopleweekly'
    mystart_urls = {
                'http://www.peopleweekly.cn/html/gongyoulanmu/shizheng/': 582,   #  时政
                'http://www.peopleweekly.cn/html/gongyoulanmu/pinglun/': 583,   #  评论
                'http://www.peopleweekly.cn/html/gongyoulanmu/caijing/': 584,   #  经济
                'http://www.peopleweekly.cn/html/gongyoulanmu/wenshi/': 585,   #  文史
                'http://www.peopleweekly.cn/html/gongyoulanmu/pinpai/': 586,   #  品牌
                'http://www.peopleweekly.cn/html/gongyoulanmu/kexue/': 587,   #  科学
    }
    # http://www.peopleweekly.cn/html/2019/shizheng_0306/11824.html
    rules = (Rule(LinkExtractor(allow=(r'peopleweekly.cn/html/%s/.*?\d+.html'%datetime.today().year,), ), callback='parse_item', follow=False),)

    def parse_item(self, response):
        try:
            # title = response.xpath('//h1[@class="zhengbiaoti"]/text()')[0].extract().strip()
            title = response.xpath('//h1/text()')[0].extract().strip()
            try:
                sub_title = response.xpath('//p[@class="fubiaoti"]/text()')[0].extract().strip()
                if sub_title:
                    if sub_title.startswith("——"):
                        title += sub_title
                    else:
                        title += "——" + sub_title
            except:
                pass

            content_div = response.xpath('//div[@class="content"]')[0]
            # head_div = response.xpath('//div[@class="rexw-ly"]/p')[0]
            head_div = response.xpath('//div[contains(@class,"rexw-ly")]/p')[0]
            time_re = head_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            # origin_name = response.xpath('//div[@class="rexw-ly"]/p/span/text()').extract_first('')
            origin_name = head_div.xpath('.//span/text()').extract()
            origin_name = '' if len(origin_name) <= 0 else origin_name[0]

            content, media, videos, cover = self.content_clean(content_div, kill_xpaths=[])
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

