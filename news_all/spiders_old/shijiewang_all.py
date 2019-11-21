# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class ShijieSpider(NewsRCSpider):
    """视界网"""
    name = 'sjw'
    mystart_urls = {
        'http://sports.cbg.cn/': 1301240,  # 视界网 体育-左侧列表采集
        'http://cq.cbg.cn/': 1301236,  # 视界网 原创-左侧列表采集
        'http://common.cbg.cn/shishang/': 1301239,  # 视界网 娱乐
        'http://news.cbg.cn/yl/': 1301242,  # 视界网 娱乐
        'http://common.cbg.cn/lvyou/': 1301237,  # 视界网 旅游
        'http://common.cbg.cn/qiche/': 1301486,  # 视界网 汽车-左侧列表
        'http://news.cbg.cn/': 1301238,  # 视界网 社会
        'http://news.cbg.cn/hotnews/': 1301241,  # 视界网 要闻
    }
    rules = (
        #http://sports.cbg.cn/tiyu/2019/0625/11211287.shtml
        #http://cq.cbg.cn/ycxw/2019/0625/11211643.shtml
        #http://news.cbg.cn/yl/2019/0624/11209883.shtml
        # http://cq.cbg.cn/ycxwsp/ycxwsp2019/0730/11255035.shtml

        # Rule(LinkExtractor(allow=(r'cbg.cn.*?%s\d{2}/\d+.s?html' %datetime.today().strftime('%Y/%m'),),
        #                    ), callback='parse_item',
        #      follow=False),
        Rule(LinkExtractor(allow=(r'cbg.cn/.*?\d{4}/\d{4}/\d+.s?html',),
                           ), callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=(r'cbg.cn.*?\d+.s?htm',), deny=(r'/201[0-8]', r'/2019/0[1-9]'),
                           ), process_request=otherurl_meta,
             follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            if xp('//div[@class="v_message"]'):
                return self.produce_debugitem(response, 'video filter')
            title = xp("//p[@class='title'][1]/text()").extract_first()
            source = xp("//p[@class='time']")[0]
            # content_div = xp("//div[@class='main']/article")[0]
            content_div = xp("//div[@class='main']/article/div")
            pubtime = source.re(r'\d{2,4}年\d{1,2}月\d{1,2}日')[0]

            og = xp("//p[@class='time']").re(r'来源：\w+')
            origin_name = og[0] if og else ""
            content, media, _, _ = self.content_clean(content_div,
                                                      kill_xpaths='//div[@class="title_top"]/preceding-sibling::*')
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
