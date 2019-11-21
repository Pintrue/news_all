#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 17:45
# @Author  : wjq
# @File    : china.py
import json
from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from news_all.tools.time_translater import Pubtime


class ChinaSpider(NewsRCSpider):
    """中国网"""
    name = 'china'
    from scrapy.conf import settings
    from copy import deepcopy
    custom_settings = {
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    # mystart_urls = {
    #     'http://travel.china.com.cn/': 18249,  # 中国网-旅游-左上角
    #
    #     'http://ent.china.com.cn/': 18254,  # 中国网-娱乐
    #     'http://cppcc.china.com.cn/': 18243,  # 中国网-政协-焦点图右侧要闻
    #     'http://cul.china.com.cn/': 18250,  # 中国网-文化
    #     'http://news.china.com.cn/world/node_7208705.htm': 18101,  # 中国网-新闻-国际外交
    #     'http://ocean.china.com.cn/node_7198590.htm': 18246,  # 中国网-海洋-全部
    #     'http://tech.china.com.cn/internet/jjds/': 18121,  # 中国网-科技
    #     'http://art.china.cn/': 18251,  # 中国网-艺术-中部列表
    #
    #     'http://music.china.com.cn/': 18253,  # 中国网-音乐-全部抓取，部分封面未抓取
    #     'http://zxx.edu.china.com.cn/node_544773.htm': 1200364,  # 中国网教育-中小学-左侧列表
    #     'http://news.china.com.cn/world/node_7208704.htm': 18100,  # 中国网-新闻-国际独家-左侧
    # }

    mystart_urls = {
        'http://news.china.com.cn/world/node_7208703.htm': 6636,
        'http://news.china.com.cn/world/node_7208704.htm': 6637,
        'http://news.china.com.cn/world/node_7239403.htm': 6638,
        'http://news.china.com.cn/node_8005004.htm': 6639,
        'http://news.china.com.cn/node_8006454.htm': 6640,
        'http://military.china.com.cn/node_7252587.htm': 6641,
        'http://military.china.com.cn/node_7252592.htm': 6642,
        'http://military.china.com.cn/node_7252588.htm': 6643,
        'http://military.china.com.cn/node_7252593.htm': 6644,
        'http://military.china.com.cn/node_7252626.htm': 6645,
        'http://military.china.com.cn/node_7252590.htm': 6646,
        'http://legal.china.com.cn/': 6647,
        'http://legal.china.com.cn/node_8014000.html': 6648,
        'http://cppcc.china.com.cn/node_7185257.htm': 6649,
        'http://cppcc.china.com.cn/node_7227325.htm': 6650,
        'http://cppcc.china.com.cn/node_7185259.htm': 6651,
        'http://cppcc.china.com.cn/node_7185260.htm': 6652,
        'http://cppcc.china.com.cn/node_7185262.htm': 6653,
        'http://cppcc.china.com.cn/node_7185266.htm': 6654,
        'http://cppcc.china.com.cn/node_7185267.htm': 6655,
        'http://cppcc.china.com.cn/node_7241958.htm': 6656,
        'http://cppcc.china.com.cn/node_7185271.htm': 6657,
        'http://cppcc.china.com.cn/node_7185268.htm': 6658,
        'http://cppcc.china.com.cn/node_7185285.htm': 6659,
        'http://cppcc.china.com.cn/node_7185287.htm': 6660,
        'http://cppcc.china.com.cn/node_7185263.htm': 6661,
        'http://cppcc.china.com.cn/node_7241959.htm': 6662,
        'http://cppcc.china.com.cn/node_7185303.htm': 6663,
        'http://cppcc.china.com.cn/node_7185304.htm': 6664,
        'http://cppcc.china.com.cn/node_7185305.htm': 6665,
        'http://cppcc.china.com.cn/node_7185306.htm': 6666,
        'http://cppcc.china.com.cn/node_7185307.htm': 6667,
        'http://cppcc.china.com.cn/node_7185308.htm': 6668,
        'http://cppcc.china.com.cn/node_7185309.htm': 6669,
        'http://cppcc.china.com.cn/node_7185310.htm': 6670,
        'http://cppcc.china.com.cn/node_7185311.htm': 6671,
        'http://cppcc.china.com.cn/node_7185312.htm': 6672,
        'http://cppcc.china.com.cn/node_7185313.htm': 6673,
        'http://cppcc.china.com.cn/node_7185315.htm': 6674,
        'http://cppcc.china.com.cn/node_7185316.htm': 6675,
        'http://cppcc.china.com.cn/node_7185317.htm': 6676,
        'http://cppcc.china.com.cn/node_7185318.htm': 6677,
        'http://cppcc.china.com.cn/node_7185319.htm': 6678,
        'http://cppcc.china.com.cn/node_7185320.htm': 6679,
        'http://cppcc.china.com.cn/node_7185321.htm': 6680,
        'http://cppcc.china.com.cn/node_7185322.htm': 6681,
        'http://cppcc.china.com.cn/node_7185323.htm': 6682,
        'http://cppcc.china.com.cn/node_7185324.htm': 6683,
        'http://cppcc.china.com.cn/node_7185325.htm': 6684,
        'http://cppcc.china.com.cn/node_7185326.htm': 6685,
        'http://cppcc.china.com.cn/node_7185327.htm': 6686,
        'http://cppcc.china.com.cn/node_7185328.htm': 6687,
        'http://cppcc.china.com.cn/node_7185329.htm': 6688,
        'http://cppcc.china.com.cn/node_7185330.htm': 6689,
        'http://cppcc.china.com.cn/node_7185331.htm': 6690,
        'http://cppcc.china.com.cn/node_7185332.htm': 6691,
        'http://finance.china.com.cn/news/live.shtml': 6692,
        'http://finance.china.com.cn/my.shtml': 6693,
        'http://finance.china.com.cn/news/index.shtml': 6694,
        'http://finance.china.com.cn/stock/zqyw/index.shtml': 6695,
        'http://finance.china.com.cn/stock/ssgs/index.shtml': 6696,
        'http://finance.china.com.cn/stock/dp/index.shtml': 6697,
        'http://finance.china.com.cn/stock/qsdt/index.shtml': 6698,
        'http://ipo.china.com.cn/live.shtml': 6699,
        'http://ipo.china.com.cn/xgyw/index.shtml': 6700,
        'http://finance.china.com.cn/stock/hkstock/index.shtml': 6701,
        'http://finance.china.com.cn/stock/usstock/index.shtml': 6702,
        'http://finance.china.com.cn/stock/xsb/index.shtml': 6703,
        'http://finance.china.com.cn/industry/my.shtml': 6704,
        'http://business.china.com.cn/node_1002157.html': 6705,
        'http://business.china.com.cn/node_1002158.html': 6706,
        'http://business.china.com.cn/node_1002159.html': 6707,
        'http://business.china.com.cn/node_1002162.html': 6708,
        'http://business.china.com.cn/node_1002163.html': 6709,
        'http://business.china.com.cn/node_1002164.html': 6710,
        'http://business.china.com.cn/node_1002165.html': 6711,
        'http://business.china.com.cn/node_1002167.html': 6712,
        'http://business.china.com.cn/node_1002168.html': 6713,
        'http://business.china.com.cn/node_1002169.html': 6714,
        'http://business.china.com.cn/node_1002170.html': 6715,
        'http://iot.china.com.cn/node_1003303.html': 6716,
        'http://iot.china.com.cn/node_1003304.html': 6717,
        'http://iot.china.com.cn/node_1003305.html': 6718,
        'http://tc.china.com.cn/node_535738.html': 6719,
        'http://tc.china.com.cn/node_535608.html': 6720,
        'http://tc.china.com.cn/node_535615.html': 6721,
        'http://tc.china.com.cn/node_535607.html': 6722,
        'http://tc.china.com.cn/node_535602.html': 6723,
        'http://tc.china.com.cn/node_535606.html': 6724,
        'http://tc.china.com.cn/node_535612.html': 6725,
        'http://tc.china.com.cn/node_535605.html': 6726,
        'http://tc.china.com.cn/node_1005641.html': 6727,
        'http://tc.china.com.cn/node_535603.html': 6728,
        'http://chuangkr.china.com.cn/column/venture-capital': 6729,
        'http://chuangkr.china.com.cn/column/business': 6730,
        'http://chuangkr.china.com.cn/column/technology': 6731,
        'http://chuangkr.china.com.cn/column/workplace': 6732,
        'http://chuangkr.china.com.cn/column/innovation': 6733,
        'http://chuangkr.china.com.cn/column/star-enterprise': 6734,
        'http://chuangkr.china.com.cn/column/activity': 6735,
        'http://chuangkr.china.com.cn/column/newsflash': 6736,
        'http://zw.china.com.cn/node_8012270.html': 6737,
        'http://zw.china.com.cn/node_8012272.html': 6738,
        'http://zw.china.com.cn/node_8012271.html': 6739,
        'http://zw.china.com.cn/node_8012276.html': 6740,
        'http://aj.china.com.cn/channels/35.html': 6741,
        'http://aj.china.com.cn/channels/484.html': 6742,
        'http://aj.china.com.cn/channels/482.html': 6743,
        'http://aj.china.com.cn/channels/480.html': 6744,
        'http://aj.china.com.cn/channels/485.html': 6745,
        'http://aj.china.com.cn/channels/487.html': 6746,
        'http://aj.china.com.cn/channels/111.html': 6747,
        'http://aj.china.com.cn/channels/49.html': 6748,
        'http://aj.china.com.cn/channels/57.html': 6749,
        'http://union.china.com.cn/jdnews/node_522763.html': 6750,
        'http://union.china.com.cn/csdt/node_522776.html': 6751,
        'http://union.china.com.cn/kx/node_522771.html': 6752,
        'http://union.china.com.cn/cmdt/node_522782.html': 6753,
        'http://union.china.com.cn/fashion/index.htm': 6754,
        'http://union.china.com.cn/node_542613.html': 6755,
        'http://travel.china.com.cn/node_8011252.html': 6756,
        'http://travel.china.com.cn/node_8011253.html': 6757,
        'http://travel.china.com.cn/node_8011254.html': 6758,
        'http://travel.china.com.cn/node_8011259.html': 6759,
        'http://travel.china.com.cn/node_7237677.html': 6760,
        'http://travel.china.com.cn/node_7237678.html': 6761,
        'http://travel.china.com.cn/node_7085313.html': 6762,
        'http://cul.china.com.cn/node_519743.htm': 6763,
        'http://cul.china.com.cn/renwu/node_519723.htm': 6764,
        'http://cul.china.com.cn/chuangyi/node_523396.htm': 6765,
        'http://cul.china.com.cn/wenbao/index.html': 6766,
        'http://cul.china.com.cn/xijua/node_519718.htm': 6767,
        'http://cul.china.com.cn/node_519757.htm': 6768,
        'http://cul.china.com.cn/minsu/node_519717.htm': 6769,
        'http://cul.china.com.cn/zhenbao/node_519715.htm': 6770,
        'http://cul.china.com.cn/chuban/': 6771,
        'http://cul.china.com.cn/chanye/': 6772,
        'http://cul.china.com.cn/photo/node_519694.htm': 6773,
        'http://life.china.com.cn/node_1004367.html': 6774,
        'http://life.china.com.cn/node_1004370.html': 6775,
        'http://life.china.com.cn/node_1004371.html': 6776,
        'http://life.china.com.cn/node_1004372.html': 6777,
        'http://life.china.com.cn/node_1004373.html': 6778,
        'http://life.china.com.cn/node_1004375.html': 6779,
        'http://life.china.com.cn/node_1004376.html': 6780,
        'http://life.china.com.cn/node_1004381.html': 6781,
        'http://life.china.com.cn/node_1004382.html': 6782,
        'http://life.china.com.cn/node_1004384.html': 6783,
        'http://life.china.com.cn/node_1004385.html': 6784,
        'http://life.china.com.cn/node_1004386.html': 6785,
        'http://health.china.com.cn/node_542831.htm': 6786,
        'http://health.china.com.cn/node_542852.htm': 6787,
        'http://health.china.com.cn/node_542853.htm': 6788,
        'http://health.china.com.cn/node_1000598.html': 6789,
        'http://health.china.com.cn/node_1000605.html': 6790,
        'http://health.china.com.cn/node_542867.htm': 6791,
        'http://health.china.com.cn/node_546366.htm': 6792,
        'http://health.china.com.cn/node_549783.htm': 6793,
        'http://v.china.com.cn/node_7251788.htm': 6794,
        'http://v.china.com.cn/news/node_7251731.htm': 6795,
        'http://v.china.com.cn/finance/node_7251730.htm': 6796,
        'http://v.china.com.cn/sports/node_7251729.htm': 6797,
        'http://v.china.com.cn/ent/node_7251922.htm': 6798,
        'http://v.china.com.cn/ent/node_7251923.htm': 6799,
        'http://v.china.com.cn/ent/node_7251921.htm': 6800,
        'http://v.china.com.cn/node_7251725.htm': 6801,
        'http://fangtan.china.com.cn/node_7249521.htm': 6802,
        'http://fangtan.china.com.cn/node_7249520.htm': 6803,
        'http://fangtan.china.com.cn/node_7249519.htm': 6804,
        'http://fangtan.china.com.cn/node_7249518.htm': 6805,
        'http://fangtan.china.com.cn/node_7249517.htm': 6806,
        'http://photo.china.com.cn/node_7248031.htm': 6807,
        'http://photo.china.com.cn/node_7248030.htm': 6808,
        'http://photo.china.com.cn/node_7250380.htm': 6809,
        'http://photo.china.com.cn/node_7248040.htm': 6810,
        'http://photo.china.com.cn/foto/node_7185692.htm': 6811,
        'http://photo.china.com.cn/foto/node_7185699.htm': 6812,
        'http://www.china.com.cn/zhibo/node_8009517.htm': 6813,
        'http://www.china.com.cn/zhibo/node_7243162.htm': 6814,
        'http://www.china.com.cn/zhibo/node_8006611.htm': 6815,
        'http://www.china.com.cn/zhibo/node_7243164.htm': 6816,
        'http://www.china.com.cn/zhibo/node_7243172.htm': 6817,
        'http://www.china.com.cn/zhibo/node_7243165.htm': 6818,
        'http://www.china.com.cn/zhibo/node_7243184.htm': 6819,
        'http://www.china.com.cn/zhibo/node_7243168.htm': 6820,
        'http://caifang.china.com.cn/node_550480.htm': 6821,
        'http://caifang.china.com.cn/node_550482.htm': 6822,
        'http://caifang.china.com.cn/node_550483.htm': 6823,
        'http://ocean.china.com.cn/node_7198590.htm': 6824,
        'http://ocean.china.com.cn/node_7198592.htm': 6825,
        'http://ocean.china.com.cn/node_7198593.htm': 6826,
        'http://ocean.china.com.cn/node_7198596.htm': 6827,
        'http://ocean.china.com.cn/node_7198597.htm': 6828,
        'http://ocean.china.com.cn/node_7198598.htm': 6829,
        'http://ocean.china.com.cn/node_7198599.htm': 6830,
        'http://ocean.china.com.cn/node_7198600.htm': 6831,
        'http://ocean.china.com.cn/node_7198601.htm': 6832,
        'http://ocean.china.com.cn/node_7198603.htm': 6833,
        'http://ocean.china.com.cn/node_7198604.htm': 6834,
        'http://ocean.china.com.cn/node_7208423.htm': 6835,
        'http://ocean.china.com.cn/node_7208421.htm': 6836,
        'http://ocean.china.com.cn/node_7198614.htm': 6837,
        'http://ocean.china.com.cn/node_7198615.htm': 6838,
        'http://ocean.china.com.cn/node_7198616.htm': 6839,
        'http://ocean.china.com.cn/node_7198617.htm': 6840,
        'http://sczg.china.com.cn/node_551322.htm': 6841,
        'http://sczg.china.com.cn/node_551324.htm': 6842,
        'http://sczg.china.com.cn/node_551327.htm': 6843,
        'http://sczg.china.com.cn/node_551328.htm': 6844,
        'http://sczg.china.com.cn/node_551329.htm': 6845,
        'http://sczg.china.com.cn/node_551337.htm': 6846,
        'http://stzg.china.com.cn/node_1001033.htm': 6847,
        'http://stzg.china.com.cn/node_1001035.htm': 6848,
        'http://stzg.china.com.cn/node_1001039.htm': 6849,
        'http://stzg.china.com.cn/node_1001040.htm': 6850,
        'http://stzg.china.com.cn/node_1001041.htm': 6851,
        'http://stzg.china.com.cn/node_1001042.htm': 6852,
        'http://stzg.china.com.cn/node_1001047.htm': 6853,
        'http://stzg.china.com.cn/node_1001048.htm': 6854,
        'http://stzg.china.com.cn/node_1001049.htm': 6855,
        'http://stzg.china.com.cn/node_1001050.htm': 6856,
        'http://stzg.china.com.cn/node_1001034.htm': 6857,
        'http://stzg.china.com.cn/node_1001043.htm': 6858,
        'http://stzg.china.com.cn/node_1001045.htm': 6859,
        'http://stzg.china.com.cn/node_1001046.htm': 6860,
        'http://stzg.china.com.cn/node_1001036.htm': 6861,
        'http://stzg.china.com.cn/node_1001051.htm': 6862,
        'http://stzg.china.com.cn/node_1001052.htm': 6863,
        'http://stzg.china.com.cn/node_1001053.htm': 6864,
        'http://stzg.china.com.cn/node_1001054.htm': 6865,
        'http://stzg.china.com.cn/node_1001037.htm': 6866,
        'http://stzg.china.com.cn/node_1001055.htm': 6867,
        'http://stzg.china.com.cn/node_1001056.htm': 6868,
        'http://stzg.china.com.cn/node_1001057.htm': 6869,
        'http://stzg.china.com.cn/node_1001058.htm': 6870,
        'http://stzg.china.com.cn/node_1001038.htm': 6871,
        'http://stzg.china.com.cn/node_1001059.htm': 6872,
        'http://stzg.china.com.cn/node_1001060.htm': 6873,
        'http://stzg.china.com.cn/node_1001061.htm': 6874,
        'http://stzg.china.com.cn/node_1001062.htm': 6875,
        'http://grassland.china.com.cn/node_1002588.html': 6876,
        'http://grassland.china.com.cn/node_1002590.html': 6877,
        'http://grassland.china.com.cn/node_1002594.html': 6878,
        'http://grassland.china.com.cn/node_1002595.html': 6879,
        'http://sl.china.com.cn/yaowen/': 6880,
        'http://sl.china.com.cn/chengshi/': 6881,
        'http://sl.china.com.cn/mzscgc/': 6882,
        'http://sl.china.com.cn/kaifaqu/': 6883,
        'http://sl.china.com.cn/dawanqu/': 6884,
        'http://sl.china.com.cn/wenhua/': 6885,
        'http://sl.china.com.cn/lvyou/': 6886,
        'http://sl.china.com.cn/jiankang/': 6887,
        'http://sl.china.com.cn/fupin/': 6888,
        'http://sl.china.com.cn/zhengce/': 6889,
        'http://sl.china.com.cn/guandian/': 6890,
        'http://sl.china.com.cn/jiaoliuhezuo/': 6891,
        'http://sl.china.com.cn/yuanchuang/': 6892,
        'http://sl.china.com.cn/shipin/': 6893,
        'http://food.china.com.cn/node_8003189.htm': 6894,
        'http://food.china.com.cn/node_8003269.htm': 6895,
        'http://food.china.com.cn/node_8003270.htm': 6896,
        'http://food.china.com.cn/node_8003199.htm': 6897,
        'http://food.china.com.cn/node_8003197.htm': 6898,
        'http://food.china.com.cn/node_8003198.htm': 6899,
        'http://food.china.com.cn/node_8003271.htm': 6900,
        'http://food.china.com.cn/node_8003194.htm': 6901,
        'http://food.china.com.cn/node_8003192.htm': 6902,
        'http://med.china.com.cn/list/1026': 6903,
        'http://med.china.com.cn/list/1013': 6904,
        'http://med.china.com.cn/list/1014': 6905,
        'http://med.china.com.cn/list/1023': 6906,
        'http://med.china.com.cn/list/1016': 6907,
        'http://med.china.com.cn/list/1015': 6908,
        'http://med.china.com.cn/list/1017': 6909,
        'http://med.china.com.cn/list/1018': 6910,
        'http://med.china.com.cn/list/3': 6911,
        'http://med.china.com.cn/list/1019': 6912,
        'http://med.china.com.cn/list/1020': 6913,
        'http://med.china.com.cn/list/1021': 6914,
        'http://med.china.com.cn/list/1022': 6915,
        'http://med.china.com.cn/list/1029': 6916,
        'http://med.china.com.cn/list/1030': 6917,
        'http://med.china.com.cn/list/612': 6918,
        'http://canjiren.china.com.cn/node_1000951.html': 6919,
        'http://canjiren.china.com.cn/node_1000953.html': 6920,
        'http://canjiren.china.com.cn/node_1000954.html': 6921,
        'http://canjiren.china.com.cn/node_1000955.html': 6922,
    }

    deny_list = [r'/201[0-8]', r'/2019(?:0[1-9]|10)\d{2}/', r'/2019-(?:0[1-9]|10)',
                 r'/2019_0[1-9]', r'/200[0-9]', r'/node_\d+(?:_\d+)*.htm',
                 r'/index\.s?html?', r'/guanyuwomen.htm', r'/fuwu/',
                 r'peoplechina.com.cn',
                 r'http://news.china.com.cn/txt/'
                 ]

    rules = (
        # http://cppcc.china.com.cn/2019-06/19/content_74898361.htm
        Rule(LinkExtractor(allow=r'cppcc.china.com.cn/%s/\d{2}/content_\d+.htm' % datetime.today().strftime('%Y-%m'),
                           deny=deny_list
                           ),
             callback='parse_item_2', follow=False),
        # http://travel.china.com.cn/txt/2019-06/19/content_74898616.html
        Rule(LinkExtractor(
            allow=(r'travel.china.com.cn/txt/%s/\d{2}/content_\d+.htm' % datetime.today().strftime('%Y-%m'),),
            deny=deny_list
            ),
            callback='parse_item_5', follow=False),
        # http://news.china.com.cn/txt/2019-11/11/content_75395242.htm
        Rule(LinkExtractor(
            allow=r'news.china.com.cn/txt/%s/\d{2}/content_\d+.htm' % datetime.today().strftime('%Y-%m'),
            deny=deny_list
            ),
            callback='parse_item_6', follow=False),
        # http://ent.china.com.cn/2019-06/19/content_74898674.htm
        # http://cul.china.com.cn/2019-06/18/content_40491710.htm
        # http://news.china.com.cn/txt/2019-05/24/content_74819454.htm
        # http://art.china.cn/txt/2019-06/18/content_40790794.shtml
        # http://ocean.china.com.cn/2019-06/19/content_74899482.htm
        # http://music.china.com.cn/2019-06/19/content_40791234.htm
        # http://zxx.edu.china.com.cn/2019-05/21/content_40757746.htm
        Rule(LinkExtractor(allow=(r'china.com.cn.*?/%s/\d{2}/content_\d+.s?htm' % datetime.today().strftime('%Y-%m'),
                                  r'china.com.cn.*?/%s/\d{2}/content_\d+_\d+\.htm' % datetime.today().strftime('%Y-%m'),),
                           deny=deny_list
                           ),
             callback='parse_item', follow=False),
        
        # http://cul.china.com.cn/zhongjiao/2019/0610/40491668.html
        Rule(LinkExtractor(allow=(r'china.com.cn.*?/%s/\d{2}/\d+.s?htm' % datetime.today().strftime('%Y/%m'),
                                  r'tech.china.com.cn/\S+/\d{8}/\d+.shtml',
                                  r'finance.china.com.cn/\S+/\d{8}/\d+.shtml'),
                           deny=deny_list
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'china.com.cn.*?\w{5,}.s?htm',),
                           deny=deny_list
                           ),
             process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath

        try:
            sdiv = xp('//div[@class="info" or '
                      'starts-with(@class,"artiInfo") or '
                      '@class="articleInfo" or '
                      '@class="artInfo"]')[0]  # 不严谨在于获取到了所有满足要求的节点
            pubtime = sdiv.xpath('//*[@id="pubtime_baidu"]/text() | '
                                 '//div[@class="pub_date"]/text()')\
                .extract_first('').replace('发布时间：', '').strip()
            origin_name = sdiv.xpath('//*[@id="source_baidu"]/text()')\
                .extract_first('')
            content_div = xp('//div[@id="artbody" or '
                             '@id="artiContent" or '
                             '@id="articleBody" or '
                             '@class="artCon"]')[0]
            title = xp('//*[@class="artTitle"]/text()').extract_first('') or \
                self.get_page_title(response).split('_')[0]
        except:
            return self.parse_item_2(response)

        next_a = xp('//div[@id="autopage"]/center/a[text()=">"]')
        if next_a:
            return response.follow(next_a[0],
                                   callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         }
                                   )
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item_2(self, response):
        xp = response.xpath

        try:
            # http://cppcc.china.com.cn/2019-06/18/content_74895370.htm
            sdiv = xp('//div[@class="center_title" or '
                '@class="photo_center" or '
                '@class="left_box"]/div[@class="span"] | '
                '//div[@class="box2" or @class="box1"]/h2')[0]
            # 发布时间： 2019-06-19 08:33:16  |  来源： 人民政协报  |  作者： 孙金诚  |  责任编辑： 王静
            pubtime = sdiv.re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}(?:\:\d{2})?')[0]
            # 书名号不能用\w正则  来源： 《求是》
            og = sdiv.re(r'来源：\s?《?\w+》?')
            origin_name = og[0] if og else ""
            content_div = xp('//div[@class="center_box" or '
                             '@id="artiContent"] | '
                             '//div[@class="box2"]/p')[0]
            title = xp('//*[@class="center_title"]/h1/text()').extract_first('') or \
                xp('//div[@class="box2"]/h1/text()').extract_first('') or \
                self.get_page_title(response).split('_')[0]
        except:
            return self.parse_item_3(response)
        next_a = xp('//div[@id="autopage"]/center/a[text()=">"]')
        if next_a:
            return response.follow(next_a[0],
                                   callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         }
            
                                   )
        
        content, media, videos, _ = self.content_clean(content_div, need_video=True)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )
    
    def parse_page(self, response):
        meta_new = deepcopy(response.meta)
        xp = response.xpath

        try:
            content_div = xp('.//div[@id="artiContent" or @class="center_box" or @id="fontzoom"] | '
                             '//div[@class="box2"]/p |'
                             '//figcaption[@class="imgComment_content"]')[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()
        next_a = xp('//div[@id="autopage"]/center/a[text()=">"]')
        if next_a:
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
        
        content, media, _, _ = self.content_clean(meta_new['content'], kill_xpaths=['//div[@id="autopage"]', ])
        
        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),
            content=content,
            media=media
        )
    
    def parse_item_3(self, response):
        # http://music.china.com.cn/2019-06/13/content_40784197.htm
        xp = response.xpath

        try:
            sdiv = xp('//div[@class="box1l"]/h4')[0]
            # 发布时间：2019-06-13 09:27:50 丨 来源：北京日报 丨 责任编辑：杨海乾
            pubtime = sdiv.re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')[0]
            origin_name = sdiv.re(r'来源：\s?\w+')[0]
            content_div = xp('//div[@class="box1l"]/div[@class="cp"]')[0]
            title = xp('//div[@class="box1l"]/h1/text()').extract_first('') or \
                    self.get_page_title(response).split('-')[0]
        except:
            return self.parse_item_4(response)

        next_a = xp('//div[@id="autopage"]/center/a[text()=">"]')
        if next_a:
            return response.follow(next_a[0],
                                   callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         }
            
                                   )
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item_4(self, response):
        # http://ocean.china.com.cn/2019-06/10/content_74871868.htm
        xp = response.xpath

        try:
            sdiv = xp('//div[@class="box18"]/dl/dd')
            if len(sdiv) > 0:
                pubtime = sdiv.xpath('./*[@id="pubtime_baidu"]/text()').extract_first('').replace('发布时间：', '').strip()
                origin_name = sdiv.xpath('./*[@id="source_baidu"]/text()').extract_first('')
            else:
                sdiv = response.xpath('//span[@class="fl time2"]/text()')
                sdiv_parts = sdiv.extract_first().split()
                if len(sdiv_parts) == 1:
                    origin_name = response.xpath('//span[@class="fl time2"]/a/text()').extract_first()
                else:
                    origin_name = sdiv_parts[1]
                pubtime = sdiv_parts[0]

            content_div = xp('//div[@id="fontzoom"]/p')
            title = self.get_page_title(response).split('_')[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        next_a = xp('//div[@id="autopage"]/center/a[text()=">"]')
        if next_a:
            return response.follow(next_a[0],
                                   callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         }
            
                                   )
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item_5(self, response):
        # http://travel.china.com.cn/txt/2019-06/17/content_74891921.html
        xp = response.xpath

        try:
            sdiv = xp('//div[@class="Tinfo"]')[0]
            pubtime = sdiv.xpath('./*[@id="pubtime_baidu"]/text()').extract_first('').replace('发布时间：', '').strip()
            origin_name = sdiv.xpath('./*[@id="source_baidu"]/text()').extract_first('')
            content_div = xp('//div[@id="fontzoom"]')[0]
            title = self.get_page_title(response).split('_')[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        next_a = xp('//div[@id="autopage"]/center/a[text()=">"]')
        if next_a:
            return response.follow(next_a[0],
                                   callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')
                                         }
            
                                   )
        content, media, _, _ = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )


class ChinaSportsSpider(NewsRCSpider):
    """中国网-体育"""
    name = 'china_sports'
    mystart_urls = {
        'http://sports.china.com.cn/': 18259,  # 中国网-体育-除视频推荐所有内容
    }
    
    rules = (
        # http://sports.china.com.cn/zutu/detail2_2019_06/13/1239455.html
        Rule(
            LinkExtractor(allow=(r'china.com.cn/zutu/detail2_%s/\d{2}/\d+.s?htm' % datetime.today().strftime('%Y_%m'),),
                          # deny=(r'',)
                          ),
            callback='parse_item_2', follow=False),
        # http://sports.china.com.cn/zuqiu/detail2_2019_06/19/1251716.html
        # http://sports.china.com.cn/tubu/detail2_2019_04/30/1152611.html
        Rule(LinkExtractor(allow=(r'china.com.cn.*?/detail2_%s/\d{2}/\d+.s?htm' % datetime.today().strftime('%Y_%m'),),
                           deny=(r'sports.china.com.cn/other/',)
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'china.com.cn.*?\w{5,}.s?htm',),
                           deny=(r'/201[0-8]', r'/20190[1-9]/', r'/detail2_2019_0[1-5]', r'/2019_0[1-5]', r'/index.htm',
                                 r'/detail2_201[0-8]', r'sports.china.com.cn/other/')
                           ),
             process_request=otherurl_meta, follow=False),
    )
    
    custom_settings = {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % ChinaSpider.name}

    def parse_item(self, response):
        xp = response.xpath
        try:
            sdiv = xp('//div[@id="menucontainer0_10"]/div/dl/dd')[0]
            pubtime = sdiv.re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}(?:\:\d{2})?')[0]
            origin_name = ""
            for i in sdiv.xpath('.//text()').extract():
                if '来源' in i:
                    origin_name = i
                    break
            content_div = xp('//div[@id="menucontainer0_10"]/div/p')
            content, media, _, _ = self.content_clean(content_div)
            title = self.get_page_title(response).split('_')[0]
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
    
    def parse_item_2(self, response):
        xp = response.xpath
        try:
            sdiv = xp('//span[@class="pic-r-span r"]')
            pubtime = sdiv.re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}(?:\:\d{2})?')[0]
            og = sdiv.re(r'来源：\s?《?\w+》?')
            origin_name = og[0] if og else ""
            title = xp('//div[@class="picTitle w"]/span[1]/text()').extract_first('')
            ss = xp('//script[contains(text(), "var picList")]')[0].extract()
            st = ss.index('var picList = [')
            ed = ss.index('];')
            dj = ss[st + len('var picList = [') - 1:ed + 1]
            dj = dj.replace('\r', '').replace('\n', '').strip()
            img_cons = json.loads(dj)  # 不是标题 <title>体育中国_中国网</title>
            content, media = self.make_img_content(img_cons)
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
    
    def make_img_content(self, img_cons):
        """
        拼接图、文列表为html
        """
        media = {'images': {}}
        content = ''
        for i, j in enumerate(img_cons):
            content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
            if j.get('detail'):
                content += '<p>' + j['detail'] + '</p>'
            
            media['images'][str(i + 1)] = {"src": j['bigPic']}
        
        return content, media


class ChinaJiangSuSpider(NewsRCSpider):
    """中国网-江苏-房产"""
    name = 'china_jianshu_house'
    mystart_urls = {
        'http://jiangsu.china.com.cn/html/jsnews/gnxw/': 1200987,
        # 中国网-国内新闻
        'http://house.china.com.cn/': 18240,  # 中国网-地产-页面全部内容
    }

    deny_list = [r'/201[0-8]', r'/20190[1-9]/', r'/2019-0[1-9]',
                 r'/2019_0[1-5]', r'/2019_0[1-9]',
                 r'house.china.com.cn/zhoukan/\d+.htm',
                 r'/html/jsnews/gnxw/\d+.html',
                 r'house.china.com.cn/helpbrowser/\w+.html',
                 r'/userweb/\w+.html?', r'/column_\d+.htm', r'/200[0-9]',
                 r'News/\S+_1s\.htm', r'/statics/.*?html',
                 r'/newhouse/.*?htm', r'/default\.htm', r'topic/.*?html',
                 r'sitemap\.htm',
                 r'http://jiangsu.china.com.cn/html/jsnews/gnxw/index.html', ]
    
    rules = (
        # http://jiangsu.china.com.cn/html/jsnews/gnxw/10640219_1.html
        # http://house.china.com.cn/newscenter/view/1576170.htm
        Rule(LinkExtractor(allow=(r'china.com.cn.*?\w{4,}\.s?htm',),
                           deny=deny_list
                           # deny=(r'/201[0-8]', r'/20190[1-9]/', r'/2019-0[1-9]', r'/2019_0[1-5]',
                           #       r'house.china.com.cn/zhoukan/\d+.htm', r'/html/jsnews/gnxw/\d+.html',
                           #       r'house.china.com.cn/helpbrowser/\w+.html', r'/userweb/\w+.html?',
                           #       r'/column_\d+.htm', r'/200[0-9]', r'News/\S+_1s.htm', r'/statics/.*?html',
                           #       r'/404.html', r'/newhouse/.*?htm', r'/default.htm', r'topic/.*?html',
                           #       r'sitemap.htm', )
                           ),
             callback='parse_item', follow=False),
        
        Rule(LinkExtractor(allow=(r'china.com.cn.*?/\w+.s?htm',),  # allow=(r'[\S.]*china.com.cn.*?/view/\w+.s?htm', ),
                           deny=deny_list
                           # deny=(r'/201[0-8]', r'/20190[1-9]/', r'/2019-0[1-9]', r'/2019_0[1-9]',
                           #       r'house.china.com.cn/zhoukan/\d+.htm', r'/html/jsnews/gnxw/\d+.html',
                           #       r'house.china.com.cn/helpbrowser/\w+.html', r'/userweb/\w+.html?',
                           #       r'/column_\d+.htm', r'/200[0-9]', r'News/\S+_1s.htm', r'/statics/.*?html',
                           #       r'/404.html', r'/newhouse/.*?htm', r'/default.htm', r'topic/.*?html',
                           #       r'sitemap.htm', )
                           ),
             process_request=otherurl_meta, follow=False),
    )
    custom_settings = {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % ChinaSpider.name}
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            sdiv = xp('//div[@id="Article"]/div[1]')[0]
            pubtime = sdiv.xpath('./*[@id="pubtime_baidu"]/text()').extract_first('').replace('发布时间：', '').strip()
            origin_name = sdiv.xpath('./*[@id="source_baidu"]/text()').extract_first('')
            content_div = xp('//div[@class="content"]/p')
            title = self.get_page_title(response).split('_')[0]
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item2(self, response):
        xp = response.xpath
        try:
            sdiv = xp('//div[@class="left_from"]/div')[0]
            pub_time = sdiv.xpath('./*[@id="pubtime_baidu"]/text()').extract_first('').replace('发布时间：', '').strip()
            origin_name = sdiv.xpath('./*[@id="source_baidu"]/text()').extract_first('').replace('来源 ：', '').strip()
            content_div = xp('//div[@class="xwzw"]/p')
            title = self.get_page_title(response).split('_')[0]
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pub_time,
            origin_name=origin_name,
            content=content,
            media=media
        )


class ChinaTFSpider(NewsRCSpider):
    name = 'china_tech_finance'
    mystart_urls = {
        'http://tech.china.com.cn/it/': 18113,  # 中国网-汽车-IT业界-左侧
        'http://tech.china.com.cn/telecom/': 18112,  # 中国网-汽车-科技通信-左侧
        'http://tech.china.com.cn/internet/': 18111,
        # 中国网-科技-互联网  http://tech.china.com.cn/internet/20190619/356937.shtml
        'http://tech.china.com.cn/elec/': 18114,  # 中国网-科技-家电  # http://tech.china.com.cn/elec/20190619/356955.shtml
        'http://tech.china.com.cn/digi/': 18115,  # 中国网-科技-数码
        'http://tech.china.com.cn/live.shtml': 18118,  # 中国网-科技-滚动
        
        'http://finance.china.com.cn/stock/ssgs/index.shtml': 18145,  # 中国网-财经-上市公司-左侧
        'http://finance.china.com.cn/': 18138,  # 中国网-财经-左侧头条以下全部
        'http://finance.china.com.cn/money/my.shtml': 18137,  # 中国网-财经-理财原创
        'http://finance.china.com.cn/stock/dp/index.shtml': 18144,  # 中国网-财经-理财大盘分析
        'http://finance.china.com.cn/money/cfsh/index.shtml': 18132,  # 中国网-财经-理财财富生活
        'http://finance.china.com.cn/stock/qsdt/index.shtml': 18148,  # 中国网-财经-证券券商动态
        'http://finance.china.com.cn/stock/my.shtml': 18153,  # 中国网-财经-证券原创
        'http://finance.china.com.cn/stock/xsb/index.shtml': 18154,  # 中国网-财经-证券新三板
        'http://finance.china.com.cn/stock/hkstock/index.shtml': 18151,  # 中国网-财经-证券港股动态
        'http://finance.china.com.cn/stock/usstock/index.shtml': 18152,  # 中国网-财经-证券美股动态
        'http://finance.china.com.cn/stock/zqyw/index.shtml': 18147,  # 中国网-财经-证券要闻
    }
    
    rules = (
        # http://finance.china.com.cn/roll/photo/20190716/14443.shtml
        # http://finance.china.com.cn/roll/photo/20190716/14441.shtml
        Rule(LinkExtractor(allow=(r'china.com.cn/roll/photo/%s\d{2}/\d+.s?htm' % datetime.today().strftime('%Y%m'),),
                           ),
             callback='parse_item_2', follow=False),
        # http://tech.china.com.cn/it/20190617/356839.shtml
        # http://tech.china.com.cn/telecom/20190618/356887.shtml
        # http://finance.china.com.cn/house/20190619/5009493.shtml
        Rule(LinkExtractor(allow=(r'china.com.cn.*?/%s\d{2}/\d+.s?htm' % datetime.today().strftime('%Y%m'),),
                           # deny=(r'',)
                           ),
             callback='parse_item', follow=False),
        
        Rule(LinkExtractor(allow=(r'china.com.cn.*?\w{5,}.s?htm',),
                           deny=(
                           r'/201[0-8]', r'/20190[1-9]/', r'/2019-0[1-9]', r'/2019_0[1-9]', r'/20190[1-9]/', '/index.htm'
                                                                                                            r'/node_\d+.htm')
                           ),
             process_request=otherurl_meta, follow=False),
    )
    custom_settings = {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % ChinaSpider.name}
    
    def parse_item(self, response):
        xp = response.xpath

        try:
            pubtime = xp('//span[@class="fl time2"]').re(r'\d{4}年\d{2}月\d{2}日\d{2}:\d{2}')[0]
            origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first('')
            content_div = xp('//div[@id="fontzoom"]')[0]
            title = self.get_page_title(response).split('_')[0]
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    # //div[@id='content']/div[@class='BX_page']
    def parse_item_2(self, response):
        # http://finance.china.com.cn/roll/photo/20190716/14443.shtml
        xp = response.xpath
        try:
            pubtime = Pubtime(xp('//span[@id="pubtime_baidu"]/text()')[0].extract())
            # 发布时间：2019-07-16 10:54:31
            origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first('')
            title = self.get_page_title(response).split('_')[0]
            ss = xp('//script[contains(text(), "var pic_data")]')[0].extract()
            """
            var pic_data={"list":[
{"note":"7月14日，在西班牙巴伦西亚，人们在街边餐厅吃饭聊天。 西班牙巴伦西亚紧靠大海，一年四季气候宜人。时值盛夏，游客纷纷来到这里度假，与当地居民一起享受悠闲夏日。 新华社记者 郭求达 摄","image":"http://image.finance.china.cn/roll/photo/20190716/182_22714443585_20190716105431.jpg"},
{"note":"7月14日，在西班牙巴伦西亚，当地居民在阳台上看风景。 西班牙巴伦西亚紧靠大海，一年四季气候宜人。时值盛夏，游客纷纷来到这里度假，与当地居民一起享受悠闲夏日。 新华社记者 郭求达 摄","image":"http://image.finance.china.cn/roll/photo/20190716/182_22714443587_20190716105431.jpg"},
{"note":"7月14日，在西班牙巴伦西亚，行人牵着狗走过小巷。 西班牙巴伦西亚紧靠大海，一年四季气候宜人。时值盛夏，游客纷纷来到这里度假，与当地居民一起享受悠闲夏日。 新华社记者 郭求达 摄","image":"http://image.finance.china.cn/roll/photo/20190716/182_22714443589_20190716105431.jpg"},
{"note":"7月14日，在西班牙巴伦西亚，孩子们在一处广场上玩肥皂泡。 西班牙巴伦西亚紧靠大海，一年四季气候宜人。时值盛夏，游客纷纷来到这里度假，与当地居民一起享受悠闲夏日。 新华社记者 郭求达 摄","image":"http://image.finance.china.cn/roll/photo/20190716/182_22714443591_20190716105431.jpg"}
]};
            """
            st = ss.index('var pic_data={"list":[')
            ed = ss.index(']};')
            dj = ss[st + len('var pic_data={"list":[') - 1:ed + 1]
            dj = dj.replace('\r', '').replace('\n', '').strip()
            img_cons = json.loads(dj)
            content, media = self.make_img_content(img_cons)
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
    
    def make_img_content(self, img_cons):
        """
        拼接图、文列表为html
        """
        media = {'images': {}}
        content = ''
        for i, j in enumerate(img_cons):
            content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
            if j.get('note'):
                content += '<p>' + j['note'] + '</p>'
        
            media['images'][str(i + 1)] = {"src": j['image']}
        return content, media
    

class ChinaOpinionSpider(NewsRCSpider):
    name = 'china_opinion'
    mystart_urls = {
        'http://opinion.china.com.cn/': 18248,  # 中国网-观点-左侧焦点
    }
    rules = (
        # http://opinion.china.com.cn/opinion_8_208808.html
        Rule(LinkExtractor(allow=(r'opinion.china.com.cn/opinion_\d+_\d+.htm',),
                           # deny=(r'',)
                           ),
             callback='parse_item', follow=False),
        
        Rule(LinkExtractor(allow=(r'opinion.china.com.cn.*?\w+.htm',),
                           deny=(
                               r'/201[0-8]', r'/20190[1-9]/', r'/2019-0[1-9]', r'/2019_0[1-9]', r'/20190[1-9]/',
                               '/index.htm'
                               r'/node_\d+.htm', r'opinion.china.com.cn/event_')
                           ),
             process_request=otherurl_meta, follow=False),
    )
    custom_settings = {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % ChinaSpider.name}
    
    def parse_item(self, response):
        xp = response.xpath

        try:
            pubtime = xp('/html/head/meta[@name="publishdate"]/@content')[0].extract()
            origin_name = xp('//span[@class="article-source"]/text()').extract_first('')
            content_div = xp('//div[@class="article-content"]')[0]
            title = self.get_page_title(response).split('_')[0]
            content, media, _, _ = self.content_clean(content_div)
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
