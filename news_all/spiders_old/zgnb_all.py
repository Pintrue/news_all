# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from news_all.tools.time_translater import Pubtime


class Zgnb_allSpider(NewsRCSpider):
    """中国宁波网"""
    name = 'zgnb'
    mystart_urls = {
        'http://news.cnnb.com.cn/tyxw/': 1301621,  # 中国宁波网-体育
        'http://news.cnnb.com.cn/gnyw/gngdxw/index.shtml': 1301622,  # 中国宁波网-各地
        'http://news.cnnb.com.cn/gnyw/gnsz/': 1301624,  # 中国宁波网-国内-左侧列表
        'http://news.cnnb.com.cn/gjyw/guojyw/': 1301623,  # 中国宁波网-国际-左侧列表
        'http://news.cnnb.com.cn/ylxw/': 1301626,  # 中国宁波网-娱乐新闻-文娱列表
        'http://news.cnnb.com.cn/gjyw/hqsy/index.shtml': 1301625,  # 中国宁波网-环球
        'http://news.cnnb.com.cn/shxw/': 1301620,  # 中国宁波网-社会
        # 'http://finance.cnnb.com.cn/zixun/': 1301619,  # 中国宁波网-经济资讯  --此网页打不开  已忽略掉
    }
    rules = (
        # http://news.cnnb.com.cn/system/2019/06/11/030058939.shtml
        # http://news.cnnb.com.cn/system/2019/06/12/030059131.shtml
        Rule(LinkExtractor(allow=(r'news.cnnb.com.cn/system/%s/\d{2}/\d+.s?htm' % datetime.today().strftime('%Y/%m')),
                           ), callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=(r'cnnb.com.cn.*?/\d+.s?htm'), deny=(r'/201[0-8]', r'/2019/0[1-9]')
                           ), process_request=otherurl_meta,
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='heading']/text()").extract_first()
            source = xp("//div[@class='source']/span[@class='left']")[0]
            content_div = xp("//div[@id='Zoom']")[0]
            pubtime = Pubtime(source.extract())
            origin_name = source.xpath('./span[@class="left"]/a/text()').extract_first('')
            content, media, videos, _ = self.content_clean(content_div, need_video=True)
        except BaseException:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )
