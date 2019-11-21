# -*- coding: utf-8 -*-
from copy import deepcopy
from scrapy.conf import settings
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.spider_models import NewsRCSpider, otherurl_meta


class china5eAllSpider(NewsRCSpider):
    """中国能源报"""
    name = 'china5e_all'
    sleep_time = 10
    mystart_urls = {
                    'https://www.china5e.com/power/coal-fire/': 6285,  # 火电
                    'https://www.china5e.com/coal/coal-mining/': 6286,  # 采煤
                    'https://www.china5e.com/new-energy/others/': 6287,  # 其他
                    'https://www.china5e.com/energy-conservation/environmental-protection/': 6288,  # 环境保护
                    'https://www.china5e.com/new-energy/solar-power/': 6289,  # 太阳能
                    'https://www.china5e.com/power/power-gird/': 6290,  # 输配电
                    'https://www.china5e.com/new-energy/general/': 6291,  # 综合
                    'https://www.china5e.com/power/hydro-power/': 6292,  # 水电
                    'https://www.china5e.com/energy-economy/macroeconomy/': 6293,  # 宏观经济
                    'https://www.china5e.com/oil-gas/general/': 6294,  # 综合
                    'https://www.china5e.com/energy-economy/stock/': 6295,  # 金融股市
                    'https://www.china5e.com/oil-gas/shale-gas-and-oil/': 6296,  # 页岩油气
    }

    # https://www.china5e.com/news/news-1054977-1.html
    rules = (
        Rule(LinkExtractor(allow=(r'china5e.com/news/news-.*?\d+.html',)), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'china5e.com.*?\w+.html',)), process_request=otherurl_meta, follow=False),
    )
    
    dd = deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES'))
    dd['news_all.middlewares.ProxyRdMiddleware'] = 100
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': dd,
        'RETRY_TIMES': 5,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1
    }
   
    def parse_item(self, response):
        try:
            head_div = response.xpath('.//div[@id="articleBox"]/div[@class="showtitle"]')[0]
            content_div = response.xpath('.//div[@id="articleBox"]/div[@id="showcontent"]/div')[0]
            source_div = response.xpath('.//div[@class="showtitle"]/div[@class="showtitinfo"]/text()').extract()
            time_re = head_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
        except:
            return self.produce_debugitem(response, "xpath error")


        title = head_div.xpath('.//h1/text()').extract_first('').strip()
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=source_div[1] if len(source_div)>1 else "",

            content=content,
            media=media
        )