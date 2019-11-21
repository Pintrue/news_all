# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import *
from news_all.tools.time_translater import timestamps


class hao123gaoxiaoSpider(NewsRCSpider):
    """hao123搞笑"""
    name = 'hao123gaoxiao'
    
    mystart_urls_base = {
        'http://www.hao123.com/gaoxiao': 3791,  # 网站-垂直网站-hao123-搞笑-搞笑首页
        'http://www.hao123.com/gaoxiao/lieqi': 3795,  # 网站-垂直网站-hao123-搞笑-猎奇八卦
    }
    
    # http://www.hao123.com/gaoxiao?pn=200
    mystart_urls = {i + '?pn=' + str(p): j for i, j in mystart_urls_base.items() for p in range(1, 201)}
    
    rules = (
        Rule(LinkExtractor(allow=(r'hao123.com/gaoxiao/detail/\d+')),
             callback='parse_item', follow=False),
        # http://www.hao123.com/gaoxiao/lieqi/detail/12074
        Rule(LinkExtractor(allow=(r'hao123.com/gaoxiao/lieqi/detail/\d+')),
             callback='parse_item_2', follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='brief']/a/text()").extract_first('') or self.get_page_title(response).replace(
                '_搞笑__hao123上网导航', '')
            cv = xp("//div[@class='txt-content']").extract() + xp("//div[@class='pic-content']").extract()
            content, media, _, _ = self.content_clean(cv)
        except:
            return self.produce_debugitem(response, "xpath error")
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=timestamps(),
            content=content,
            media=media,
        )
    
    def parse_item_2(self, response):
        # http://www.hao123.com/gaoxiao/lieqi/detail/12074
        xp = response.xpath
        try:
            title = xp("//div[@class='title js_title']/h3/text()").extract_first('')
            # txtContent clearfix js_txtContent
            # picContent clearfix js_picContent
            cv = xp("//div[@id='joker-lieqi-detail']")[0]
            content, media, _, _ = self.content_clean(cv, kill_xpaths=["//div[@class='title js_title']",
                                                                "//div[@class='zhuanti-roller js_zhuanti_roller']",
                                                                "//div[@class='joker-controller js_joker_controller']",
                                                                "//div[@class='vote-comment js_vote_comment']",
                                                                "//div[@class='comment-frame']", ])
        
        except:
            return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,
            title=title,
            pubtime=timestamps(),
            content=content,
            media=media,
        )
