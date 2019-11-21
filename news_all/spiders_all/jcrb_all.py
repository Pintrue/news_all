# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class JcrbAllSpider(NewsRCSpider):
    """正义网"""
    name = 'jcrb_all'
    mystart_urls = {
        'http://news.jcrb.com/Currentpolitical/leaders/': 1981,
        'http://news.jcrb.com/Currentpolitical/personnel/': 1982, 'http://news.jcrb.com/gnxw/': 1983,
        'http://news.jcrb.com/shxw/': 1984, 'http://news.jcrb.com/xwjj/': 1985,
        'http://news.jcrb.com/ycgj/': 1986,
        'http://www.jcrb.com/anticorruption/ffyw/': 2030,
        'http://www.jcrb.com/anticorruption/daya/': 2031, 'http://www.jcrb.com/anticorruption/ffpl/': 2032,
        'http://www.jcrb.com/anticorruption/lzwh/yswj/': 2033,
        'http://www.jcrb.com/anticorruption/tgchl/': 2034,
        'http://www.jcrb.com/culture/literatures/essay/': 2035, 'http://www.jcrb.com/culture/news/': 2036,
        'http://www.jcrb.com/culture/WHYW/': 2037, 'http://www.jcrb.com/FYFZ/zxbd/': 2038,
        'http://www.jcrb.com/gongsupindao/XASD/': 2039, 'http://www.jcrb.com/legal/dong/': 2040,
        'http://www.jcrb.com/legal/jishi/': 2041, 'http://www.jcrb.com/legal/sdbd/': 2042,
        'http://www.jcrb.com/legal/sfgz/': 2043, 'http://www.jcrb.com/legal/yaowen/': 2044,
        'http://www.jcrb.com/opinion/fygc/': 2045, 'http://www.jcrb.com/opinion/jrtt/': 2046,
        'http://www.jcrb.com/opinion/mzsp/': 2047, 'http://www.jcrb.com/opinion/zywy/': 2048,
        'http://www.jcrb.com/procuratorate/GYSS/': 2049, 'http://www.jcrb.com/procuratorate/highlights/': 2050,
        'http://www.jcrb.com/procuratorate/XSJC/': 2051, 'http://www.jcrb.com/spptv/information/': 2052,
    
        # 老爬虫的
        'http://www.jcrb.com/legal/jj/': 87,  # 1301575,  # 正义网-法治频道&gt;&gt;今日头条-左侧列表
    }

    #http://news.jcrb.com/jxsw/201904/t20190409_1986798.html     http://news.jcrb.com/jxsw/201903/t20190322_1979577.html

    rules = (
        Rule(LinkExtractor(allow=(r'jcrb.com/.*?/%s.*?_\d+.html'%datetime.today().year), ),
                           callback='parse_item', follow=False),
    )

    # http://news.jcrb.com/jxsw/201904/t20190409_1986798.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@id="main"]/div[@id="mainLeft"]')[0]
            source_div = news_div.xpath('./div[@id="about"]')[0]
            content_div = news_div.xpath('.//*/div[@class="TRS_Editor"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
        except:
            return self.parse_item2(response)

        title = ''.join(i.strip() for i in news_div.xpath('./h1/text()').extract())
        origin_name = source_div.xpath('./span[@id="source_baidu"]/text()').extract_first('').replace('新闻来源：', '').strip()
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://yq.jcrb.com/SJHLW/HLWJSK/201903/t20190320_1978841.html
    def parse_item2(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="main topk"]/div[@class="mainL wz"]')[0]
            source_div = news_div.xpath('./div[@class="about"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = news_div.xpath('.//*/div[@class="TRS_Editor"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        title = ''.join(i.strip() for i in news_div.xpath('./h1/text()').extract())
        origin_name = source_div.xpath('./span[3]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

