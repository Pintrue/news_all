# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class ceweeklySpider(NewsRCSpider):
    """中国经济周刊"""
    name = 'ceweekly'
    mystart_urls = {
        'http://www.ceweekly.cn/': 560,  # '首页'
        'http://www.ceweekly.cn/news/comment/': 561,  # 时评
        'http://www.ceweekly.cn/company/': 562,  # 公司
        'http://www.ceweekly.cn/economic/it/': 563,  # 科教
        'http://www.ceweekly.cn/finance/macro/': 564,  # '宏观'
        # 来自spiders_all
        # 'http://www.ceweekly.cn/company/': 687,  # 首页-公司  和562 url重复 但mongo source中没删除687
        'http://www.ceweekly.cn/area/shanghai/': 688,  # 区域-上海
        'http://www.ceweekly.cn/area/beijing/': 689,  # 区域-北京
        'http://www.ceweekly.cn/area/guangdong/': 690,  # 区域-广东
        'http://space.ceweekly.cn/chenweishan': 691,  # 专栏-陈惟衫
        'http://space.ceweekly.cn/chendongdong': 692,  # 专栏-陈栋栋
        'http://space.ceweekly.cn/niuwenxin': 693,  # 专栏-钮文新
        'http://space.ceweekly.cn/xiewei': 694,  # 专栏-谢玮
        'http://space.ceweekly.cn/zhangyan': 695,  # 专栏-张燕
        'http://space.ceweekly.cn/zhouqi': 696,  # 专栏-周琦
    }
    # http://www.ceweekly.cn/2019/0305/250830.shtml
    rules = (Rule(LinkExtractor(allow=r'ceweekly.cn/%s\d{2}/\d+.shtml' % datetime.today().strftime('%Y/%m'),
                                deny=('video', 'audio'),
                                # restrict_xpaths="//div[@class='column mar-t-10'][2]"   之前有的  线上最新的3.14
                                ),
                  callback='parse_item',
                  follow=False),
             )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            pubtime = xp('//span[@class="date"]/text()')[0].extract()
            title = xp('//h1[@class="article-title"]/text()')[0].extract().strip()
            content_div = xp('//div[@class="article-content fontSizeSmall BSHARE_POP"]')[0]
            origin_name = xp("//span[@class='source']/text()").extract_first('')
            content, media, videos, cover = self.content_clean(content_div, need_video=True, kill_xpaths=[])
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
