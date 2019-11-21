# -*- coding: utf-8 -*-
# @Time   : 2019/3/6 上午9:08
# @Author : NewmanZhou
# @Project : news_all
# @FileName: cnenergynews_gn_sj_spider.py

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class CnenergynewsGNSJSpipder(NewsRCSpider):
    name = 'cnenergynews_gn_sj_spider'

    # 中国能源报 ==》 国内 ==》时间
    mystart_urls = {
        'http://www.cnenergynews.cn/yw/': 569,  # '国内 时间'
        'http://www.cnenergynews.cn/yq/sy/': 571,  # '石油  时间'
        'http://www.cnenergynews.cn/xny_183/': 572,  # '新能源  时间'
    }
    # http://www.cnenergynews.cn/xwzt/2019lhzt/lhtt/201903/t20190304_753302.html
    rules = (Rule(LinkExtractor(allow=r'cnenergynews.cn/.*?\d+.html', deny=('video', 'audio'),
                                restrict_xpaths='//div[@class="main4_left"]/div[position()=2]'),
                  callback='parse_item', follow=False),
             )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='xltitle']/text()").extract()[0]
            pubtime = xp("//div[@class='xltimer']/span[@class='xltimerl']/text()").extract()[0].strip()
            origin_name = xp("//div[@class='xltimer']/span[@class='xltimerl']/span[@class='laiyuan']/span/text()").extract_first('')
            cv = xp("//div[@class='xlcontent']")[0]
            content, media, video, cover = self.content_clean(cv, need_video=False)
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
