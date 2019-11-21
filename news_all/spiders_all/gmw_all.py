#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 11:32
# @Author  : wjq
# @File    : gmw_all.py
from copy import deepcopy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import isStartUrl_meta
from news_all.spiders.gmw import GmwSpider


class GmwAllSpider(GmwSpider):
    """光明网_all"""
    name = 'gmw_all'
    mystart_urls = {
        'http://culture.gmw.cn/node_10250.htm': 1076, 'http://culture.gmw.cn/node_10565.htm': 1136,
        'http://culture.gmw.cn/node_10570.htm': 1137, 'http://culture.gmw.cn/node_10572.htm': 1138,
        'http://culture.gmw.cn/node_10575.htm': 1139, 'http://culture.gmw.cn/node_11507.htm': 1140,
        'http://culture.gmw.cn/node_4369.htm': 1141, 'http://culture.gmw.cn/node_4455.htm': 1142,
        'http://culture.gmw.cn/node_9670.htm': 1143, 'http://dangjian.gmw.cn/node_10207.htm': 1144,
        'http://dangjian.gmw.cn/node_11924.htm': 1146, 'http://dangjian.gmw.cn/node_11928.htm': 1148,
        'http://dangjian.gmw.cn/node_11929.htm': 1149, 'http://dangjian.gmw.cn/node_11936.htm': 1150,
        'http://dangjian.gmw.cn/node_11938.htm': 1151, 'http://dangjian.gmw.cn/node_11940.htm': 1152,
        'http://dangjian.gmw.cn/node_11941.htm': 1155, 'http://dangjian.gmw.cn/node_22417.htm': 1156,
        'http://e.gmw.cn/node_10798.htm': 1157, 'http://e.gmw.cn/node_110454.htm': 1158,
        'http://e.gmw.cn/node_7511.htm': 1159, 'http://e.gmw.cn/node_7516.htm': 1161,
        'http://e.gmw.cn/node_8753.htm': 1162, 'http://economy.gmw.cn/node_12470.htm': 1166,
        'http://economy.gmw.cn/node_21787.htm': 1167, 'http://economy.gmw.cn/node_8969.htm': 1168,
        'http://economy.gmw.cn/node_8971.htm': 1169, 'http://edu.gmw.cn/node_10602.htm': 1170,
        'http://edu.gmw.cn/node_10810.htm': 1171, 'http://edu.gmw.cn/node_9729.htm': 1172,
        'http://edu.gmw.cn/node_9737.htm': 1173, 'http://edu.gmw.cn/node_9746.htm': 1174,
        'http://edu.gmw.cn/node_9757.htm': 1175, 'http://feiyi.gmw.cn/node_115940.htm': 1176,
        'http://feiyi.gmw.cn/node_115941.htm': 1177, 'http://gmw.cn/index/node_4841.htm': 1178,
        'http://gongyi.gmw.cn/node_37842.htm': 1179, 'http://gongyi.gmw.cn/node_37844.htm': 1180,
        'http://gongyi.gmw.cn/node_37846.htm': 1181, 'http://guancha.gmw.cn/node_117767.htm': 1182,
        'http://guancha.gmw.cn/node_26274.htm': 1183, 'http://guancha.gmw.cn/node_7292.htm': 1184,
        'http://guancha.gmw.cn/node_87838.htm': 1185, 'http://health.gmw.cn/node_24189.htm': 1186,
        'http://health.gmw.cn/node_9583.htm': 1187, 'http://it.gmw.cn/node_29390.htm': 1188,
        'http://it.gmw.cn/node_29409.htm': 1189, 'http://it.gmw.cn/node_29412.htm': 1190,
        'http://it.gmw.cn/node_4487.htm': 1191, 'http://it.gmw.cn/node_5972.htm': 1192,
        'http://it.gmw.cn/node_6060.htm': 1193, 'http://it.gmw.cn/node_6061.htm': 1194,
        'http://junshi.gmw.cn/node_121246.htm': 1195, 'http://junshi.gmw.cn/node_90294.htm': 1196,
        'http://kepu.gmw.cn/node_87685.htm': 1197, 'http://lady.gmw.cn/node_33671.htm': 1198,
        'http://lady.gmw.cn/node_33738.htm': 1199, 'http://legal.gmw.cn/node_9015.htm': 1200,
        'http://legal.gmw.cn/node_9020.htm': 1201, 'http://legal.gmw.cn/node_9668.htm': 1202,
        'http://life.gmw.cn/node_115918.htm': 1203, 'http://life.gmw.cn/node_9251.htm': 1204,
        'http://life.gmw.cn/node_9252.htm': 1205, 'http://life.gmw.cn/node_9261.htm': 1206,
        'http://life.gmw.cn/node_9265.htm': 1207, 'http://life.gmw.cn/node_9268.htm': 1208,
        'http://life.gmw.cn/node_9269.htm': 1209, 'http://life.gmw.cn/node_9682.htm': 1210,
        'http://m.gmw.cn/node_103483.htm': 1211, 'http://meiwen.gmw.cn/node_23777.htm': 1213,
        'http://meiwen.gmw.cn/node_24064.htm': 1214, 'http://meiwen.gmw.cn/node_24065.htm': 1215,
        'http://meiwen.gmw.cn/node_24075.htm': 1216, 'http://mil.gmw.cn/node_8982.htm': 1217,
        'http://mil.gmw.cn/node_8984.htm': 1221, 'http://mil.gmw.cn/node_8986.htm': 1223,
        'http://mil.gmw.cn/node_8988.htm': 1224, 'http://mil.gmw.cn/node_9664.htm': 1225,
        'http://museum.gmw.cn/node_115788.htm': 1227, 'http://museum.gmw.cn/node_115789.htm': 1228,
        'http://museum.gmw.cn/node_115790.htm': 1229, 'http://news.gmw.cn/node_23545.htm': 1230,
        'http://news.gmw.cn/node_23547.htm': 1231, 'http://news.gmw.cn/node_23548.htm': 1232,
        'http://news.gmw.cn/node_23707.htm': 1233, 'https://news.gmw.cn/node_23708.htm': 1234,
        'https://news.gmw.cn/node_23709.htm': 1235, 'http://photo.gmw.cn/node_10442.htm': 1236,
        'http://photo.gmw.cn/node_65800.htm': 1237, 'http://politics.gmw.cn/node_10495.htm': 1238,
        'http://politics.gmw.cn/node_23717.htm': 1239, 'http://politics.gmw.cn/node_26858.htm': 1240,
        'http://politics.gmw.cn/node_9826.htm': 1241, 'http://politics.gmw.cn/node_9831.htm': 1242,
        'http://politics.gmw.cn/node_9836.htm': 1243, 'http://politics.gmw.cn/node_9838.htm': 1244,
        'http://politics.gmw.cn/node_9840.htm': 1245, 'http://politics.gmw.cn/node_9843.htm': 1246,
        'http://politics.gmw.cn/node_9844.htm': 1247, 'http://reader.gmw.cn/node_4244.htm': 1248,
        'http://reader.gmw.cn/node_5547.htm': 1249, 'http://reader.gmw.cn/node_9139.htm': 1250,
        'http://shuhua.gmw.cn/node_10673.htm': 1251, 'http://shuhua.gmw.cn/node_9004.htm': 1252,
        'http://sports.gmw.cn/node_9636.htm': 1253, 'http://sports.gmw.cn/node_9638.htm': 1254,
        'http://sports.gmw.cn/node_9641.htm': 1255, 'http://sports.gmw.cn/node_9644.htm': 1256,
        'http://tech.gmw.cn/jd/index.htm': 1257, 'http://tech.gmw.cn/jd/node_39857.htm': 1258,
        'http://tech.gmw.cn/node_10609.htm': 1259, 'http://tech.gmw.cn/node_10617.htm': 1260,
        'http://tech.gmw.cn/node_4394.htm': 1261, 'http://tech.gmw.cn/node_9671.htm': 1262,
        'http://theory.gmw.cn/node_10133.htm': 1263, 'http://theory.gmw.cn/node_10139.htm': 1268,
        'http://theory.gmw.cn/node_10141.htm': 1269, 'http://theory.gmw.cn/node_10145.htm': 1270,
        'http://theory.gmw.cn/node_101633.htm': 1271, 'http://theory.gmw.cn/node_41267.htm': 1272,
        'http://theory.gmw.cn/node_4227.htm': 1273, 'http://theory.gmw.cn/node_4403.htm': 1274,
        'http://theory.gmw.cn/node_47530.htm': 1275, 'http://topics.gmw.cn/node_115823.htm': 1276,
        'http://topics.gmw.cn/node_117662.htm': 1277, 'http://travel.gmw.cn/node_23658.htm': 1278,
        'http://travel.gmw.cn/node_9126.htm': 1279, 'http://travel.gmw.cn/node_9130.htm': 1280,
        'http://wenyi.gmw.cn/node_84175.htm': 1281, 'http://wenyi.gmw.cn/node_84176.htm': 1282,
        'http://wenyi.gmw.cn/node_84177.htm': 1283, 'http://wenyi.gmw.cn/node_84178.htm': 1284,
        'http://wenyi.gmw.cn/node_84179.htm': 1285, 'http://wenyi.gmw.cn/node_84239.htm': 1286,
        'http://wenyi.gmw.cn/node_87905.htm': 1287, 'http://world.gmw.cn/node_24177.htm': 1288,
        'http://world.gmw.cn/node_24178.htm': 1289, 'http://world.gmw.cn/node_24179.htm': 1290,
        'http://world.gmw.cn/node_4485.htm': 1291, 'http://world.gmw.cn/node_4660.htm': 1292,
        'http://world.gmw.cn/node_4661.htm': 1293, 'http://world.gmw.cn/node_4696.htm': 1295,
        'http://world.gmw.cn/node_8858.htm': 107,  # 1297,
        'http://world.gmw.cn/node_9663.htm': 1298,
        'http://www.gmw.cn/index/node_11225.htm': 1299, 'http://www.gmw.cn/index/node_4841.htm': 1300,
        'http://www.gmw.cn/xueshu/node_118122.htm': 1301, 'http://www.gmw.cn/xueshu/node_118214.htm': 1302,
        'http://www.gmw.cn/xueshu/node_118216.htm': 1303, 'http://www.gmw.cn/xueshu/node_23639.htm': 1304,
        'http://yangsheng.gmw.cn/node_12206.htm': 1305, 'http://yangsheng.gmw.cn/node_12207.htm': 1307,
        'http://yangsheng.gmw.cn/node_12212.htm': 1308, 'http://zhongyi.gmw.cn/node_118363.htm': 1309,
        'https://news.gmw.cn/node_23545.htm': 1310,
        'https://news.gmw.cn/node_23547.htm': 1311,
        'https://news.gmw.cn/node_23548.htm': 1312,
        'https://news.gmw.cn/node_23707.htm': 1313,
    }
    # http://sports.gmw.cn/2019-02/28/content_32582948.htm
    rules = (
        Rule(LinkExtractor(allow=(r'.gmw\.cn/%s/\d{2}/content_\d+\.htm' % datetime.today().strftime('%Y-%m'),),
                           deny=r'topics.gmw.cn'), callback='parse_item', follow=False),
        # 翻页  http://politics.gmw.cn/node_9840_3.htm
        Rule(LinkExtractor(allow=(r'.gmw\.cn/node_\d+_\d+\.htm',),
                           restrict_xpaths='//*[@id="displaypagenum"]/center/a[text()="下一页"]'), follow=True,
             process_request=isStartUrl_meta),
    )
    custom_settings = deepcopy(GmwSpider.custom_settings)
    custom_settings.update(
        {
            'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
            "SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % GmwSpider.name,
        }
    )