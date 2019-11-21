# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Sczx_allSpider(NewsRCSpider):
    """四川在线"""
    name = 'sczx'
    mystart_urls = {
        'https://sichuan.scol.com.cn/fffy/': 1301252,  # 四川在线 四川新闻-原创-左侧列表采集
        'https://sichuan.scol.com.cn/sczh/': 1301251,  # 四川在线 四川新闻-社会故事
        'https://sichuan.scol.com.cn/dwzw/': 1301491,  # 四川在线 天府要闻
        'https://it.scol.com.cn/jd/': 1301494,  # 四川在线 尚生活频道-慧生活
        'https://women.scol.com.cn/cxb/': 1301493,  # 四川在线 尚生活频道-潮生活
        'https://women.scol.com.cn/mls/': 1301495,  # 四川在线 尚生活频道-美生活
        'https://teach.scol.com.cn/cczx/': 1301492,  # 四川在线 教育-成长资讯列表
        'https://tour.scol.com.cn/xwdt/': 1301248,  # 四川在线 旅游-新闻动态
        'https://auto.scol.com.cn/053/': 1301249,  # 四川在线 汽车-观点原创-左侧列表

    }
    rules = (
        #https://sichuan.scol.com.cn/fffy/201906/56997790.html
        #https://sichuan.scol.com.cn/sczh/201906/56997451.html
        #https://women.scol.com.cn/cxb/201906/56997672.html
        #https://women.scol.com.cn/mls/201906/56995611.html
        #https://teach.scol.com.cn/cczx/201904/56846979.html
        #https://auto.scol.com.cn/053/201905/56986912.html
        #https://it.scol.com.cn/jd/201906/56995600.html
        Rule(LinkExtractor(allow=(r'(?:sichuan|it|women|teach|auto).scol.com.cn.*?/%s/\d+.html' % datetime.today().strftime('%Y%m'),),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@id='webreal_scol_title']/text()").extract_first()
            # source = xp("//div[@id='scol_time']")[0]
            content_div = xp("//div[@id='scol_txt']")[0]

            pubtime = xp("//div[@id='scol_time']/span[@id='pubtime_baidu']").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            
            
            origin_name =xp('//div[@id="scol_time"]/span[@id="source_baidu"]/a/text()').extract_first('')
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
