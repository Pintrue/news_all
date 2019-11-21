# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class CmaAllSpider(NewsRCSpider):
    """中国气象网"""
    name = 'cma_all'
    mystart_urls = {
        'http://www.cma.gov.cn/2011zwxx/2011zbmgk/2011zjld/2011zjzlym/2011zzyhdzgg/': 2350,
        'http://www.cma.gov.cn/2011xwzx/2011xqxxw/2011xqxyw/': 2351, 'http://www.cma.gov.cn/2011xwzx/2011xmtjj/': 2352,
        'http://www.cma.gov.cn/2011xwzx/2011xqxxw/2011xylsp/': 2353,
        'http://www.cma.gov.cn/2011xwzx/2011xqxkj/2011xkjdt/': 2354,
        'http://www.cma.gov.cn/2011xwzx/2011xqxkj/2011xkjxm/': 2355,
        'http://www.cma.gov.cn/2011xwzx/2011xqxkj/2011xkjcgyjl/': 2356,
        'http://www.cma.gov.cn/2011xwzx/2011xqxxw/2011xhydt/': 2357,
        'http://www.cma.gov.cn/2011xwzx/2011xqxkj/2011xfzyhz/': 2358,
        'http://www.cma.gov.cn/2011xwzx/2011xqxkj/cxgc/': 2359,
        'http://www.cma.gov.cn/2011xwzx/2011xqhbh/2011xqhbhyhy/': 2360,
        'http://www.cma.gov.cn/2011xwzx/2011xqhbh/2011xkydt/': 2361,
        'http://www.cma.gov.cn/2011zwxx/2011zflfg/2011zzcjd/index_588.html': 2362,
        'http://www.cma.gov.cn/2011zwxx/2011zflfg/2011zzcjd/zjqxjd/': 2363,
        'http://www.cma.gov.cn/2011zwxx/2011zdflz/ywjj/': 2364,
        'http://www.cma.gov.cn/2011zwxx/2011zdflz/2015qtgz/': 2365,
        'http://www.cma.gov.cn/2011xwzx/2011xqxkj/qxkjgjqy/': 2366
    }

    # http://www.cma.gov.cn/2011xwzx/2011xqxxw/2011xqxyw/201904/t20190416_520546.html   http://www.cma.gov.cn/2011xwzx/2011xqxxw/2011xqxyw/201904/t20190419_520792.html

    rules = (
        Rule(LinkExtractor(allow=(r'cma.gov.cn.*?/%s/t\d+_\d+.html'%datetime.today().strftime('%Y%m')), ),
                           callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'cma.gov.cn*?\w+.htm'), deny=(r'/201[0-8]', r'/20190[1-9]/')),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="news_text"]')[0]
            source_div = news_div.xpath('./div[@class="news_textspan"]')[0]
            content_div = news_div.xpath('./div[@class="TRS_Editor"]')[0]
            # pubtime = source_div.xpath('./div[@class="ly"]/span[@id="time_tex"]/text()').extract_first('').strip()
            time_re = source_div.re(r'\d{2,4}年\d{1,2}月\d{1,2}日\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        title = ''.join(i.strip() for i in news_div.xpath('./h1/text()').extract())
        origin_name = source_div.xpath('./div[@class="news_textspan"]/div[1]/span[1]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
