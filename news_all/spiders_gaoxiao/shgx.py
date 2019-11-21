# -*- coding: utf-8 -*-


from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.spider_models import NewsRCSpider
from news_all.tools.time_translater import timestamps


class ShgxSpider(NewsRCSpider):
    '''搜狐搞笑'''
    name = 'shgx'
    mystart_urls = {
        "http://www.sohu.com/tag/66633?spm=smpc.tag-page.hot-spots.12.1566265767944kWUAcL2": 3815,  # 网站-门户网站-搜狐网-吐槽
        "http://www.sohu.com/tag/77833?spm=smpc.tag-page.hot-spots.2.1566285828259Bf1Mdf7": 3816,  # 网站-门户网站-搜狐网-爱情小说
        "http://www.sohu.com/tag/70304?spm=smpc.tag-page.hot-spots.7.1566285795032UVc4sCJ": 3817,  # 网站-门户网站-搜狐网-笑话
        "http://www.sohu.com/tag/71334?spm=smpc.tag-page.hot-spots.8.1566285788529vRu3aN5": 3818,
        # 网站-门户网站-搜狐网-freestyle
        "http://www.sohu.com/tag/71337?spm=smpc.tag-page.hot-spots.9.1566285782339Br2tVjj": 3819,  # 网站-门户网站-搜狐网-方言
        "http://www.sohu.com/tag/70339?spm=smpc.tag-page.hot-spots.10.1566285744163nEovARO": 3820,  # 网站-门户网站-搜狐网-内涵
        "http://www.sohu.com/tag/70340?spm=smpc.tag-page.hot-spots.11.1566285737931f3D0JqO": 3821,  # 网站-门户网站-搜狐网-爆笑
    }
    rules = (
        # http://www.sohu.com/a/335302890_99984457?spm=smpc.tag-page.feed.1.1566369635675R1LUw0o
        Rule(LinkExtractor(allow=(r'sohu.com/a/.*?',),
                           ), callback='parse_item',
             follow=False)
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='text-title']/h1/text()").extract_first() or \
                    self.get_page_title(response).split('_')[0]
            # pubtime = xp("//span[@id='news-time']/text()").extract_first()
            content_div = xp("//article[@id='mp-editor']")[0]
        except:
            return self.produce_debugitem(response, 'xpath error')

        content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[
            "//article[@id='mp-editor']/p[last() - position() < 2]", ])

        return self.produce_item(
            response=response,
            title=title,
            pubtime=timestamps(),
            content=content,
            media=media
        )
