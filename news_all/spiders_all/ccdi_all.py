# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider, otherurl_meta, js_meta


class CcdiAllSpider(NewsRCSpider):
    """中央纪委监察部网站"""
    name = 'ccid_all'
    mystart_urls = {
        'http://www.ccdi.gov.cn/ldhd/gcsy/': 2302, 'http://www.ccdi.gov.cn/ldhd/wbld/': 2303,
     'http://www.ccdi.gov.cn/scdc/zyyj/zjsc/': 2304, 'http://www.ccdi.gov.cn/scdc/zyyj/djcf/': 2305,
     'http://www.ccdi.gov.cn/scdc/sggb/zjsc/': 2306, 'http://www.ccdi.gov.cn/scdc/sggb/djcf/': 2307,
     'http://www.ccdi.gov.cn/lswh/lilun/': 2308, 'http://www.ccdi.gov.cn/lswh/renwu/': 2309,
     'http://www.ccdi.gov.cn/lswh/shijian/': 2310, 'http://www.ccdi.gov.cn/lswh/hwgc/': 2311,
     'http://www.ccdi.gov.cn/lswh/wenhua/mryz/': 2312,
    }

    # mystart_urls = {
    #     'http://www.ccdi.gov.cn/': 1,
    #     'http://www.ccdi.gov.cn/ldhd/gcsy/': 2,
    #     'http://www.ccdi.gov.cn/yaowen/': 3,
    #     'http://www.ccdi.gov.cn/scdc/': 4,
    #     'http://www.ccdi.gov.cn/scdc/zggb/zjsc/': 5,
    #     'http://www.ccdi.gov.cn/scdc/zggb/djcf/': 6,
    #     'http://www.ccdi.gov.cn/scdc/zyyj/zjsc/': 7,
    #     'http://www.ccdi.gov.cn/scdc/zyyj/djcf/': 8,
    #     'http://www.ccdi.gov.cn/scdc/sggb/zjsc/': 9,
    #     'http://www.ccdi.gov.cn/scdc/sggb/djcf/': 10,
    #     'http://www.ccdi.gov.cn/xsxc/': 11,
    #     'http://www.ccdi.gov.cn/special/jdbg3/index.html': 12,
    #     'http://www.12388.gov.cn/': 13,
    #     'http://www.ccdi.gov.cn/special/jdbg3/qb_bgt/fjbxgdwt_jdbg3/': 14,
    #     'http://www.ccdi.gov.cn/special/jdbg3/qb_bgt/sffbwt_jdbg3/': 15,
    #     'http://www.ccdi.gov.cn/special/jdbg3/zq_jdbg3/': 16,
    #     'http://www.ccdi.gov.cn/fgk/index': 17,
    #     'http://www.ccdi.gov.cn/shipin/zxft/': 18,
    #     'http://www.ccdi.gov.cn/shipin/sjddzgkk/': 19,
    #     'http://v.ccdi.gov.cn/kjxwlzty/MOON/index.shtml': 20,
    #     'http://www.ccdi.gov.cn/bwgsg/': 21,
    #     'http://www.ccdi.gov.cn/shipin/daxue/': 22,
    #     'http://www.ccdi.gov.cn/shipin/yuewei/': 23,
    #     'http://www.ccdi.gov.cn/shipin/ffsrt/': 24,
    #     'http://v.ccdi.gov.cn/special/qlzg5/shouye/index.shtml': 25,
    #     'http://www.ccdi.gov.cn/lswh/lilun/': 26,
    #     'http://www.ccdi.gov.cn/lswh/renwu/': 27,
    #     'http://www.ccdi.gov.cn/lswh/shijian/': 28,
    #     'http://www.ccdi.gov.cn/lswh/hwgc/': 29,
    #     'http://www.ccdi.gov.cn/lswh/wenhua/mryz/': 30,
    #     'http://v.ccdi.gov.cn/wszg/index.shtml': 31,
    #     'http://www.ccdi.gov.cn/toutiao/': 32,
    #     'http://www.ccdi.gov.cn/shudan/': 33,
    #     'http://www.ccdi.gov.cn/tjts/': 34,
    #     'http://www.ccdi.gov.cn/tjts/manhua/': 35,
    #     'http://www.ccdi.gov.cn/tjts/ytdd/': 36,
    #     'http://www.ccdi.gov.cn/tjts/jingtou/': 37,
    #     'http://www.ccdi.gov.cn/shipin/jsdwj/': 38,
    #     'http://people.ccdi.gov.cn/': 39,
    #     'http://www.ccdi.gov.cn/special/sjjzyjw4cqh/index.html': 40,
    #     'http://www.ccdi.gov.cn/xbl/index_1760.html': 41,
    #     'http://www.ccdi.gov.cn/special/zxzzzt/dt_zxzzzt/': 42,
    #     'http://www.ccdi.gov.cn/special/bwzp/wqhg_bwzp/': 43,
    #     'http://www.ccdi.gov.cn/special/jwsjtth/wqhg_jwsjtth/': 44,
    #     'http://www.ccdi.gov.cn/special/sjjzyjw4cqh/yw_sjj4cqh/': 45,
    # }
    #
    # http://www.ccdi.gov.cn/scdc/sggb/zjsc/201904/t20190415_192308.html
    # http://www.ccdi.gov.cn/xsxc/201904/t20190410_192003.html
    # http://www.ccdi.gov.cn/lswh/lilun/201903/t20190325_191086.html
    rules = (
        Rule(LinkExtractor(allow=r'ccdi.gov.cn.*?/%s/t\d{8}_\d{5,}.html' % datetime.today().strftime('%Y%m'),
                           ),
             callback='parse_item',
             # process_request=js_meta,
             follow=False),
        Rule(LinkExtractor(allow=r'ccdi.gov.cn.*?\w{5,}.html',  deny=(r'/201[0-8]', r'/2019/?(?:0[1-9]|10)'),
                           ),
             process_request=otherurl_meta,
             follow=False),
    )

    downloader = deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    # downloader['news_all.middlewares.PhantomJSMiddleware'] = 540

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
        # 'DOWNLOADER_MIDDLEWARES': downloader
    }

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('————')[0]
            pubtime = xp(r'//div[@class="daty_con"]/em[@class="e e2"]/text()').extract_first('').replace("发布时间：", "").strip()
            
            

            cv = xp('//div[@class="content"]/div[@class="TRS_Editor"]')[0]
            content, media, video, cover = self.content_clean(cv)
            origin_name = xp(r'//div[@class="daty_con"]/em[@class="e e1"]/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media,
        )
