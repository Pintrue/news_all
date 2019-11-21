# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class RmzxbSpider(NewsRCSpider):
    """人民政协报"""
    name = 'rmzxb'
    mystart_urls = {
        'http://www.rmzxb.com.cn/zxxs/zzx/index.shtml': 1301476,  # 人民政协报 政协·协商-最政协
        'http://www.rmzxb.com.cn/zszq/tj/index.shtml': 1301475,  # 人民政协报 政声·政情-推荐列表
        'http://www.rmzxb.com.cn/sqmy/lgsh/index.shtml': 1301471,  # 人民政协报 社情民意-乐观社会
        'http://www.rmzxb.com.cn/sqmy/nywy/index.shtml': 1301472,  # 人民政协报 社情民意-你言我语
        'http://www.rmzxb.com.cn/sqmy/hlyh/index.shtml': 1301470,  # 人民政协报 社情民意-画里有话
        'http://www.rmzxb.com.cn/yl/rp/index.shtml': 1301473,  # 人民政协报 要论-锐评
        'http://www.rmzxb.com.cn/yw/tx/index.shtml': 1301474,  # 人民政协报 要闻-天下
        'http://whkj.rmzxb.com.cn/index.shtml': 1301469,  # 人民政协报-文化·科教
    }
    rules = (
        # http://www.rmzxb.com.cn/c/2019-05-30/2354458.shtml
        Rule(LinkExtractor(allow=(r'rmzxb.com.cn/c/%s-\d{2}/\d+\.s?htm' % datetime.today().strftime('%Y-%m'),),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='Content_title']/span/text()").extract_first()
            content_div = xp("//div[@class='text_box']")[0]

            pubtime = xp('//div[@class="Remark"]/span[1]').re(r'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            
            
            origin_name = xp("//div[@class='Remark']/span/a/text()").extract_first() or xp(
                '/html/head/meta[@name="source"]/@content').extract_first()

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
