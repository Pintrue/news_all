# -*- coding: utf-8 -*-

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.spider_models import NewsRCSpider, js_meta


class BaiduSpider(NewsRCSpider):
    name = 'baidu'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            # 'news_all.middlewares.ProxyRdMiddleware': 100
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        'http://cpu.baidu.com/block/wap/268662363/2688': 10086,  # 百度-体育-全部采集
        'http://cpu.baidu.com/block/wap/268662363/2695': 10092,  # 百度-健康
        'http://cpu.baidu.com/block/wap/268662363/2690': 10088,  # 百度-军事
        'http://cpu.baidu.com/block/wap/268662363/2691': 10089,  # 百度-娱乐
        'http://cpu.baidu.com/block/wap/268662363/2689': 10087,  # 百度-社会
        'http://cpu.baidu.com/block/wap/268662363/2694': 10091,  # 百度-科技
        'http://cpu.baidu.com/block/wap/268662363/2693': 10090,  # 百度-财经

    }
    # https://cpu.baidu.com/wap/1022/268662363/detail/30852779190834798/news?blockId=2688&from=block
    # https://cpu.baidu.com/wap/1022/268662363/detail/30782492185253444/news?blockId=2694&from=block
    # https://cpu.baidu.com/wap/1022/268662363/detail/30900472655173222/news?blockId=2690
    rules = (
        Rule(LinkExtractor(allow=(r'cpu.baidu.com/.*?/detail/\d+/news'), ),  # .*?from=block
             callback='parse_item', follow=False, process_request=js_meta
             ),
    )

    # custom_settings = {
    #     'DEPTH_LIMIT': 3,  # 翻页需要设置深度为0 或者 >1
    #     'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    # }

    def parse_item(self, response):
        try:
            title = response.xpath('.//h1').extract()[0]
            content_div = response.xpath('.//article[@class="article container"]')[0]
            source_div = response.xpath('.//div[@class="page-info container splitter"]')[0]
            pubtime = source_div.re(r'\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}')[0]
            origin_name = response.xpath('.//em[@class="source_name"]/text()').extract_first('')
            content, media, *_ = self.content_clean(content_div)
        except BaseException:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(response=response,
                                 title=title,
                                 pubtime=pubtime,
                                 origin_name=origin_name,
                                 content=content,
                                 media=media,
                                 )