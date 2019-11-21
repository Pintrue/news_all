# -*- coding: utf-8 -*-
# @Time   : 2019/3/4 下午4:25
# @Author : NewmanZhou
# @Project : news_all
# @FileName: stcn_kx_spider.py


from copy import deepcopy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spiders_four.stcn_kx_spider import StcnKXSpipder
from news_all.spider_models import isStartUrl_meta
from datetime import datetime
from scrapy.conf import settings


class StcnAll(StcnKXSpipder):
    name = 'stcn_all'

    # 证券时报 ==》 补充全站采集
    mystart_urls = {
        'http://data.stcn.com/zijinliuxiang/': 1790,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://data.stcn.com/kandianshuju/': 1792,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://data.stcn.com/djsj/': 1793,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://data.stcn.com/': 1794,  # 数据频道-证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://data.stcn.com/djsj/index.shtml': 1794,  # 手动增加的
        'http://news.stcn.com/dwq/index.shtml': 1795,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://space.stcn.com/zsx': 1796,  # 专栏频道_证券时报网
        'http://company.stcn.com/gsdt/': 1797,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://news.stcn.com': 1798,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://news.stcn.com/roll/': 1800,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://stock.stcn.com/zhuli/': 1801,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://stock.stcn.com/xingu/': 1803,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://stock.stcn.com/bankuai/': 1804,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://space.stcn.com/mumu': 1805,  # 专栏频道_证券时报网
        'http://space.stcn.com/zsx/': 1806,  # 专栏频道_证券时报网
        'http://stock.stcn.com/dapan/': 1808,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://data.stcn.com/list/jqr.shtml': 1809,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://news.stcn.com/xwyw/': 1810,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://kuaixun.stcn.com/yb/trade/': 1811,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://finance.stcn.com/quanshang/': 1812,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://kuaixun.stcn.com/company/internal/': 1813,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://kuaixun.stcn.com/': 1815,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
        'http://kuaixun.stcn.com/list/kxgs.shtml': 1817,  # 证券时报网-证券时报官方网站，创业板指定信息披露平台
    }

    rules = (
        # http://data.stcn.com/2019/0404/14984734.shtml
        # http://news.stcn.com/2019/0408/14988367.shtml
        Rule(LinkExtractor(allow=r'stcn.com/%s/\d{4}/\d{6,}.shtml' % datetime.today().year, deny=('video', 'audio'),
                                ),
             callback='parse_item',
             follow=False),
        # http://kuaixun.stcn.com/index_2.shtml
        Rule(LinkExtractor(allow=r'stcn.com/.*?\d+.shtml', restrict_xpaths=r'//div[contains(@class,"pagelist")]//a[text()="下一页" or @class="next"]'
                        ),
          follow=True, process_request=isStartUrl_meta),
             )

    custom_settings = {
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % StcnKXSpipder.name,
        'DEPTH_LIMIT': 3,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }