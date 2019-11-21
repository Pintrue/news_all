#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 9:10
# @Author  : wjq
# @File    : jinritaotiao_wap.py
import random
from datetime import datetime
import json
import time
import execjs
from scrapy import Request
from news_all.spider_models import NewsRSpider
from news_all.tools.agents import USER_AGENTS
from copy import deepcopy
from scrapy.conf import settings

from news_all.tools.html_clean import decode_html


class JrttWapSpider(NewsRSpider):
    chinese_name = """今日头条app"""
    name = 'jrtt_app'
    dd = deepcopy(settings.getdict('APP_DOWN'))
    dd['news_all.middlewares.ProxyRdMiddleware'] = 100  # 备用 使用隧道代理
    """
    2019-06-03 10:39:34 [scrapy.core.engine] DEBUG: Crawled (301) <GET http://toutiao.com/group/6697879472701440524/> (referer: None)
    2019-06-03 10:39:34 [scrapy.spidermiddlewares.httperror] INFO: Ignoring response <301 http://toutiao.com/group/6697879472701440524/>: HTTP status code is not handled or not allowed
    2019-06-03 10:39:34 [scrapy.core.engine] DEBUG: Crawled (301) <GET http://toutiao.com/group/6697570849295172110/> (referer: None)
    2019-06-03 10:39:35 [scrapy.spidermiddlewares.httperror] INFO: Ignoring response <301 http://toutiao.com/group/6697570849295172110/>: HTTP status code is not handled or not allowed
    """

    custom_settings = {
        'HTTPERROR_ALLOWED_CODES': [301, 302],
        # 为了解决在online3服务器出现报错  方法
        # 1. 不修改代码在online1跑
        # 2. 加上设置'HTTPERROR_ALLOWED_CODES': [301, 302]再online3测试
        # 3. 不加设置, 而把news_url("http://toutiao.com/group/6697806251838931464/")替换为https://www.toutiao.com/a6697806251838931464/

        'DOWNLOADER_MIDDLEWARES': dd, }
    sleep_time = 300
    mystart_urls = {
        'https://lf.snssdk.com/api/news/feed/v47/?category=news_hot&refer=1&count=20&last_refresh_sub_entrance_interval=1558418761&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4277&cid=34389&cp=59cbe03497549q1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558418761355': 3632,
        # 'https://lf.snssdk.com/api/news/feed/v47/?category=video&refer=1&count=20&last_refresh_sub_entrance_interval=1558419094&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4277&cid=34389&cp=59c5e23499696q1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419094281': 3633,
        # 视频暂不抓
        'https://lf.snssdk.com/api/news/feed/v47/?category=nineteenth&refer=1&count=20&last_refresh_sub_entrance_interval=1558419113&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4277&cid=34389&cp=5dcdeb39956a9q1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419113416': 3634,
        'https://lf.snssdk.com/api/news/feed/v47/?category=news_entertainment&concern_id=6215497896830175745&refer=1&count=20&last_refresh_sub_entrance_interval=1558419178&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4277&cid=34389&cp=51c9ea3e9f6eaq1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419178641': 3635,
        'https://lf.snssdk.com/api/news/feed/v47/?category=%E7%BB%84%E5%9B%BE&refer=1&count=20&min_behot_time=1558419200&last_refresh_sub_entrance_interval=24&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=pull&lac=4277&cid=34389&cp=51c2e83c9c719q1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419225319': 3636,
        'https://lf.snssdk.com/api/news/feed/v47/?category=news_tech&concern_id=6215497899594222081&refer=1&count=20&last_refresh_sub_entrance_interval=1558419286&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4277&cid=34389&cp=5acbeb3190756q1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419286084': 3637,
        'https://lf.snssdk.com/api/news/feed/v47/?category=news_car&concern_id=6215497898671475202&refer=1&count=20&last_refresh_sub_entrance_interval=1558419310&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4277&cid=34389&cp=59c6e2329276eq1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419310250': 3638,
        'https://lf.snssdk.com/api/news/feed/v47/?category=news_sports&concern_id=6215497726554016258&refer=1&count=20&last_refresh_sub_entrance_interval=1558419364&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4278&cid=41755&cp=5dcde73f987a4q1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419364471': 3639,
        'https://lf.snssdk.com/api/news/feed/v47/?category=news_finance&concern_id=6215497900357585410&refer=1&count=20&last_refresh_sub_entrance_interval=1558419389&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4278&cid=41755&cp=5ec4e3379b7bdq1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419389546': 3640,
        'https://lf.snssdk.com/api/news/feed/v47/?category=news_military&concern_id=6215497895454444033&refer=1&count=20&last_refresh_sub_entrance_interval=1558419426&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4278&cid=41755&cp=55cce3319d7e2q1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419426591': 3641,
        'https://lf.snssdk.com/api/news/feed/v47/?category=news_world&concern_id=6215497896255556098&refer=1&count=20&last_refresh_sub_entrance_interval=1558419457&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4278&cid=41755&cp=58c2ee389d801q1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419457534': 3642,
        'https://lf.snssdk.com/api/news/feed/v47/?category=news_health&concern_id=6215497895248923137&refer=1&count=20&last_refresh_sub_entrance_interval=1558419483&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4278&cid=41755&cp=55cce8329881bq1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419483278': 3643,
        'https://lf.snssdk.com/api/news/feed/v47/?category=positive&concern_id=6215497898474342913&refer=1&count=20&last_refresh_sub_entrance_interval=1558419519&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4278&cid=41755&cp=58c8ec359a83fq1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419519826': 3644,
        'https://lf.snssdk.com/api/news/feed/v47/?category=news_house&concern_id=6215497897127971330&refer=1&count=20&last_refresh_sub_entrance_interval=1558419550&loc_mode=7&loc_time=1558418670&latitude=39.920306&longitude=116.467767&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4278&cid=41755&cp=58c7e7379185eq1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419550211': 3645,
        'https://lf.snssdk.com/api/news/feed/v47/?category=%E5%86%AC%E5%A5%A5%E4%BC%9A&concern_id=6213176486224988674&refer=1&count=20&last_refresh_sub_entrance_interval=1558419951&loc_mode=7&loc_time=1558418831&latitude=39.920369&longitude=116.467763&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4278&cid=41755&cp=5ac5e2379c9efq1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419951508': 3646,
        'https://lf.snssdk.com/api/news/feed/v47/?category=NBA&concern_id=6213187421211724290&refer=1&count=20&last_refresh_sub_entrance_interval=1558419995&loc_mode=7&loc_time=1558418831&latitude=39.920369&longitude=116.467763&city=%E5%8C%97%E4%BA%AC%E5%B8%82&tt_from=enter_auto&lac=4277&cid=34389&cp=53cde23993a1bq1&iid=6373631806&device_id=7898061635&ac=wifi&channel=tengxun&aid=13&app_name=news_article&version_code=584&version_name=5.8.4&device_platform=android&ab_version=830855%2C754087%2C770570%2C903094%2C662176%2C665176%2C674053%2C770488%2C643893%2C374116%2C550042%2C435213%2C649429%2C677131%2C377573%2C522765%2C710077%2C801968%2C707372%2C758013%2C603441%2C789246%2C900122%2C800208%2C603381%2C603398%2C603404%2C603405%2C866773%2C833900%2C844799%2C886435%2C661903%2C668775%2C832706%2C894306%2C795195%2C792681%2C891859%2C607361%2C739393%2C764921%2C662099%2C900107%2C812271%2C875783%2C894991%2C668774%2C894997%2C775311%2C765193%2C549647%2C615291%2C857803%2C546701%2C757281%2C798159%2C853743%2C862909%2C679101%2C767991%2C861913%2C779958%2C894723%2C660830%2C900478%2C903667%2C457481%2C649400%2C860529&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=R8207&device_brand=OPPO&language=zh&os_api=19&os_version=4.4.4&uuid=865685026456493&openudid=aa864676b309bf74&manifest_version_code=584&resolution=720*1280&dpi=320&update_version_code=5844&_rticket=1558419995147': 3647,
    }
    
    def parse(self, response):
        rs = json.loads(response.text)
        total = 0  # 一次刷新列表页 得到有效时限内的新闻数量
        for i in rs.get('data'):
            rc = i.get('content')
            rd = json.loads(rc)
            result = self.deal_one_article(rd, response)
            if result:
                if isinstance(result, Request):
                    total += 1
                yield result

            articles = rd.get('data', [])
            for art in articles:
                result = self.deal_one_article(art, response)
                if result:
                    if isinstance(result, Request):
                        total += 1
                    yield result
        self.log('source_id: %s, 刷出新闻数量: %s' % (response.meta.get('source_id'), total))

    def deal_one_article(self, art, response):
        # 排除视频
        if art.get('has_video') == True:
            return  # 排除视频
        urls = [art.get('display_url'), art.get('article_url'), art.get('share_url'), art.get('article_alt_url'),
                art.get('url'), ]
        # 'https://m.toutiaocdn.net/group/6695695736870273548/?app=news_article&is_hit_share_recommend=0'
        news_url = None
        for u in urls:
            if u and ('toutiao.com' in u or 'toutiaocdn.net' in u or 'toutiaocdn.com' in u):
                news_url = u
                break
        if not news_url:
            self.log('source_id: %s, have no news_url or data key' % response.meta.get('source_id'))
            return
        aid = news_url.split('/')[-2]
        if not aid.isdigit():
            self.log('source_id: %s, news_url: %s has not id' % (response.meta.get('source_id'), news_url))
            return
        news_url = 'https://www.toutiao.com/a{}'.format(aid)

        title = art.get('title')
        pubtime = art.get('publish_time')
        origin_name = art.get('source')
        time.sleep(random.uniform(0, 5))
        return Request(
            url=news_url,
            callback=self.parse_item,
            # headers={"User-Agent": UA[random.randint(0, len(UA) - 1)]},
            headers={"User-Agent": USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)]},
            # 比如<GET https://www.toutiao.com/a6696250259334496776/> 不能用安卓浏览器
            # headers={"User-Agent": APP_uSER_AGENTS[random.randint(0, len(APP_uSER_AGENTS) - 1)]},
            meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                   'origin_name': origin_name,
                  'start_url_time': response.meta.get('start_url_time'),
                  'schedule_time': response.meta.get('schedule_time')}
        )

    def img_cont(self, con_dict):
        ps = con_dict.get('sub_abstracts')  # 段落文字
        imgs = con_dict.get('sub_images')
        if not ps or not imgs:
            return None, {}
        if len(ps) != len(imgs):
            self.log('段落数量: %s, 图片数量: %s' % (len(ps), len(imgs)))

        media = {"images": {}}
        new_content = ''

        for i, j in enumerate(imgs):
            media["images"][str(i + 1)] = {'src': j.get('url')}
            new_content += '<p>' + '${{%s}}$' % (i + 1) + '</p>' + '<p>' + ps[i] + '</p>'

        new_content.replace('$$', '$<br>$')  # 连续2图片加换行
        return new_content, media

    def parse_item(self, response):
        if 'www.toutiao.com' not in response.url:
            self.log('host is not www.toutiao.com, source_id=%s, url=%s, last_url=%s' % (
            response.meta.get('source_id'), response.url, response.request.url))
            return
        xp = response.xpath
        try:
            ss = xp('//script[contains(text(), "var BASE_DATA")]/text()')[0].extract()
            # var __wenda_data
            ect1 = execjs.compile(ss)
            rj = ect1.eval('BASE_DATA')
            if 'articleInfo' in rj:
                content_div = rj.get('articleInfo').get('content')
                content = decode_html(content_div)
                content, media, _, _ = self.content_clean(content)
            elif rj['headerInfo'].get('chineseTag') == '问答':
                return
            else:
                gallery = rj.get('galleryInfo').get('gallery')  # rj['headerInfo'].get('chineseTag') == '图片'
                content, media = self.img_cont(gallery)
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,
            title=response.meta['title'],
            pubtime=response.meta['pubtime'],
            origin_name=response.meta['origin_name'],
            
            content=content,
            media=media,
        )