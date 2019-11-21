# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


class YidaiyiluSpider(NewsRCSpider):
    '''中国一带一路网'''
    name = 'yidaiyilu'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10149": 7577,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10002": 7578,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10005": 7579,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10003": 7580,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10004": 7581,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10122": 7582,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10358": 7583,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10359": 7584,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10150": 7585,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10006": 7586,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10008": 7587,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10009": 7588,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10010": 7589,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10011": 7590,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10029": 7591,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10046": 7592,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10030": 7593,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?tm_id=96": 7594,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10148": 7595,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10025": 7596,
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10026": 7597,
    }
    rules = (
        # https://www.yidaiyilu.gov.cn/xwzx/xgcdt/94867.htm
        Rule(LinkExtractor(allow=(r'yidaiyilu.gov.cn/[a-z]+/[a-z]+/\d+\.htm',),
                           ), callback='parse_item',
             follow=False,process_request=js_meta),
    )
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='main_content_title']/text()").extract_first()
            content_div = xp("//div[@class='info_content']")[0]

            source = xp('//html/head/meta[@name="source"]/@content')[0].extract()
            pubtime = xp('//html/head/meta[@name="others"]/@content')[0].extract()
        except:
            return self.produce_debugitem(response, "xpath error")
        # 过滤视频


        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=source,

            content=content,
            media=media
        )

