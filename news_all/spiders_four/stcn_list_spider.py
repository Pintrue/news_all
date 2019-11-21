# -*- coding: utf-8 -*-
# @Time   : 2019/3/4 下午5:12
# @Author : NewmanZhou
# @Project : news_all
# @FileName: stcn_list_spider.py

import time
from scrapy.conf import settings
from copy import deepcopy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spiders_four.stcn_kx_spider import StcnKXSpipder


class StcnYWSpipder(StcnKXSpipder):
    name = 'stcn_yw_spider'

    # 证券时报 ==》 首页 ==》 快讯
    mystart_urls = {
        'http://news.stcn.com/': 496,  # '要闻列表'
        'http://news.stcn.com/guonei/': 497,  # '国内'
        'http://news.stcn.com/xwhw/': 498,  # '海外'
        'http://news.stcn.com/sdbd/': 499,  # '深度报道'
        'http://news.stcn.com/xwpl/': 500,  # '评论'
        'http://news.stcn.com/sbgc/': 501,  # '时报观察'
        'http://news.stcn.com/xwct/': 502,  # '创投'
        'http://news.stcn.com/renwu/': 503,  # '人物'
        # 股票
        'http://stock.stcn.com/': 504,  # '股市'
        'http://stock.stcn.com/xingu/index.shtml': 505,  # '新股'
        'http://stock.stcn.com/dapan/index.shtml': 507,  # '大盘'
        'http://stock.stcn.com/zhuli/index.shtml': 509,  # '主力'
        'http://stock.stcn.com/bankuai/index.shtml': 510,  # '板块'
        'http://kuaixun.stcn.com/list/kxyb.shtml': 511,  # '研报'

        # 公司
        'http://company.stcn.com/': 513,  # '公司'
        # 动态
        'http://www.stcn.com/list/scdt.shtml': 516,  # '动态' # 有两个娶不到时间 标题 发布者
        # 机构
        'http://finance.stcn.com/': 517,  # '机构'
    }

    # http://kuaixun.stcn.com/2019/0304/14900431.shtml
    rules = (Rule(LinkExtractor(allow='stcn.com/%s/.*?\d+.shtml' % time.strftime('%Y',time.localtime(time.time())), deny=('video', 'audio'),
                                restrict_xpaths='//div[@class="box_left"]/ul/li'),
                  callback='parse_item', follow=False),
             # Rule(LinkExtractor(  # allow='\d+.shtml', # 可以不写正则, 只用xpath找url
             #     restrict_xpaths='//div[@class="pagelist"]'),
             #     follow=True, process_request=isStartUrl_meta),  # todo 暂不翻页
             # 把翻页的request 优先级放最低，因为增量爬虫第二轮时，第2/3..页几乎没有新新闻
             )

    custom_settings = {
        # 'DEPTH_LIMIT': 6,
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % StcnKXSpipder.name,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }


class StcnZLSpipder(StcnKXSpipder):
    name = 'stcn_zl_spider'

    # 证券时报 ==》 首页 ==》 快讯
    mystart_urls = {
        # 专栏
        'http://space.stcn.com/': 514,  # '专栏'
    }

    # http://kuaixun.stcn.com/2019/0304/14900431.shtml
    rules = (Rule(LinkExtractor(allow='stcn.com/.*?\d+.s?htm', deny=('video', 'audio'),
                                restrict_xpaths='//div[@class="box_left2"]/div[@id="news_list2"]'),
                  callback='parse_item_all_2', follow=False),
             )
    custom_settings = {
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % StcnKXSpipder.name,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }


class StcnSJSpipder(StcnKXSpipder):
    name = 'stcn_sj_spider'

    # 证券时报 ==》 数据 ==》 数据
    mystart_urls = {
        # 数据
        'http://data.stcn.com/djsj/index.shtml': 512,  # '数据'
    }

    # http://kuaixun.stcn.com/2019/0304/14900431.shtml
    rules = (Rule(LinkExtractor(allow='stcn.com/.*?\d+.s?htm', deny=('video', 'audio'),
                                restrict_xpaths='//div[@class="box_left2"]/ul[@id="news_list2"]'),
                  callback='parse_item_all_3', follow=False),
             # Rule(LinkExtractor(allow=r'tcn.com/djsj/\d.shtml',
             #                    restrict_xpaths='//div[@class="pagelist"]/ul/li/a[text()="下一页"]'),
             #      follow=True, process_request=isStartUrl_meta),  # todo 暂不翻页
             )

    custom_settings = {
        # 'DEPTH_LIMIT': 6,
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % StcnKXSpipder.name,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }