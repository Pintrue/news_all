# -*- coding: utf-8 -*-
# @Time   : 2019/8/26 下午2:05
# @Author : NewmanZhou
# @Project : news_all
# @FileName: peopleweekly_video.py


from news_all.spider_models import NewsRCSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from datetime import datetime


class PeopleWeeklyVideoSpider(NewsRCSpider):
    """人民周刊 视频"""
    name = 'peopleweekly_video'

    mystart_urls = {
        'http://www.peopleweekly.cn/html/gongyoulanmu/shipin/': 3879,  # 人民周刊_视频
    }

    # http://www.peopleweekly.cn/html/2019/shipin_0619/15782.html
    rules = (
        Rule(LinkExtractor(allow=(r'peopleweekly\.cn/html/%s/shipin_\d{4}/\d+.html') % datetime.today().strftime('%Y'),
                           ), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            origin_name = xp('//div[@id="Article"]/div[@class="rexw-ly sp-ly"]/p/span/text()').extract_first()
            title = xp('//div[@class="container rmxw-spinfo spauto"]/div[@class="row"]/h1/text()').extract_first()
            pubtime = xp('//div[@id="Article"]/div[@class="rexw-ly sp-ly"]/p/text()').extract_first()

            content_div = xp('//video[@id="my-video"]').extract() + xp('//div[@class="content"]').extract()
            content, media, videos, _ = self.content_clean(content_div, need_video=True)
        except:
            return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,
        )
