#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/22 15:46
# @Author  : wjq
# @File    : ifeng_wap.py


import json
from scrapy import Request
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings


class IfengWapSpider(NewsRSpider):
    chinese_name = """凤凰新闻app"""
    name = 'ifeng_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        'https://api.iclient.ifeng.com/nlist?id=19METTING&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772175670&sn=9c6d0dfc919dbff2c9d23bcb0bd581fc&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2691,
        'https://api.iclient.ifeng.com/nlist?id=19METTING&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580788782322&sn=47cdebf4389e0dab26b5e60f487d9376&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2692,
        'https://api.iclient.ifeng.com/nlist?id=BLOCKCHAIN,FOCUSBLOCKCHAIN&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580774665780&sn=8e5ee5c4a3bcddac44e530c407a31665&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2696,
        'https://api.iclient.ifeng.com/nlist?id=BLOCKCHAIN,FOCUSBLOCKCHAIN&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789202531&sn=75f6aa596393c764d294b262b9445bd6&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2727,
        'https://api.iclient.ifeng.com/nlist?id=CIRCLEHOT&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772815091&sn=2608c26805d6380aabb4b14fe7672136&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2729,
        'https://api.iclient.ifeng.com/nlist?id=CJ33,FOCUSCJ33,HNCJ33&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580759325660&sn=cdce867c46b810bfaea8607498fc6942&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2737,
        'https://api.iclient.ifeng.com/nlist?id=CJ33,FOCUSCJ33,HNCJ33&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580759325660&sn=cdce867c46b810bfaea8607498fc6942&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2788,
        'https://api.iclient.ifeng.com/nlist?id=COLLECT&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580774857198&sn=72b582b9d2b6fbee7af198dbca555114&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2789,
        'https://api.iclient.ifeng.com/nlist?id=DELIC,FOCUSDELIC&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580783606386&sn=de3c93088cab27e2b90b39778eb2f27f&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2791,
        'https://api.iclient.ifeng.com/nlist?id=DELIC,FOCUSDELIC&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580783606386&sn=de3c93088cab27e2b90b39778eb2f27f&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2792,
        'https://api.iclient.ifeng.com/nlist?id=DS57,FOCUSDS57&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789284282&sn=a4ffc50888ba02c8aa0d65ab59af5483&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2797,
        'https://api.iclient.ifeng.com/nlist?id=DYPD&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580780912739&sn=5906517119001c09aff7fd338122c986&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2807,
        'https://api.iclient.ifeng.com/nlist?id=DYPD&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580780935866&sn=80bbc52e8dcbda224b3f625e4c8cb04a&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2817,
        'https://api.iclient.ifeng.com/nlist?id=DZPD,FOCUSDZPD&page=1&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772339870&sn=e2406c23ef3f7193e5edbc68d4aec590&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2825,
        'https://api.iclient.ifeng.com/nlist?id=F1MATCH,FOCUSF1MATCH&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580774768756&sn=3a36003ae642ef4eca086681cdc47d23&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2844,
        'https://api.iclient.ifeng.com/nlist?id=F1MATCH,FOCUSF1MATCH&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789067624&sn=c45fdf9dcf4394df851da803ecb46a1d&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2845,
        'https://api.iclient.ifeng.com/nlist?id=FHYX,FOCUSFHYX&page=1&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580783619295&sn=95e26435f673cbde3486a38d278df595&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2846,
        'https://api.iclient.ifeng.com/nlist?id=FYXA21,FOCUSFYXA21&page=1&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580774742718&sn=60160f563ab253cdbde3adaf6edf3c36&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2851,
        'https://api.iclient.ifeng.com/nlist?id=GA18,FOCUSGA18&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789242769&sn=342efa38215c4e9b04906925e66279e0&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2859,
        'https://api.iclient.ifeng.com/nlist?id=GA18,FOCUSGA18&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789247505&sn=27ae824a4303f74b6b6d2468f5544c1b&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2879,
        'https://api.iclient.ifeng.com/nlist?id=GGKFPD&page=1&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580774575573&sn=8de7afc5c0bc22da25a0c7741990b0a6&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2919,
        'https://api.iclient.ifeng.com/nlist?id=GJPD,FOCUSGJPD&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772783360&sn=5eea8d3d021066f0a17674fd5764aa35&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2937,
        'https://api.iclient.ifeng.com/nlist?id=GJPD,FOCUSGJPD&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772798463&sn=3cc9864293a42a79aea7a70c0bdf684b&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2938,
        'https://api.iclient.ifeng.com/nlist?id=GXPD,FOCUSGXPD&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580783629535&sn=d2911d6dafed4173e8a44c01d073d0c3&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 2941,
        'https://api.iclient.ifeng.com/nlist?id=GXPD,FOCUSGXPD&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580783645483&sn=33e10b041b4e8092d9d14b57c80bc914&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3080,
        'https://api.iclient.ifeng.com/nlist?id=HEALTHLIVE&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772975806&sn=e629fbea6dbf3a1a795a85800bcec846&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3081,
        'https://api.iclient.ifeng.com/nlist?id=HEALTHLIVE&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772986045&sn=f796ff4dbb98eea0b388e617aaa4a935&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3082,
        'https://api.iclient.ifeng.com/nlist?id=HKSTOCKS,FOCUSHKSTOCKS&page=1&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580774791008&sn=eef5e03c1333f10b09c32099c087db5a&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3083,
        'https://api.iclient.ifeng.com/nlist?id=JK36&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772834126&sn=eb9ac27c7cb9dca8ee7a340a6329234d&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3095,
        'https://api.iclient.ifeng.com/nlist?id=JK36&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772838186&sn=44b1b8d8792d137b1410a7cd1cb5da3f&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3096,
        'https://api.iclient.ifeng.com/nlist?id=JS83,FOCUSJS83&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772274849&sn=ec753072b555846cec4d387e04337449&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3097,
        'https://api.iclient.ifeng.com/nlist?id=JS83,FOCUSJS83&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772288582&sn=0b24efb4ebba872fec8d95b7f725463f&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3098,
        'https://api.iclient.ifeng.com/nlist?id=JY90&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580783583702&sn=ff89c5606fbc8e3f8c1949421443713f&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3107,
        'https://api.iclient.ifeng.com/nlist?id=JYPD,FOCUSJYPD&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580788039247&sn=c2b965abbaf10cfd384d2dbcf754cd61&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3108,
        'https://api.iclient.ifeng.com/nlist?id=JYPD,FOCUSJYPD&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789372703&sn=2d29f59244bee769c203e26b5129e4ad&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3109,
        'https://api.iclient.ifeng.com/nlist?id=KJ123,FOCUSKJ123,SECNAVKJ123&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772305902&sn=5fe4e3acad3b97a4f6bd947415cb07dc&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3110,
        'https://api.iclient.ifeng.com/nlist?id=KJ123,FOCUSKJ123,SECNAVKJ123&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772327509&sn=9378a89d1a61c4e7d17cba2313c79396&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3111,
        'https://api.iclient.ifeng.com/nlist?id=KJ5G&page=1&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772432397&sn=6d64ea236342e579cc9371501faeede0&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3112,
        'https://api.iclient.ifeng.com/nlist?id=KJCKJ,FOCUSKJCKJ&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580774718865&sn=6b5ff00f75bb685686b72c7ae63a4c3e&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3113,
        'https://api.iclient.ifeng.com/nlist?id=KJCKJ,FOCUSKJCKJ&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580781514432&sn=851b299430c44e726810bae50d1d1acc&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3114,
        'https://api.iclient.ifeng.com/nlist?id=LS153,FOCUSLS153&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772517768&sn=3c20eb744df5ae0be36b9b532cf08316&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3115,
        'https://api.iclient.ifeng.com/nlist?id=LS153,FOCUSLS153&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772523145&sn=e709f97f07a89a44953cb8258291c8e1&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3116,
        'https://api.iclient.ifeng.com/nlist?id=LY67,FOCUSLY67,SECNAVLY67&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772895199&sn=e455c68a5fff1df3bdd9ab33df25ab0f&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3117,
        'https://api.iclient.ifeng.com/nlist?id=LY67,FOCUSLY67,SECNAVLY67&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772903077&sn=66ddb2ed1b56c07b87e1659cd823a854&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3118,
        'https://api.iclient.ifeng.com/nlist?id=MATERIAL&page=1&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772542590&sn=df44b5d0e5cca89b9bdfa4c581a5ca65&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3119,
        'https://api.iclient.ifeng.com/nlist?id=MENGCHONG,FOCUSMENGCHONG&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580775028663&sn=f005a541841b0703001749941f908c29&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3121,
        'https://api.iclient.ifeng.com/nlist?id=MENGCHONG,FOCUSMENGCHONG&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580775032033&sn=00956d22e50f86b109b0d80d68f51474&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3124,
        'https://api.iclient.ifeng.com/nlist?id=NBAPD,FOCUSNBAPD&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580774971551&sn=adfaaef5a7004b12204277b64d721b75&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3126,
        'https://api.iclient.ifeng.com/nlist?id=NBAPD,FOCUSNBAPD&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580774999046&sn=b67ee325be28726a37b01b123fab528c&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3129,
        'https://api.iclient.ifeng.com/nlist?id=NXWPD,FOCUSNXWPD&page=1&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772689058&sn=a8f4f3c8737aa3cf7b0c5823c6aead71&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3131,
        'https://api.iclient.ifeng.com/nlist?id=PARENT&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772998618&sn=226283f6c6a1a217a715ba233aebf281&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3132,
        'https://api.iclient.ifeng.com/nlist?id=PARENT&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580783177412&sn=02e3a698e282f3df30f455bbe4068f7a&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3133,
        'https://api.iclient.ifeng.com/nlist?id=PBPD,PBPDFOCUS&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789359146&sn=f15e5e9565474e5a56a7330c64b6f584&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3134,
        'https://api.iclient.ifeng.com/nlist?id=PBPD,PBPDFOCUS&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789366529&sn=80ac3e3cfb33db613a1137983c4bd927&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3136,
        'https://api.iclient.ifeng.com/nlist?id=PICPD&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772851890&sn=b520d30b165aa6e1239ee74c1de448de&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3137,
        'https://api.iclient.ifeng.com/nlist?id=PICPD&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772861330&sn=4a0f0fd90a9a27df937f9452eb3037e1&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3139,
        'https://api.iclient.ifeng.com/nlist?id=PL40,FOCUSPL40&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789324823&sn=05d36efefa10028f7c740026c4758b63&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3140,
        'https://api.iclient.ifeng.com/nlist?id=PL40,FOCUSPL40&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789346207&sn=da20b65a6f46afe7605c540ec978e434&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3141,
        # 'https://api.iclient.ifeng.com/nlist?id=RECOMVIDEO&action=up&pullNum=1&timestamp=2019%2F05%2F17+11%3A08%3A09&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772071013&sn=05d2b2a68406d37ecd90333b9e562846&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3143,
        # 'https://api.iclient.ifeng.com/nlist?id=RECOMVIDEO&action=down&pullNum=1&timestamp=2019%2F05%2F17+11%3A08%3A09&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580788529777&sn=69c62b723d64f5b7a2846f16686e308c&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3144,
        'https://api.iclient.ifeng.com/nlist?id=SDJT,FOCUSSDJT&page=1&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772212698&sn=ade731b0e1606ff60221339b21709061&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3146,

        'https://api.iclient.ifeng.com/nlist?id=SM66,FOCUSSM66&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789225063&sn=39df430d871a39a103df8c6fa79c41cc&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3151,
        'https://api.iclient.ifeng.com/nlist?id=SM66,FOCUSSM66&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789238968&sn=59073276e2a15b8ead641af68989eb8e&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3152,
        'https://api.iclient.ifeng.com/nlist?id=SS78,FOCUSSS78,SECNAVSS78&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772879650&sn=5c8f87ca6b720c6947ac87c6f2c8e9ac&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3153,
        'https://api.iclient.ifeng.com/nlist?id=SS78,FOCUSSS78,SECNAVSS78&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772886282&sn=f1605549c5245fc6c6f2290e29a587c4&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3154,
        'https://api.iclient.ifeng.com/nlist?id=SYLB10,SYDT10&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772027191&sn=69797faddcf2cb80453c6ca6328d48f8&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3155,
        'https://api.iclient.ifeng.com/nlist?id=TW73,FOCUSTW73&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580788707673&sn=94d75656569d1c18990a0cba7c0b76fc&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3157,
        'https://api.iclient.ifeng.com/nlist?id=TY43,FOCUSTY43,TYTOPIC&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772471546&sn=ba0517e03b64c9d13f1b72f46a7abbd3&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3158,
        'https://api.iclient.ifeng.com/nlist?id=TY43,FOCUSTY43,TYTOPIC&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772494907&sn=1dccfd130ba4a9e65c7272ca20334a07&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3159,
        'https://api.iclient.ifeng.com/nlist?id=VAMPIRE,FOCUSVAMPIRE,SECNAVVAMPIRE&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772916010&sn=b16d50e3f87bd106e1534865982d76a0&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3160,
        'https://api.iclient.ifeng.com/nlist?id=VAMPIRE,FOCUSVAMPIRE,SECNAVVAMPIRE&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772936206&sn=6698b2fa65395b0c683c920fc0078b5e&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3161,
        # 'https://api.iclient.ifeng.com/nlist?id=VIDEOSHORT&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580773012678&sn=0748e71eba8da10b8b0e9a8f08796f6c&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3162,
        # 'https://api.iclient.ifeng.com/nlist?id=VIDEOSHORT&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580773025241&sn=f989ca53bf37293420b4fce086cd77e6&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3163,
        'https://api.iclient.ifeng.com/nlist?id=WH25,FOCUSWH25&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789261864&sn=b7ac456cb8bcbaf438fa0fb50a9144f8&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3164,
        'https://api.iclient.ifeng.com/nlist?id=WH25,FOCUSWH25&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789274739&sn=9a863c932367a286dde48d6bf5489848&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3165,
        'https://api.iclient.ifeng.com/nlist?id=XZ09,FOCUSXZ09&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789312010&sn=e6ce49eff6c19490329a30e2eb10b8da&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3166,
        'https://api.iclient.ifeng.com/nlist?id=XZ09,FOCUSXZ09&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789312359&sn=41fa568d4b54395ccd2e718e892c8c0e&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3167,
        'https://api.iclient.ifeng.com/nlist?id=YAOWEN223&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772606961&sn=9a28ee17a6c193a4da88a2727f8554d9&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3168,
        'https://api.iclient.ifeng.com/nlist?id=YAOWEN223&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772601236&sn=c363ed87771ff0d78489364d901fe176&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3169,
        'https://api.iclient.ifeng.com/nlist?id=YL53,FOCUSYL53,SECNAVYL53&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772129602&sn=771469bd0b35e1f8f17cc218ab54ebb6&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3171,
        'https://api.iclient.ifeng.com/nlist?id=YL53,FOCUSYL53,SECNAVYL53&action=down&pullNum=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580772149151&sn=7c78968acd8485bb303e82c1304f103f&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3173,
        'https://api.iclient.ifeng.com/nlist?id=YX11,FOCUSYX11&action=default&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580774774456&sn=667ea44b6ee431ad4f3d93ae61bf8b5a&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3174,
        'https://api.iclient.ifeng.com/nlist?id=ZHENGWUPD,FOCUSZHENGWUPD&page=1&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580789156178&sn=64d89327e726287ac15a7a6ac7d02dd0&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3176,
        'https://api.iclient.ifeng.com/nlist?id=ZNL345&page=1&gv=6.5.5&av=6.5.5&uid=861603035854842&deviceid=861603035854842&proid=ifengnews&os=android_23&df=androidphone&vt=5&screen=1080x1920&publishid=6001&nw=wifi&loginid=&st=15580783572342&sn=7760a57502cc1e8e26eaf85720a60318&dlt=39.927129&dln=116.480333&dcy=%E5%8C%97%E4%BA%AC%E5%B8%82&dpr=%E5%8C%97%E4%BA%AC%E5%B8%82': 3178,

    }
    #  [<twisted.python.failure.Failure OpenSSL.SSL.Error: [('SSL routines', 'ssl3_read_bytes', 'ssl handshake failure')]>]
    # todo 视频真实地址
    # http://42.81.104.1/video19.ifeng.com/video09/2019/05/21/p21151666-102-9987636-144143.mp4?vid=ce9b6c8f-fff3-4cb9-b1d7-2836dddd17c1
    # &uid=1538924117390_2cpfmg3830&from=v_Free&pver=vHTML5Player_v2.0.0
    # &sver=&se=%E6%88%91%E6%89%8D%E6%98%AF%E5%A5%B3%E4%B8%BB%E8%A7%92  # '我才是女主角'
    # &cat=&ptype=&platform=pc&sourceType=h5&dt=1558420826000&gid=y8CPAWrzgu1Z
    # &sign=18cf678cccf66cbf52e5b09e621064ee&tm=1558863605083
    # &vkey=%2FmNI4BGNhZjRJ0LV5OrtU6ZU1pfWdItk3MdJA%2BPVNYsuLzKeSwfV%2BltT1mw7HDFIJylXgArXmmCcLRFLnckqRtG7djMODAxkev1C0ziwvTelk9s4YJtRH%2B7VdOlTIp%2FkjmeuW5Mirz4qCZucV0sdHLNNFGn6hg7%2B%2BN6Z7c6XlDAkWUuYC6t0bii4F47PdPjyhfOpVSr3m07CEuFSrQXrFBZAR4FWs9mWFKmmn7PteoH3tV97JW96JoNZFgPeedUY%2FCm7Qz56IqFlnfPRSyokTviZh9UECObr6CtWzG%2FNkPr77bVNf%2BssTUxLZj3qT0C6
    """
       "link":{
        "type":"phvideo",
        "url":"ce9b6c8f-fff3-4cb9-b1d7-2836dddd17c1",
        "weburl":"https://ishare.ifeng.com/c/shareVideos/ce9b6c8f-fff3-4cb9-b1d7-2836dddd17c1?f=app",
        "vid":"ce9b6c8f-fff3-4cb9-b1d7-2836dddd17c1",
        "mp4":"http://ips.ifeng.com/video19.ifeng.com/video09/2019/05/21/p21151666-102-9987636-144143/index.m3u8?ifsign=1"
    },
    """

    def parse(self, response):
        rs = json.loads(response.text)
        for r in rs:
            items = r.get('item')

            for i in items:
                if i.get('type') == 'advert':  # 排除广告
                    continue

                """
                # style可能如下
                {
                    "view":"fastmessagescroll",
                    "backreason":[],
                    "defaultreason":"0_不感兴趣"
                },
                {
                    "attribute":"广告",
                    "backreason":[
                        "不感兴趣",
                        "虚假广告",
                        "看过了",
                        "档次太低"
                    ],
                    "defaultreason":"0_不感兴趣",
                    "view":"titleimg"
                },
                {'type': 'slides',
                'images': ['https://d.ifengimg.com/w230_h152_q100_aix29_aiy0_aiw712_aih471_webp/e0.ifengimg.com/09/2019/0520/2D4413BE105BB85E63D53280634355E876884819_size58_w755_h471.jpeg.webp',
                'https://d.ifengimg.com/w230_h152_q100_aix0_aiy17_aiw750_aih495_webp/e0.ifengimg.com/05/2019/0520/D971E3C4EFBC8EA500F3DE038A873933E0C297F4_size52_w750_h513.jpeg.webp',
                'https://d.ifengimg.com/w230_h152_q100_aix0_aiy17_aiw751_aih495_webp/e0.ifengimg.com/01/2019/0520/6678254D6CD98ADA683D068B8EDE126FF410951A_size39_w751_h513.jpeg.webp'],
                'backreason': ['0_来源:不凡智库', 'c_科技'],
                'defaultreason': '0_不感兴趣',
                'slideCount': 9,
                'view': 'slideimg'}
                """

                style = i.get('style')
                if style and style.get('attribute') == "广告":
                    continue
                """
                {
                    "type":"doc",
                    "url":"https://api.iclient.ifeng.com/getNewsDocs?aid=ucms_7msSL6WzkXE&channelKey=dWNtc19yZWNvbW1lbmRfNzUyMTk=&category=&imId=",
                    "weburl":"https://share.iclient.ifeng.com/shareNews?ch=qd_sdk_dl1&aid=ucms_7msSL6WzkXE",
                    "openType":"1"
                }
                """
                link = i.get('link')
                if link.get('type') == 'phvideo':
                    continue  # 排除视频
                print('link["type"]', link.get('type'))  # doc web slide topic2
                news_url = link.get('url')
                if not news_url:
                    print('no url, get weburl=%s' % (link.get('weburl')))  # todo check weburl是否有新闻可以xpath处理
                    continue
                if ':' not in news_url:
                    """
                    {'type': 'phvideo',
                     'url': '4878a77a-8a24-444b-948a-e2fbcfc094a4',
                      'weburl': 'https://ishare.ifeng.com/c/shareVideos/4878a77a-8a24-444b-948a-e2fbcfc094a4?f=app'}
                    """
                    if not link.get('weburl'):
                        print('have not url or weburl!')
                        continue
                    if "shareVideos" in link.get('weburl'):
                        continue
                    else:
                        print(': not in news_url=%s, weburl=%s' % (news_url, link.get('weburl')))
                        news_url = link.get('weburl')  # todo check是否有这种情况

                # 排除快讯http://finance.ifeng.com/gold/zhibo/m/index.shtml https://finance.ifeng.com/studio
                # 排除专题视频 https://api.iclient.ifeng.com/TopicApiForCmpp?topicid=360139&json=y
                if '/zhibo/' in news_url or news_url.endswith('studio') or 'topicid=' in news_url:
                    continue

                title = i.get('title')
                origin_name = i.get('source')

                pubtime = i.get('updateTime')
                yield Request(
                    url=news_url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                          'origin_name': origin_name,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )

    def parse_item(self, response):
        kill_xpaths = [r'//*[starts-with(text(),"【记者】")]',
                       r'//*[starts-with(text(),"【通讯员】")]',
                       r'//*[starts-with(text(),"【作者】")]',
                       r'//*[starts-with(text(),"【来源】")]',
                       r'//*[text()="相关阅读:"]/following::*',
                       r'//*[text()="相关阅读："]/following::*',
                       r'//*[text()="相关阅读:"]',
                       r'//*[text()="相关阅读："]',
                       # 关注同花顺财经微信公众号(ths518)，获取更多财经资讯
                       r'//*[re:match(text(),"关注\w{2,10}公众号")]'
                       ]
        try:
            rs = json.loads(response.text)
        except Exception as e:
            print(e)  # 状态码205
            return
        try:
            body = rs.get('body')
            if body.get('videos'):  # 排除视频
                return
            content_div = body.get('text')
            if content_div:
                content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=kill_xpaths)
            else:
                content_div = body.get('slides')
                content, media = self.make_img_content(content_div)

                content = self.parser.cleaner.clean_html(content, kill_xpaths=kill_xpaths)
        except:
            return self.produce_debugitem(response, 'json error')

        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            content=content,
            media=media
        )

    def make_img_content(self, img_cons):
        """拼接图、文列表为html
        # https://ishare.ifeng.com/c/s/7mnfFORqzyq
        [{
            "image":"https://d.ifengimg.com/mw640_q100/p1.ifengimg.com/2019_21/44F4EF8E5F71ABDC24A12C657B413B173520A5DE_w683_h1024.jpg",
            "title":"夺赛点！勇士大比分3-0开拓者 库里砍下36分",
            "description":"北京时间5月19日NBA2018-2019赛季季后赛继续进行，今天波特兰开拓者队回到主场迎来了与金州勇士队的系列赛三番战。最终，勇士队在一度落后18分的情况下以110比99又逆转战胜了开拓者队，至此，勇士队在杜兰特缺阵的情况下迎来了赛点。"
        },
        {
            "image":"https://d.ifengimg.com/mw640_q100/p0.ifengimg.com/2019_21/6BD50F9037B982E8E94EDEB2E59E421EA5C45938_w1024_h682.jpg",
            "title":"夺赛点！勇士大比分3-0开拓者 库里砍下36分",
            "description":"勇士：库里36分6个篮板3次助攻，格林20分13个篮板12次助攻，克莱19分5个篮板5次助攻，伊戈达拉2分5个篮板2次助攻，卢尼8分3个篮板，利文斯顿6分，贝尔6分2个篮板2次助攻。"
        },
        {
            "image":"https://d.ifengimg.com/mw640_q100/p1.ifengimg.com/2019_21/CDE4E08FD68D9DAFDA523B56E64C4D72C4E9CF20_w1024_h683.jpg",
            "title":"夺赛点！勇士大比分3-0开拓者 库里砍下36分",
            "description":"开拓者：麦科勒姆23分3个篮板5次助攻，利拉德18投5中得到19分6个篮板6次助攻，伦纳德16分。"
        },
        {
            "image":"https://d.ifengimg.com/mw640_q100/p0.ifengimg.com/2019_21/E66A29297A255F03F153172E496174CEE67CFF6C_w1024_h694.jpg",
            "title":"夺赛点！勇士大比分3-0开拓者 库里砍下36分",
            "description":"格林突破。"
        }
    ]
        """
        media = {'images': {}}
        content = ''
        for i, j in enumerate(img_cons):
            content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
            if j.get('description'):
                content += '<p>' + j['description'] + '</p>'

            media['images'][str(i + 1)] = {"src": j['image']}

        return content, media
