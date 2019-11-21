# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Sxxw_allSpider(NewsRCSpider):
    """山西新闻网"""
    name = 'sxxw'
    mystart_urls = {
        'http://news.sxrb.com/sxxww/xwpd/ty/': 1301482,  # 山西新闻网 体育新闻
        'http://news.sxrb.com/sxxww/xwpd/ylxw/': 1301483,  # 山西新闻网 娱乐新闻列表
        'http://www.sxrb.com/sxxww/xwpd/shxw/': 1301481,  # 山西新闻网 社会新闻

        # 'http://jt.sxrb.com/jtyw/': 1301480,  # 山西新闻网 交通要闻    404 not found
        # 'http://travel.sxrb.com/mysx/': 1301479,  # 山西新闻网 慢游山西  404 not found
        # 'http://travel.sxrb.com/lxkb/': 1301478,  # 山西新闻网 旅讯快播  404 not found
        # 'http://jr.sxrb.com/jrtt/': 1301477,  # 山西新闻网 金融头条   404 not found
    }

    rules = (
        #http://news.sxrb.com/sxxww/xwpd/ty/7950856.shtml
        #http://news.sxrb.com/sxxww/xwpd/ylxw/7950821.shtml
        #http://www.sxrb.com/sxxww/xwpd/shxw/7951216.shtml
        Rule(LinkExtractor(allow=(r'news.sxrb.com/sxxww/xwpd/[a-z]+/\d+.shtml'),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='catalog_main']/p[@class='art_tit']/text()").extract_first()
            source = xp("//h3[@class='art_info']")[0]
            content_div = xp("//div[@class='art_txt']")[0]

            pubtime = xp("//h3[@class='art_info']/span[1]").re(r'\d{2,4}年\d{1,2}月\d{1,2}日')[0]
            
            
            origin_name =xp('//h3[@class="art_info"]/span[2]/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )
