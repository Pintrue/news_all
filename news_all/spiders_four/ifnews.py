# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, isStartUrl_meta
from news_all.tools.time_translater import Pubtime


class ifnewsSpider(NewsRCSpider):
    """国际金融报网_第四批"""
    name = 'ifnews'
    mystart_urls = {
        'http://www.ifnews.com/': 573,  # 首页
        'http://www.ifnews.com/5/': 574,  # 公司
        'http://www.ifnews.com/18/': 575,  # 金融
        'http://www.ifnews.com/19/': 576,  # 机构
        'http://www.ifnews.com/3/': 577,  # 国际
    }

    rules = (
        Rule(LinkExtractor(allow=(r'ifnews.com/.*?\d+.html',), ), callback='parse_item', follow=False),
        # http://www.ifnews.com/5/?page=3
        Rule(LinkExtractor(allow=r'ifnews.com/\d+/\?page=\d+',
                           restrict_xpaths='//div[@class="pagelist"]/span[@class="down"]/a'),
             follow=True, process_request=isStartUrl_meta),
             )
    custom_settings = {'DEPTH_LIMIT': 3}  # 列表翻页要设置深度
    
    def parse_item(self, response):
        # http://www.ifnews.com/17/detail-38125.html 采集不全已解决
        if "Database Error" in self.get_page_title(response):
            return self.produce_debugitem(response, 'ifnews.com Database Error')
        xp = response.xpath
        try:
            ps = xp('//span[@class="publish-time"]/text()').extract_first("") or xp('//h2/span/i').extract()[0]
            pubtime = Pubtime(ps)
            title = xp('//h2/text()')[0].extract().strip()
            content_div = xp('//div[@class="left bgf"]')
            content, media, videos, cover = self.content_clean(content_div, need_video=True, kill_xpaths=[r'.//h2',
                                                                                         r'.//div[@class="fx_tit"]/parent::div'])

        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media,
            videos=videos
        )
