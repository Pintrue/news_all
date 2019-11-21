# -*- coding: utf-8 -*-

import json
import os
import jsonpath
from scrapy import Request
from news_all.spider_models import NewsRSpider
import re
from scrapy.conf import settings

ip = re.compile(r'\<\!--IMG#\d+--\>')
vp = re.compile(r'\<\!--VIDEO#\d+--\>')  # <!--VIDEO#0-->


class Wangyi163WapSpider(NewsRSpider):
    chinese_name = """网易app"""
    name = 'wangyi163_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}

    mystart_urls = {
        'http://c.m.163.com/dlist/article/dynamic?from=T1348649079062&offset=0&size=10&fn=2&devId=uU6bIcFeYHt14K2%2Bb79MKw%3D%3D': 1085,
        # 体育
        'http://c.m.163.com/dlist/article/dynamic?from=T1348648517839&offset=0&size=10&fn=2&devId=uU6bIcFeYHt14K2%2Bb79MKw%3D%3D': 1086,
        # 娱乐
        'http://c.m.163.com/dlist/article/dynamic?from=T1348649580692&offset=0&size=10&fn=2&devId=uU6bIcFeYHt14K2%2Bb79MKw%3D%3D': 1087,
        # 科技
        'http://c.m.163.com/dlist/article/dynamic?from=T1348648141035&offset=0&size=10&fn=2&devId=uU6bIcFeYHt14K2%2Bb79MKw%3D%3D': 1089,
        # 军事

        # 扩展的栏目 5月28日打标
        'https://c.m.163.com/nc/article/list/T1348649503389/0-20.html': 3515,
        'https://c.m.163.com/dlist/article/dynamic?from=T1348654151579&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975063&sign=b4QhGEuad%2BM%2B%2F4sdYc9YTsEJOA8hVAcyqMSZ8QTmivB48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3526,
        'https://c.m.163.com/dlist/article/dynamic?from=T1348648650048&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975197&sign=QSpcpWOSHSI2ZGeAO9VxW4z65lkgMo5pVT16oqFcQwV48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3527,
        'https://c.m.163.com/nc/article/list/T1491816738487/0-20.html': 3528,
        'https://c.m.163.com/dlist/article/dynamic?from=T1441074311424&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975399&sign=%2FF6dPtvw6BOc7iUIbxHtNSFwd8eqLDH46K6Na9RVmkV48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3529,
        'https://c.m.163.com/dlist/article/dynamic?from=T1467284926140&offset=0&size=20&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975570&sign=wdMhltZ%2F8YOcvFDVBV0toJcMLUq41P3QI%2FGnANiHMiN48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3530,
        'https://c.m.163.com/nc/article/list/T1482470888760/0-20.html': 3531,
        'https://c.m.163.com/nc/article/list/T1492136373327/0-20.html': 3532,
        'https://c.m.163.com/nc/article/list/T1414142214384/0-20.html': 3533,  # 新时代
        'https://c.m.163.com/nc/article/list/T1464592736048/0-20.html': 3534,
        'https://c.m.163.com/nc/article/list/T1456394562871/0-20.html': 3535,
        'https://c.m.163.com/dlist/article/dynamic?from=T1499853820829&offset=0&size=10&fn=2&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=a9ymprMSyFrjiYaUCfXQ6g%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975778&sign=0mIM2gP2OPSbBRcwtu%2FieUx%2Bent956qO20rdZXaUcTh48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3536,
        'https://c.m.163.com/dlist/article/dynamic?from=T1348649776727&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975189&sign=RIbg03wZQX%2BgZ0qTXAVvNhdMTQChIaeqg1k68blGyXZ48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3537,
        'https://c.m.163.com/dlist/article/dynamic?from=T1348649654285&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975407&sign=2WBNivWlQP6vaU88%2BnasOHLIR9LmoH%2BEFFTHt6YdWYl48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3538,
        'https://c.m.163.com/dlist/article/dynamic?from=T1348650593803&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557974753&sign=YSK32xY8qQ%2Byvdu%2BP%2BAMDMK6AXqukGEdZGdPtPtfcpJ48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3539,
        'https://c.m.163.com/dlist/article/dynamic?from=T1348650839000&offset=0&size=10&fn=2&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=a9ymprMSyFrjiYaUCfXQ6g%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975701&sign=Rnq%2FxR2ZSm0MZH1RkGgBIrWX54EXJKkUTWu%2FPOS1QB148ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3540,
        'https://c.m.163.com/nc/article/list/T1350383429665/0-20.html': 3541,
        'https://c.m.163.com/dlist/article/dynamic?from=T1397116135282&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975196&sign=3fM5N3P5iALCzJf6WhCGN7FtgNM0MdGP%2BpNQ%2FAkSDuN48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3542,
        'https://c.m.163.com/nc/article/list/T1411113472760/0-20.html': 3543,
        'https://c.m.163.com/dlist/article/dynamic?from=T1348650839000&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975398&sign=L%2BR2A78jtHEzV2A6PxxIxTJSks07MOhuqtBRKDi1gH148ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3544,
        'https://c.m.163.com/dlist/article/dynamic?from=T1348654204705&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975195&sign=pqdhfjAQGuy1ivSKoWjUYmjs8aJOIW%2Bhq%2F6nKblpEXd48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3545,
        'https://c.m.163.com/nc/article/list/T1368497029546/0-20.html': 3546,
        'https://c.m.163.com/dlist/article/dynamic?from=T1348654225495&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975392&sign=AyADDPqUuLd0ktZxQuwfJvxu8%2FgqOx193OhRVdRhiZR48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3547,
        'https://c.m.163.com/dlist/article/dynamic?from=T1414389941036&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975083&sign=hEypvFL8DJ5897%2FnVMDMZlzb7ZUQHnDsdoEY4UEBsQ148ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3548,
        'https://c.m.163.com/dlist/article/dynamic?from=T1348654105308&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557974944&sign=GzL2HUD2YS6lfnzEyJz0rr2N5IlUkU%2BRGdv5v3pOPi548ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3549,
        'https://c.m.163.com/dlist/article/dynamic?from=T1348649176279&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975191&sign=S3jvNbG%2BfMvo4A7X7pk8NEPO230vCn34%2BZ5n50xrD0d48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3550,
        'https://c.m.163.com/dlist/article/dynamic?from=T1473054348939&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557974853&sign=bX9nOA6rzLoULO79RGr9LQObUgx3Xln%2BWFlV0NFiYnd48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3551,
        'https://c.m.163.com/dlist/article/dynamic?from=T1524118019401&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=a9ymprMSyFrjiYaUCfXQ6g%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975577&sign=0qWpWt9AX%2B3XdVc4uwqobphcgVZiRGetjsDBw1jl%2FJZ48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3552,
        'https://c.m.163.com/nc/article/list/T1481105123675/0-20.html': 3553,
        'https://c.m.163.com/nc/article/list/T1370583240249/0-20.html': 3554,
        'https://c.m.163.com/nc/article/list/T1486979691117/0-20.html': 3555,
        'https://c.m.163.com/dlist/article/dynamic?from=T1348648756099&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=3%2B5Avjk4wDrLGkQNJXjlHA%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557974605&sign=GjgdshVhg%2FuuDgggcQTQ4IxS%2FgFQIDZ6p9NDneOPVxV48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3556,
        'https://c.m.163.com/dlist/article/dynamic?from=T1348649145984&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=C%2BDLFMmU%2BHEL12sc5FYe8Kgl5w4sTcBIU1x7WfNS7JsYcc10Igbb4P5j0Ss0EqlqIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=a9ymprMSyFrjiYaUCfXQ6g%3D%3D&lon=l5pNav9vlUIZPPYR8sWs%2FA%3D%3D&version=55.5&net=wifi&ts=1557975605&sign=xwO0sSlyGl649ODvemuxDbf9QIo7SPkCY2A8FNvEHSZ48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=QQ_news_CPD1&mac=ZZqMsphoaYi6%2Ba2dzXFxyYe1A3IUPLLdoCiqBVf2Go0%3D&open=&openpath=': 3557,
        'https://c.m.163.com/nc/article/list/T1348649475931/0-20.html': 3558,

    }

    start_headers = {'User-Agent': 'NewsApp/56.2 Android/6.0 (Xiaomi/Redmi Pro)'}

    def parse(self, response):
        if response.status > 200 and not response.text:
            self.log(
                'source_id: %s, url: %s, status: %s' % (response.meta.get('source_id'), response.url, response.status))
            return
        try:
            rs = json.loads(response.text)
            k0 = list(rs.keys())[0]  # re.findall(".*from=(.*)&offset.*", response.url)
            feedlist_items = rs.get(k0)  # 取dict第一个值
        except:
            return self.produce_debugitem(response, 'json error')
        # http://c.m.163.com/nc/article/EDMFA12I0005877U/full.html
        for i in feedlist_items:
            docid = i.get('docid')
            news_url = "http://c.m.163.com/nc/article/" + docid + "/full.html"
            # http://c.m.163.com/nc/special/S1556005906291/full.html

            if 'updateDoc' in news_url:  # todo 什么网址
                # 新闻url  http://c.m.163.com/nc/article/9IG74V5H00963VRO_0036set2103110updateDoc/full.html
                # 内容是 <p>　　您的新闻客户端版本太低啦，升级之后就能看到更丰富的新闻形式了！<\/p><p>　　<!--link0--><\/p><p>　　<!--link1--><\/p><p>　　Windows Phone和Win8/Win10客户端暂不支持从新闻列表中直接进入图集、视频、直播室。iPad客户端暂不支持从新闻列表中直接进入视频。我们在不断提升用户体验，后续功能敬请期待！<\/p><p>　　     网易新闻，各有态度！为4亿人新闻阅读而生！<\/p><p><!--viewpoint--><\/p>
                # 说明是直播 '贵阳数博会5G直播'
                continue
            pubtime = i.get('ptime')

            title = i.get('title')
            if '您的客户端版本过低' in title:
                self.log('url: %s, source_id: %s, 您的客户端版本过低!' % (response.url, response.meta.get('source_id')))
                yield self.produce_debugitem(response, "'您的客户端版本过低' in title")
                continue
            origin_name = i.get('source')
            yield Request(
                url=news_url,
                callback=self.parse_item,
                headers=self.start_headers,
                meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                      'origin_name': origin_name, 'docid': docid,
                      'start_url_time': response.meta.get('start_url_time'),
                      'schedule_time': response.meta.get('schedule_time')}
            )

    def parse_item(self, response):
        # 示例 有视频有图片， 图片有二维码 http://c.m.163.com/nc/article/EOS9JM5100058781/full.html
        if response.status > 200 and not response.text:
            self.log(
                'source_id: %s, url: %s, status: %s' % (response.meta.get('source_id'), response.url, response.status))
            return

        docid = response.meta['docid']
        try:
            rs = json.loads(response.text)
            article = rs.get(docid)
            content_div = jsonpath.jsonpath(rs, '$..body')[0]
            img_dict_list = article.get('img', [])
            media = {}
            for i, j in enumerate(img_dict_list):
                media.setdefault("images", {})  # <!--IMG#2-->
                # ind = re.search(r'\<\!--IMG#(\d+)--\>', i.get('ref')).group(1)
                media['images'][str(i + 1)] = {"src": j.get('src')}

            content, img_count, video_count = self.__clean(content_div)
            content = self.parser.cleaner.clean_html(content, kill_xpaths=['//*[re:match(text(),"欢迎搜索关注公众号")]',
                                                                           '//*[re:match(text(), "投稿请联系邮箱：")]',
                                                                           '//*[re:match(text(), "关注公众号【")]',
                                                                           '//*[re:match(text(),"关注公众号，观看更多精彩内容")]',
                                                                           '//*[re:match(text(), "扫描下方二维码")]',
                                                                           '//*[re:match(text(),"关注公众号：")]',
                                                                           ])

            videos = {}
            video_urls = jsonpath.jsonpath(rs, '$..video[*].url_mp4')
            if video_urls:
                if video_count != len(video_urls):
                    self.log('视频数量不符!')
                for i, j in enumerate(video_urls):
                    if j:
                        videos[str(i + 1)] = {'src': j}
                    else:
                        print()
            elif video_count > 0:
                self.log('视频数量不符!')

            if img_count != len(img_dict_list):
                self.log('图片数量不符!')
        except:
            return self.produce_debugitem(response, 'json error')

        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            content=content,
            media=media,
            videos=videos
        )

    def __clean(self, content):
        imgs = ip.findall(content)
        vids = vp.findall(content)

        # 去二维码 'http://cms-bucket.ws.126.net/2019/01/04/4661e219fca94186a823c89358d523f7.jpeg'
        # 去公众号 http://cms-bucket.ws.126.net/2019/06/05/6f8200c31e604d808067ab6dcaf6614d.png
        # http://cms-bucket.ws.126.net/2019/05/24/195d30b1a0534bf480e08c76c95e8a11.png
        if imgs and os.path.basename(imgs[-1]).split('.')[0] in (
                '4661e219fca94186a823c89358d523f7', '6f8200c31e604d808067ab6dcaf6614d'):
            imgs.pop()

        for i, j in enumerate(imgs):
            content = content.replace(j, '${{%s}}$' % (i + 1))
        for i, j in enumerate(vids):
            content = content.replace(j, '#{{%s}}#' % (i + 1))

        content = content.replace('$$', '$<br>$')  # 连续2图片 视频加换行
        return content, len(imgs), len(vids)
