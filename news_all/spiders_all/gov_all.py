# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class GovAllSpider(NewsRCSpider):
    """教育部网站"""
    name = 'gov_all'
    mystart_urls = {

        'http://www.moe.gov.cn/jyb_xwfb/s6052/': 2344,
        'http://www.moe.gov.cn/jyb_sy/sy_jyyw/': 2345, 'http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/': 2346,
        'http://www.moe.gov.cn/jyb_xwfb/s5148/': 2347, 'http://www.moe.gov.cn/jyb_xwfb/s6192/s133/': 2348,
        'http://www.moe.gov.cn/jyb_xwfb/xw_fbh/moe_2069/xwfbh_2019n/': 2349
    }

    # http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/moe_1485/201904/t20190422_379118.html
    rules = (
        Rule(LinkExtractor(allow=(r'moe.gov.cn/.*?/%s.*?\d+.html'%datetime.today().year), ),
                           callback='parse_item', follow=False),
    )

    # http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/moe_1485/201904/t20190422_379118.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@id="content_body"]')[0]
            source_div = news_div.xpath('./div[@id="content_date_source"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = news_div.xpath('./div[@class="TRS_Editor"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        title = news_div.xpath('./h1/text()').extract_first('').strip()
        sub_title = news_div.re(r'var file_subdoctitle=.*?;')[0].replace('var file_subdoctitle=\'', '').replace('\';', '')
        if( len(sub_title) ==0):
            sub_title = news_div.re(r'var file_yt=.*?;')[0].replace('var file_yt=\'', '').replace(
                '\';', '')
        title = join_titles(title, sub_title)

        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media
        )

    def get_full_title(self, title_div, response):
        # 新闻标题  副标题本身以"——"开头的直接把主副标题连起来, 否则主+"——"+副
        # pre_title = ''.join(i.strip() for i in title_div.xpath('.//*[contains(@class,"pre")]/text()').extract())
        # http://dangjian.people.com.cn/n1/2019/0211/c117092-30617896.html 标题内如有<br>等html标签都删除只保留text拼接
        title = ''.join(i.strip() for i in title_div.xpath('.//h1/text()').extract())
        sub_title = ''.join(i.strip() for i in title_div.xpath('.//h2/text()').extract() or title_div.xpath(
            './/*[contains(@class,"sub")]/text()').extract())
        return join_titles(title, sub_title)


def join_titles(title, sub_title):
    if sub_title:
        if sub_title.startswith("——"):
            title += sub_title
        else:
            title += "——" + sub_title
    return title
