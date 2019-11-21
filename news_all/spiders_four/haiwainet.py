# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.conf import settings
from copy import deepcopy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, isStartUrl_meta, otherurl_meta
import re
import json


class HaiWaiNetSpider(NewsRCSpider):
    """海外网"""
    name = 'haiwainet'
    mystart_urls = {
        'http://opinion.haiwainet.cn/': 474,  # 首页
        'http://opinion.haiwainet.cn/353596/': 475,  # 原创评论
        # 'http://opinion.haiwainet.cn/353596/index.html': 909,
        'http://opinion.haiwainet.cn/456318/': 476,  # 学习小组
        # 'http://opinion.haiwainet.cn/456318/index.html': 928,
        'http://opinion.haiwainet.cn/456317/': 477,  # 侠客岛
        # 'http://opinion.haiwainet.cn/456317/index.html': 925,
        'http://opinion.haiwainet.cn/456465/': 478,  # 港台腔
        # 'http://opinion.haiwainet.cn/456465/index.html': 926,
        'http://news.haiwainet.cn/': 479,  # 首页 滚动
        'http://theory.haiwainet.cn/study/': 481,  # 学习中国
        # 'http://theory.haiwainet.cn/study/index.html': 1129,
        'http://theory.haiwainet.cn/decode/': 482,  # 解码中国
        # 'http://theory.haiwainet.cn/decode/index.html': 1128,
        'http://theory.haiwainet.cn/thinktank/': 483,  # 智汇中国
        # 'http://theory.haiwainet.cn/thinktank/index.html': 1132,
        'http://theory.haiwainet.cn/abroad/': 484,  # 海外中国
        # 'http://theory.haiwainet.cn/abroad/index.html': 1130,
        'http://huaren.haiwainet.cn/yuanchuang/': 485,  # 原创推荐
        'http://huaren.haiwainet.cn/232658/': 486,  # 全球华媒联播
        'http://huaren.haiwainet.cn/345784/': 487,  # 华商中心
        'http://huaren.haiwainet.cn/': 488,  # 华人频道
        'http://huaren.haiwainet.cn/345785/': 489,  # 人在异国
        'http://hk.haiwainet.cn/': 490,  # 首页
        'http://hk.haiwainet.cn/news/': 491,  # 滚动
        
        'http://tw.haiwainet.cn/scroll-news/': 493,  # 滚动
        # 'http://tw.haiwainet.cn/scroll-news/index.html': 1127,
        'http://tw.haiwainet.cn/': 494,  # 首页
        
        # 来自spiders_all
        'http://travel.haiwainet.cn/wanzhuanhaiwai/index.html': 862,  # ok
        'http://travel.haiwainet.cn/renwufangtan/index.html': 864,  # ok
        'http://travel.haiwainet.cn/guoneiyou/index.html': 868,  # ok
        'http://travel.haiwainet.cn/gexingyou/index.html': 869,  # ok
        'http://travel.haiwainet.cn/chujingyou/index.html': 871,  # ok
        'http://travel.haiwainet.cn/456573/index.html': 872,  # ok
        'http://sannong.haiwainet.cn/457135/index.html': 873,  # ok
        'http://sannong.haiwainet.cn/457137/': 874,
        # 'http://sannong.haiwainet.cn/457137/index.html': 1093,
        'http://sannong.haiwainet.cn/457130/': 876,
        # 'http://sannong.haiwainet.cn/457130/index.html': 1091,
        'http://minsheng.haiwainet.cn/455825/': 877,  # ok
        'http://minsheng.haiwainet.cn/455830/': 878,  # ok
        'http://jinrong.haiwainet.cn/gjjr/': 879,  # ok
        'http://jinrong.haiwainet.cn/zhengquan/': 880,  # ok
        'http://jinrong.haiwainet.cn/zhengce/': 881,  # ok
        'http://jinrong.haiwainet.cn/chuangxin/': 882,  # ok
        'http://jinrong.haiwainet.cn/wenhua/': 884,  # ok
        'http://jinrong.haiwainet.cn/zixun/': 885,  # ok
        'http://jinrong.haiwainet.cn/jrnews/': 889,  # ok
        'http://renwen.haiwainet.cn/lywh/': 890,
        # 'http://renwen.haiwainet.cn/lywh/index.html': 1106,
        'http://jiaoyu.haiwainet.cn/zyjy/': 892,  # ok
        'http://jiaoyu.haiwainet.cn/jygd/': 893,  # ok
        'http://jiaoyu.haiwainet.cn/guojijiaoliu/': 894,
        # 'http://jiaoyu.haiwainet.cn/guojijiaoliu/index.html': 1090,
        'http://jiaoyu.haiwainet.cn/xiaoyuan/': 895,
        # 'http://jiaoyu.haiwainet.cn/xiaoyuan/index.html': 1089,
        'http://jiaoyu.haiwainet.cn/zhonghuamingxiao/': 896,  # ok
        'http://jiaoyu.haiwainet.cn/bainianxuefu/': 897,  # ok
        'http://opinion.haiwainet.cn/456475/': 898,  # ok
        'http://opinion.haiwainet.cn/456900/': 899,  # ok
        'http://travel.haiwainet.cn/shijiemeishi/': 900,
        # 'http://travel.haiwainet.cn/shijiemeishi/index.html': 867,
        'http://opinion.haiwainet.cn/mingjiashalong/': 901,
        # 'http://opinion.haiwainet.cn/mingjiashalong/index.html': 1015,
        'http://haiju.haiwainet.cn/top/': 903,
        # 'http://haiju.haiwainet.cn/top/index.html': 927,
        'http://tw.haiwainet.cn/345692/': 904,
        # 'http://tw.haiwainet.cn/345692/index.html': 924,
        'http://world.haiwainet.cn/345796/': 905,
        # 'http://world.haiwainet.cn/345796/index.html': 922,
        'http://chuangxin.haiwainet.cn/news/': 907,  # ok
        'http://opinion.haiwainet.cn/345437/': 908,
        # 'http://opinion.haiwainet.cn/345437/index.html': 1131,
        'http://theory.haiwainet.cn/po/': 910,
        # 'http://theory.haiwainet.cn/po/index.html': 1133,
        'http://pt.haiwainet.cn/aomen/': 912,  # ok
        'http://www.haiwainet.cn/liuxue/cxcy/': 915,  # ok
        'http://www.haiwainet.cn/liuxue/hgjy/': 916,  # ok
        'http://www.haiwainet.cn/liuxue/hwsh/': 917,  # ok
        'http://culture.haiwainet.cn/mjhc/': 918,
        # 'http://culture.haiwainet.cn/mjhc/index.html': 1126,
        'http://quyu.haiwainet.cn/xwtt/': 919,  # ok
        'http://renwen.haiwainet.cn/xwjj/': 920,
        # 'http://renwen.haiwainet.cn/xwjj/index.html': 1125,
        'http://chengjian.haiwainet.cn/tebiebaodao/': 921,
        # 'http://chengjian.haiwainet.cn/tebiebaodao/index.html': 1119,
        'http://xiaokang.haiwainet.cn/xinwenzixun/': 923,
        # 'http://xiaokang.haiwainet.cn/xinwenzixun/index.html': 1118,
        'http://haisi.haiwainet.cn/chanjing/': 929,
        # 'http://haisi.haiwainet.cn/chanjing/index.html': 1117,
        'http://haisi.haiwainet.cn/wenlv/': 930,
        # 'http://haisi.haiwainet.cn/wenlv/index.html': 1116,
        'http://haisi.haiwainet.cn/shengtai/': 931,
        # 'http://haisi.haiwainet.cn/shengtai/index.html': 1115,
        'http://law.haiwainet.cn/qywh/': 932,
        'http://law.haiwainet.cn/gzms/': 933,
        # 'http://law.haiwainet.cn/gzms/index.html': 1112,
        'http://law.haiwainet.cn/sfyw/': 934,
        # 'http://law.haiwainet.cn/sfyw/index.html': 1113,
        'http://law.haiwainet.cn/fzxw/': 935,
        # 'http://law.haiwainet.cn/fzxw/index.html': 1111,
        'http://silu.haiwainet.cn/sltoutiao/': 936,
        # 'http://silu.haiwainet.cn/sltoutiao/index.html': 1110,
        'http://chengjian.haiwainet.cn/pinpaijujiao/': 937,
        # 'http://chengjian.haiwainet.cn/pinpaijujiao/index.html': 1109,
        'http://chengjian.haiwainet.cn/loushizhisheng/': 938,
        # 'http://chengjian.haiwainet.cn/loushizhisheng/index.html': 1108,
        'http://chengjian.haiwainet.cn/guoziguoqi/': 939,
        # 'http://chengjian.haiwainet.cn/guoziguoqi/index.html': 1107,
        'http://chengjian.haiwainet.cn/chengjiandongtai/': 940,
        'http://renwen.haiwainet.cn/zhjy/': 941,
        # 'http://renwen.haiwainet.cn/zhjy/index.html': 1104,
        'http://renwen.haiwainet.cn/cxzg/': 942,
        # 'http://renwen.haiwainet.cn/cxzg/index.html': 1099,
        'http://renwen.haiwainet.cn/smdq/': 943,
        # 'http://renwen.haiwainet.cn/smdq/index.html': 1098,
        'http://renwen.haiwainet.cn/rwzg/': 944,
        # 'http://renwen.haiwainet.cn/rwzg/index.html': 1097,
        'http://travel.haiwainet.cn/tiyankaocha/': 945,
        # 'http://travel.haiwainet.cn/tiyankaocha/index.html': 1096,
        'http://chuangxin.haiwainet.cn/348217/': 946,
        # 'http://chuangxin.haiwainet.cn/348217/index.html': 1095,
        'http://culture.haiwainet.cn/toutiao/': 947,
        # 'http://culture.haiwainet.cn/toutiao/index.html': 1086,
        'http://culture.haiwainet.cn/chengshi/': 948,
        # 'http://culture.haiwainet.cn/chengshi/index.html': 1087,
        'http://canada.haiwainet.cn/Associations/': 949,
        # 'http://canada.haiwainet.cn/Associations/index.html': 1085,
        'http://us.haiwainet.cn/News1/': 950,
        # 'http://us.haiwainet.cn/News1/index.html': 1084,
        'http://australia.haiwainet.cn/suggest/': 951,
        # 'http://australia.haiwainet.cn/suggest/index.html': 1083,
        'http://de.haiwainet.cn/457014/': 952,
        # 'http://de.haiwainet.cn/457014/index.html': 911,
        'http://haiju.haiwainet.cn/liu/': 953,
        # 'http://haiju.haiwainet.cn/liu/index.html': 1082,
        'http://huamei.haiwainet.cn/business/': 954,  # ok
        'http://nanhai.haiwainet.cn/observe/': 955,
        # 'http://nanhai.haiwainet.cn/observe/index.html': 1081,
        'http://nanhai.haiwainet.cn/news/': 956,
        # 'http://nanhai.haiwainet.cn/news/index.html': 1080,
        'http://tw.haiwainet.cn/345658/': 957,
        # 'http://tw.haiwainet.cn/345658/index.html': 1079,
        'http://tw.haiwainet.cn/345665/': 958,
        # 'http://tw.haiwainet.cn/345665/index.html': 1077,
        'http://news.haiwainet.cn/yuanchuang/': 959,
        # 'http://news.haiwainet.cn/yuanchuang/index.html': 1075,
        'http://news.haiwainet.cn/photo/': 960,  # ok
        'http://opinion.haiwainet.cn/345415/': 961,
        # 'http://opinion.haiwainet.cn/345415/index.html': 1074,
        'http://pinpai.haiwainet.cn/stny/': 963,
        # 'http://pinpai.haiwainet.cn/stny/index.html': 1073,
        'http://pinpai.haiwainet.cn/3541024/': 964,
        'http://pinpai.haiwainet.cn/dfzx/': 966,  # ok
        'http://pinpai.haiwainet.cn/ywzx/': 968,
        # 'http://pinpai.haiwainet.cn/ywzx/index.html': 1071,
        'http://pinpai.haiwainet.cn/kjcx/': 969,
        # 'http://pinpai.haiwainet.cn/kjcx/index.html': 1070,
        'http://pinpai.haiwainet.cn/456974/': 971,
        # 'http://pinpai.haiwainet.cn/456974/index.html': 1069,
        'http://pinpai.haiwainet.cn/nyzy/': 972,
        # 'http://pinpai.haiwainet.cn/nyzy/index.html': 1068,
        'http://smartcity.haiwainet.cn/mrzx/': 973,
        # 'http://smartcity.haiwainet.cn/mrzx/index.html': 1067,
        'http://shichuang.haiwainet.cn/zuixinhuodong/': 974,
        # 'http://shichuang.haiwainet.cn/zuixinhuodong/index.html': 1065,
        'http://shichuang.haiwainet.cn/meilizhongguo/': 975,
        # 'http://shichuang.haiwainet.cn/meilizhongguo/index.html': 1064,
        'http://shichuang.haiwainet.cn/kejiao/': 976,
        # 'http://shichuang.haiwainet.cn/kejiao/index.html': 1063,
        'http://shichuang.haiwainet.cn/shuhua/': 977,
        # 'http://shichuang.haiwainet.cn/shuhua/index.html': 1062,
        'http://shichuang.haiwainet.cn/nengyuan/': 978,
        # 'http://shichuang.haiwainet.cn/nengyuan/index.html': 1061,
        'http://shichuang.haiwainet.cn/wenlv/': 979,
        # 'http://shichuang.haiwainet.cn/wenlv/index.html': 1060,
        'http://shichuang.haiwainet.cn/chanjing/': 980,
        # 'http://shichuang.haiwainet.cn/chanjing/index.html': 1059,
        'http://jiankang.haiwainet.cn/syaq/': 981,
        # 'http://jiankang.haiwainet.cn/syaq/index.html': 1055,
        'http://jiankang.haiwainet.cn/jkmr/': 982,
        # 'http://jiankang.haiwainet.cn/jkmr/index.html': 1054,
        'http://jiankang.haiwainet.cn/zhyl/': 983,
        # 'http://jiankang.haiwainet.cn/zhyl/index.html': 1052,
        'http://jiankang.haiwainet.cn/tbbd/': 984,
        # 'http://jiankang.haiwainet.cn/tbbd/index.html': 1053,
        'http://qiaojie.haiwainet.cn/furg/': 985,
        # 'http://qiaojie.haiwainet.cn/furg/index.html': 1051,
        'http://qiaojie.haiwainet.cn/wljy/': 986,
        # 'http://qiaojie.haiwainet.cn/wljy/index.html': 1048,
        'http://qiaojie.haiwainet.cn/hrfc/': 987,
        # 'http://qiaojie.haiwainet.cn/hrfc/index.html': 1049,
        'http://shengtai.haiwainet.cn/stxf/': 988,
        # 'http://shengtai.haiwainet.cn/stxf/index.html': 1047,
        'http://shengtai.haiwainet.cn/stsp/': 989,
        # 'http://shengtai.haiwainet.cn/stsp/index.html': 1046,
        'http://shengtai.haiwainet.cn/stcy/': 990,
        # 'http://shengtai.haiwainet.cn/stcy/index.html': 1042,
        'http://shengtai.haiwainet.cn/stjy/': 991,
        # 'http://shengtai.haiwainet.cn/stjy/index.html': 1043,
        'http://shengtai.haiwainet.cn/mlzg/': 992,
        # 'http://shengtai.haiwainet.cn/mlzg/index.html': 1045,
        'http://shengtai.haiwainet.cn/stlt/': 993,
        # 'http://shengtai.haiwainet.cn/stlt/index.html': 1044,
        'http://shengtai.haiwainet.cn/lsjr/': 994,
        # 'http://shengtai.haiwainet.cn/lsjr/index.html': 1041,
        'http://shengtai.haiwainet.cn/gjjl/': 995,
        # 'http://shengtai.haiwainet.cn/gjjl/index.html': 1040,
        'http://shengtai.haiwainet.cn/rdzt/': 996,
        # 'http://shengtai.haiwainet.cn/rdzt/index.html': 1039,
        'http://shengtai.haiwainet.cn/sxyw/': 997,
        # 'http://shengtai.haiwainet.cn/sxyw/index.html': 1037,
        'http://nengyuan.haiwainet.cn/nyjs/': 998,  # ok
        'http://chanjing.haiwainet.cn/whly/': 999,  # ok
        'http://chanjing.haiwainet.cn/zxsd/': 1000,
        # 'http://chanjing.haiwainet.cn/zxsd/index.html': 1038,
        'http://chanjing.haiwainet.cn/xwjj/': 1001,
        'http://ziyuan.haiwainet.cn/kejichuangxin/': 1002,
        # 'http://ziyuan.haiwainet.cn/kejichuangxin/index.html': 1036,
        'http://ziyuan.haiwainet.cn/nongyenongcun/': 1003,
        # 'http://ziyuan.haiwainet.cn/nongyenongcun/index.html': 1035,
        'http://ziyuan.haiwainet.cn/ziranziyuan/': 1004,  # ok
        'http://ziyuan.haiwainet.cn/wenhualvyou/': 1005,
        # 'http://ziyuan.haiwainet.cn/wenhualvyou/index.html': 1034,
        'http://ziyuan.haiwainet.cn/shianjiankang/': 1006,
        # 'http://ziyuan.haiwainet.cn/shianjiankang/index.html': 1033,
        'http://ziyuan.haiwainet.cn/jiaotongyunshu/': 1007,
        # 'http://ziyuan.haiwainet.cn/jiaotongyunshu/index.html': 1032,
        'http://ziyuan.haiwainet.cn/shengtaihuanbao/': 1008,
        # 'http://ziyuan.haiwainet.cn/shengtaihuanbao/index.html': 1029,
        'http://ziyuan.haiwainet.cn/pinpaizhongguo/': 1009,
        'http://ziyuan.haiwainet.cn/chanyejingji/': 1010,
        # 'http://ziyuan.haiwainet.cn/chanyejingji/index.html': 1031,
        'http://ziyuan.haiwainet.cn/tebieguanzhu/': 1011,
        # 'http://ziyuan.haiwainet.cn/tebieguanzhu/index.html': 1028,
        'http://ziyuan.haiwainet.cn/yinxiangzhongguo/': 1012,
        # 'http://ziyuan.haiwainet.cn/yinxiangzhongguo/index.html': 1027,
        'http://ziyuan.haiwainet.cn/yaowen/': 1013,
        # 'http://ziyuan.haiwainet.cn/yaowen/index.html': 1026,
        'http://jingmao.haiwainet.cn/gxyq/': 1014,  # ok
        
        'http://shenlan.haiwainet.cn/cbdx/': 1016,  # ok
        'http://shenlan.haiwainet.cn/kjjk/': 1017,  # ok
        'http://shenlan.haiwainet.cn/slts/': 1019,  # ok
        'http://shenlan.haiwainet.cn/slvs/': 1020,  # ok
        'http://shenlan.haiwainet.cn/lsmx/': 1021,  # ok
        'http://shenlan.haiwainet.cn/lsjj/': 1022,  # ok
        'http://shenlan.haiwainet.cn/sltt/': 1023,  # ok
        'http://shenlan.haiwainet.cn/llsj/': 1024,  # ok
        'http://wenyi.haiwainet.cn/mingjiazatan/': 1025,  # ok
        'http://ziyuan.haiwainet.cn/zuolichengshi/index.html': 1030,  # ok
        'http://qiaojie.haiwainet.cn/qwqx/index.html': 1050,
        'http://jiankang.haiwainet.cn/zyzy/index.html': 1056,
        'http://jiankang.haiwainet.cn/jkxz/index.html': 1057,
        'http://jiankang.haiwainet.cn/bzyrz/index.html': 1058,
        'http://nanhai.haiwainet.cn/play/lvyouzixun/': 1066,
        # 'http://nanhai.haiwainet.cn/play/lvyouzixun/index.html': 1135,
        'http://pinpai.haiwainet.cn/ppzf/index.html': 1072,
        'http://tw.haiwainet.cn/scroll-news/taiwan/': 1078,
        # 'http://tw.haiwainet.cn/scroll-news/taiwan/index.html': 1134,
        'http://finance.haiwainet.cn/redianjujiao/index.html': 1088,
        'http://sannong.haiwainet.cn/457134/index.html': 1092,
        'http://chuangxin.haiwainet.cn/348213/index.html': 1094,
        'http://renwen.haiwainet.cn/csgy/index.html': 1100,
        'http://renwen.haiwainet.cn/ctwh/index.html': 1101,
        'http://renwen.haiwainet.cn/hrtx/index.html': 1102,
        'http://renwen.haiwainet.cn/sjyc/index.html': 1103,
        'http://renwen.haiwainet.cn/ppgs/index.html': 1105,
        'http://haisi.haiwainet.cn/fazhi/index.html': 1114,
        'http://huashang.haiwainet.cn/zhuanti/index.html': 1123,
        'http://haisi.haiwainet.cn/redianxinwen/index.html': 1124,
    }
    # http://opinion.haiwainet.cn/n/2019/0304/c345415-31507616.html
    rules = (
        Rule(LinkExtractor(allow=(r'haiwainet.cn/n/%s\d{2}/c\d+-\d+.html' % datetime.today().strftime('%Y/%m'),),
                           # http://v.haiwainet.cn/n/2019/0425/c346113-31544732.html
                           deny=r'v.haiwainet.cn/'),  # 排除视频
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'haiwainet.cn.*?\d{6,}.html',),
                           deny=(r'v.haiwainet.cn/', r'/201[0-8]', r'/20190[1-9]/')),
             process_request=otherurl_meta, follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            # <meta name="publishdate" content="2019-04-25 09:11:47">
            pubtime = xp('//head/meta[@name="publishdate"]/@content').extract_first('')
            if not pubtime:
                source_div = xp('//div[contains(@class,"show_text")]//span[@class="first"]')
                pubtime = source_div[0].re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')[0]
            
                
            # <meta name="source" content="来源：央视网">
            origin_name = xp('//head/meta[@name="source"]/@content').extract_first("")
            
            cvs = xp('//div[@class="contentMain"]') or xp('//div[@id="cen"]')
            content_div = cvs[0]
        
        except:
            return self.parse_item_2(response)

        content, media, videos, cover = self.content_clean(content_div, kill_xpaths=[])
        
        return self.produce_item(
            response=response,
            title=xp('//h1/text()').extract_first('') or self.get_page_title(response).split('-')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item_2(self, response):
        # http://world.haiwainet.cn/n/2019/0411/c3541003-31534745.html
        xp = response.xpath
        try:
            pubtime = xp('//head/meta[@name="publishdate"]/@content').extract_first('')
            if not pubtime:
                pubtime = xp('//div[@class="show_jintai")]//span[@class="time"]/text()').extract_first('')
            
            origin_name = xp('//head/meta[@name="source"]/@content').extract_first("")
            cv = xp('//div[@class="show_jintai"]')[0]
            content_div = cv.xpath('./p')
            content, media, videos, cover = self.content_clean(content_div, kill_xpaths=[])
        except:
            return self.parse_images(response)

        return self.produce_item(
            response=response,
            title=xp('//h1/text()').extract_first('') or self.get_page_title(response).split('-')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_images(self, response):
        xp = response.xpath
        try:
            pubtime = xp('//head/meta[@name="publishdate"]/@content').extract_first('')
            if not pubtime:
                source_div = xp('.//div[@class="newsMess"]') or xp(
                    '//div[contains(@class,"show_text")]//span[@class="first"]')
                pubtime = source_div[0].re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')[0]
            
            rt = xp('.//body')[0].extract()
            m = re.search(r"picData='\[.*?\]'", rt)
            p = m.group()
            news_imgs_str = p.replace("picData=", "").replace(",]", "]")
            news_json = json.loads(eval(news_imgs_str))
            media = {}
            new_content = ''
            
            for i, j in enumerate(news_json):
                media.setdefault("images", {})
                src = j['src']
                media["images"][str(i + 1)] = {"src": src}
                new_content += '${{%s}}$<p>%s</p>' % ((i + 1), j['alt'])
        except:
            return self.produce_debugitem(response, "xpath error")
        
        return self.produce_item(
            response=response,
            title=xp('//h1/text()').extract_first('') or self.get_page_title(response).split('-')[0],
            # '大熊猫“园园”启程前往奥地利 - 图片 - 海外网
            pubtime=pubtime,
            origin_name=xp('//head/meta[@name="source"]/@content').extract_first(""),
            content=new_content,
            media=media
        )


class HaiWaiNetPageSpider(HaiWaiNetSpider):
    """海外网_翻页"""
    name = 'haiwainet_page'
    mystart_urls = {
        'http://www.haiwainet.cn/roll/': 492,  # 海外网滚动
        # 'http://www.haiwainet.cn/roll/index.html': 906,  # 和492网址相同
    }
    # http://opinion.haiwainet.cn/n/2019/0304/c345415-31507616.html        http://www.haiwainet.cn/roll/10.html
    rules = (
        Rule(LinkExtractor(allow=r'haiwainet.cn/n/%s\d{2}/c\d+-\d+.html' % datetime.today().strftime('%Y/%m'),
                           deny=r'v.haiwainet.cn/'),  # 排除视频),
                                callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'haiwainet\.cn/roll/.*?\d+\.html',
                             restrict_xpaths='//div[@class="w650 fl"]/p[@class="mclp1"]//a[text()="下一页"]'),
               follow=True, process_request=isStartUrl_meta)
    )
    
    custom_settings = {
        'DEPTH_LIMIT': 3,  # 不能设置为0防止request队列太长
        # 和父spider一起去重
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % HaiWaiNetSpider.name,
        # 禁止重定向
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
