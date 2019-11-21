# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class GfbgovSpider(NewsRCSpider):
    '''国防部'''
    name = 'gfbgov'
    mystart_urls = {
        "http://www.mod.gov.cn/topnews/node_46932.htm": 7602,
        "http://www.mod.gov.cn/action/node_46956.htm": 7603,
        "http://www.mod.gov.cn/action/node_46957.htm": 7604,
    }
    rules = (
        # http://www.mod.gov.cn/topnews/2019-06/26/content_4844432.htm
        Rule(LinkExtractor(allow=(r'mod.gov.cn/[a-z]+/\d{4}-\d{2}/\d{2}/content_\d+\.htm',),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title_div = xp("//div[@class='article-header']")[0]
            title = self.get_full_title(title_div, response)
            content_div = xp("//div[@id='article-content']")[0]
            pubtime = xp("//div[@class='info']/span[4]/text()").extract_first().strip()
            origin_name = xp("//div[@class='info']/span[1]/text()").extract_first().replace('来源：','')
        except:
            return self.produce_debugitem(response, "xpath error")
        # 过滤视频


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
    def get_full_title(self, title_div, response):
        # 新闻标题  副标题本身以"——"开头的直接把主副标题连起来, 否则主+"——"+副
        # pre_title = ''.join(i.strip() for i in title_div.xpath('.//*[contains(@class,"pre")]/text()').extract())
        # http://dangjian.people.com.cn/n1/2019/0211/c117092-30617896.html 标题内如有<br>等html标签都删除只保留text拼接
        try:
            title = ''.join(i.strip() for i in title_div.xpath('./h1/text()').extract_first())
            sub_title = ''.join(i.strip() for i in title_div.xpath('./h3/text()').extract_first())
            return join_titles(title, sub_title)
        except:
            # title = ''.join(i.strip() for i in title_div.xpath('./h1/text()').extract_first())
            return title


def join_titles(title, sub_title):
    if sub_title:
        if sub_title.startswith("——"):
            title += sub_title
        else:
            title += "——" + sub_title
    return title
