# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from news_all.tools.others import to_list

from news_all.spider_models import NewsRCSpider, NewsSpider, NewsCrawlSpider

class ZgwjbSpider(NewsRCSpider):
    '''中华人民共和国外交部'''
    # 一个错误，但错误网页打不开 https://www.fmprc.gov.cn/web/syldrzt/t1291348.shtml
    name = 'zgwjb'
    mystart_urls = {
        "http://www.fmprc.gov.cn/web/" : 1200990 ,
        'http://www.fmprc.gov.cn/web/wjdt_674879/gjldrhd_674881/': 1200992,  # 外交部-外交动态-右侧列表
        'http://www.fmprc.gov.cn/web/wjbz_673089/': 1200991,  # 外交部-外交部长-中部左侧列表
        'http://www.fmprc.gov.cn/web/ziliao_674904/zyjh_674906/': 1200993,  # 外交部-重要讲话-右侧列表
        'http://www.fmprc.gov.cn/web/wjbz_673089/zyhd_673091/': 1301254,  # 外交部网站 外交部长-相关新闻-右侧列表
    }
    rules = (
        # todo
        # https://www.fmprc.gov.cn/web/wjbzhd/t1670560.shtml
        # https://www.fmprc.gov.cn/web/wjbxw_673019/t1669569.shtml
        # https://www.fmprc.gov.cn/web/wjdt_674879/gjldrhd_674881/t1671434.shtml
        # https://www.fmprc.gov.cn/web/wjbz_673089/xghd_673097/t1671204.shtml
        # https://www.fmprc.gov.cn/web/ziliao_674904/zyjh_674906/t1666974.shtml
        # https://www.fmprc.gov.cn/web/wjbz_673089/zyhd_673091/t1667553.shtml
        Rule(LinkExtractor(allow=(r'fmprc.gov.cn/web/.*?/t\d+\.s?html',),
                           deny=(r'https://www.fmprc.gov.cn/web/syldrzt/t1291348.shtml')),
             callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title_div = xp('//div[@class="vibox"]')[0]
            title = self.get_full_title(title_div, response)
            content_div = xp('//div[@id="News_Body_Txt_A"]')[0]
            # 过滤视频

            # if self.video_filter(content_div) or self.page_turn_filter(content_div):
            #     return
            pubtime = xp('//span[@id="News_Body_Time"]/text()').extract_first()
            # 
            #     return
            
                
            origin_name = ''

        except:
            return self.produce_debugitem(response, "xpath error")
            # return self.parse_item_2(response)
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
        title = ''.join(i.strip() for i in title_div.xpath('.//div[@id="News_Body_Title"]/text()').extract())
        sub_title = ''.join(i.strip() for i in title_div.xpath('.//div[@id="News_Body_subitle"]/text()').extract())
        return join_titles(title, sub_title)

def join_titles(title, sub_title):
    if sub_title:
        if sub_title.startswith("——"):
            title += sub_title
        else:
            title += "——" + sub_title
    return title


