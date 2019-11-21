# -*- coding: utf-8 -*-


from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from news_all.spider_models import NewsRCSpider


class YcwbAllSpider(NewsRCSpider):
    """金羊网"""
    name = 'ycwb_all'

    mystart_urls = {

        'http://3c.ycwb.com/ityj.htm': 1301444,  # 金羊网-业界动态
        'http://news.ycwb.com/n_gn.htm': 1301446,  # 金羊网-国内
        'http://news.ycwb.com/n_gj.htm': 1301445,  # 金羊网-国际-左下侧列表采集
        'http://3c.ycwb.com/mobile.htm': 1301443,  # 金羊网-手机-列表
        'http://auto.ycwb.com/auto_newcars.htm': 1301205,  # 金羊网-新车
        'http://auto.ycwb.com/auto_ceping.htm': 1301204,  # 金羊网-试驾
        'http://www.ycen.com.cn/2016news/yule/': 1301540,  # 银川晚报-娱乐-左侧列表

    }

    # http://3c.ycwb.com/2019-06/24/content_30285020.htm    http://3c.ycwb.com/2019-06/21/content_30283495.htm
    rules = (
        Rule(LinkExtractor(allow=r'ycwb.com/%s/\d+/content_\d+.htm' % datetime.today().strftime('%Y-%m'),
                           deny='video', ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//h1/text()').extract()[0]
            content_div = xp('//div[@class="main_article"]')[0]
            head_div = xp('//div[@class="source"]')[0]
            pubtime = head_div.re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}')[0]
            
            
        except:
            return self.produce_debugitem(response, "xpath error")
        # origin_name = "".join(source_div.re(r'[\u4e00-\u9fa5]+')).replace('来源', '').strip()
        origin_name = head_div.xpath('//span[@id="source_baidu"]/text()').extract_first()
        content, media, videos, video_cover = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media,
            videos=videos,
        )

