# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class QizhiwangAllSpider(NewsRCSpider):
    """旗帜网"""
    name = 'qizhiwang_all'
    mystart_urls = {

        'http://www.qizhiwang.org.cn/GB/422352/422364/index.html': 2318,
        'http://www.qizhiwang.org.cn/GB/422352/422365/index.html': 2319,
        'http://www.qizhiwang.org.cn/GB/422352/422366/index.html': 2320,
        'http://www.qizhiwang.org.cn/GB/422353/422368/index.html': 2321,
        'http://www.qizhiwang.org.cn/GB/422353/422369/index.html': 2322,
        'http://www.qizhiwang.org.cn/GB/422353/422371/index.html': 2323,
        'http://www.qizhiwang.org.cn/GB/422354/422372/index.html': 2324,
        'http://www.qizhiwang.org.cn/GB/422354/422373/index.html': 2325,
        'http://www.qizhiwang.org.cn/GB/422354/422374/index.html': 2326,
        'http://www.qizhiwang.org.cn/GB/422355/422375/index.html': 2327,
        'http://www.qizhiwang.org.cn/GB/422355/422376/index.html': 2328,
        'http://www.qizhiwang.org.cn/GB/422355/422377/index.html': 2329,
        'http://www.qizhiwang.org.cn/GB/422355/422378/index.html': 2330,
        'http://www.qizhiwang.org.cn/GB/422356/422379/index.html': 2331,
        'http://www.qizhiwang.org.cn/GB/422357/422382/index.html': 2332,
        'http://www.qizhiwang.org.cn/GB/422357/422383/index.html': 2333,
        'http://www.qizhiwang.org.cn/GB/422357/422384/index.html': 2334,
        'http://www.qizhiwang.org.cn/GB/422358/422386/index.html': 2335,
        'http://www.qizhiwang.org.cn/GB/422358/422387/index.html': 2336,
        'http://www.qizhiwang.org.cn/GB/422358/422388/index.html': 2337,
        'http://www.qizhiwang.org.cn/GB/422359/422391/index.html': 2338,
        'http://www.qizhiwang.org.cn/GB/422359/422392/index.html': 2339,
        'http://www.qizhiwang.org.cn/GB/422359/422393/index.html': 2340,
        'http://www.qizhiwang.org.cn/GB/422359/422394/index.html': 2341,
        'http://www.qizhiwang.org.cn/GB/422360/422395/index.html': 2342,
        'http://www.qizhiwang.org.cn/GB/422360/422396/index.html': 2343

    }

    # http://www.qizhiwang.org.cn/n1/2019/0428/c422351-31054338.html

    rules = (
        Rule(LinkExtractor(allow=(r'qizhiwang.org.cn/.*?/%s/.*?\d+.html'%datetime.today().year), ),
                           callback='parse_item', follow=False),

    )
    # http://www.qizhiwang.org.cn/n1/2019/0428/c422351-31054338.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('.//h1/text()')[0].extract()
            source_div = xp('.//div[@class="ptime"]')[0]
            content_div = xp('.//div[@class="text_con w1000 clearfix"]')[0]
            time_re = source_div.re(r'\d{2,4}年\d{1,2}月\d{1,2}日\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            origin_name = source_div.xpath('./em/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
