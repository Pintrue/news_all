# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider
from news_all.tools.others import get_sub_str_ex


class XjjwSpider(NewsRCSpider):
    """宣讲家网"""
    name = 'xjjw'
    mystart_urls = {
        'http://www.71.cn/sddjt/speech/': 99850,  # 宣讲家网-文稿
        'http://www.71.cn/acastudies/impremarks/speech/': 99851,  # 宣讲家网-要闻
    }
    rules = (
        # http://www.71.cn/2019/0109/1030117.shtml
        # http://www.71.cn/2018/1227/1029122.shtml
        Rule(LinkExtractor(allow=(r'71.cn/%s\d{2}/\d+.shtml' % datetime.today().strftime('%Y/%m'),),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1/text()").extract_first() or self.get_page_title(response).split('−')[0]
            pubtime = xp("//div[@class='article-infos']/span[@class='date']/text()").extract_first('')
            content_div = xp("//div[@id='article-content']")[0]
            origin_name = xp('//span[@class="source"]/text()').extract_first('')
            content, media, videos, _ = self.content_clean(content_div, need_video=True,
                                                           kill_xpaths='//*[re:match(text(), "点击|此观|查看\w{0,8}视频|报告")]')
        except:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )

    def parse_item_2(self, response):
        # 图集 http://www.71.cn/2019/0902/1056778.shtml
        xp = response.xpath
        try:
            title = xp("//h1/text()").extract_first()
            pubtime = xp('//span[@class="post-time"]/text()').extract_first('')
            content = xp('//p[@class="summary"]').extract_first('')

            origin_name = xp('//span[@class="source"]/text()').extract_first('')
            media = {'images': {}}

            pics = xp('//script[re:match(text(), "photos.push")]').re(r'photos.push\((.*?)\)')
            for i, j in enumerate(pics):
                try:
                    media['images'][str(i + 1)] = {"src": next(get_sub_str_ex(j, "orig: '", '\'', False))}
                    content += "<p>${{%s}}$</p><p>" % (i + 1) + next(get_sub_str_ex(j, 'note: "', '"', False)).encode('utf-8').decode('unicode_escape') + '</p>'
                except:
                    pass  # 防止next 取不到

        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )
