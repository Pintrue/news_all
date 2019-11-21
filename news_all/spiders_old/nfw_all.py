# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Nfw_allSpider(NewsRCSpider):
    """南方网"""
    name = 'nfw'
    mystart_urls = {
        'http://economy.southcn.com/node_196431.htm': 1301459,  # 南方网 原创-左侧列表
        'http://economy.southcn.com/node_321266.htm': 1301458,  # 南方网 理财-左侧列表
        'http://news.southcn.com/community/': 1301460,  # 南方网 社会-左侧列表
        'http://qy.southcn.com/q/node_287651.htm': 1201026,  # 南方网-民生-左侧列表

    }

    rules = (
        #http://economy.southcn.com/e/2019-06/13/content_187943427.htm
        #http://economy.southcn.com/e/2019-06/13/content_187952055.htm
        #http://news.southcn.com/community/content/2019-06/13/content_187947678.htm
        #http://qy.southcn.com/content/2019-03/18/content_186069918.htm
        Rule(LinkExtractor(allow=(r'economy.southcn.com/e/%s/\d{2}/content_\d+.htm' % datetime.today().strftime('%Y-%m'),),
                           ), callback='parse_item',
             follow=False),

        Rule(LinkExtractor(
            allow=(r'(?:news|qy).southcn.com.*?/%s/\d{2}/content_\d+.htm' % datetime.today().strftime('%Y-%m'),),
            ), callback='parse_item',
             follow=False),

    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h2[@id='article_title']/text()").extract_first()
            content_div = xp("//div[@id='content']")[0]

            pubtime = xp("//div[@class='fl']/span[@id='pubtime_baidu']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]

            
            
            origin_name =xp('//div[@class="fl"]/span[@id="source_baidu"]/text()').extract_first('')
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")
        
        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )
