# -*- coding: utf-8 -*-
# @Time    : 2018/11/20 5:28 PM
# @Author  :
# @File    : proxy_tool.py
import hashlib
import random
import base64
import time
from urllib.parse import urlparse


class RandomProxy(object):
    """
    隧道代理工具
    添加代理: 将代理的获取方法放在类的静态方法中，返回tuple(proxies,auth)
    """

    @classmethod
    def proxy_fn_list(cls, target_proxy=''):
        proxy_fn = {
            # 'horocn': cls.proxy_horocn,
            'abuyun': cls.proxy_abuyun,
            # 'xdaili': cls.proxy_xdaili,
            # 'mogu'  : cls.proxy_mogu,
        }
        if not target_proxy or target_proxy not in proxy_fn:
            return list(proxy_fn.values())
        else:
            return proxy_fn[target_proxy]

    @classmethod
    def prepare_scrapy_request(cls, request, target_proxy=''):
        """为scrapy_request添加随机添加代理"""
        if target_proxy:
            proxy_fn = cls.proxy_fn_list(target_proxy)  # 指定代理名称
        else:
            pl = cls.proxy_fn_list()
            proxy_fn = pl[random.randint(0, len(pl) - 1)]  # 随机抽取代理

        ip_port, auth = proxy_fn()

        request.meta['proxy_name'] = proxy_fn.__name__
        request.meta['proxy'] = urlparse(request.url).scheme + "://" + ip_port
        if auth:
            request.headers['Proxy-Authorization'] = auth

    @classmethod
    def prepare_session(cls, session, target_proxy=''):
        """为session添加随机添加代理"""
        if target_proxy:
            proxy_fn = cls.proxy_fn_list(target_proxy)  # 指定代理名称
        else:
            pl = cls.proxy_fn_list()
            proxy_fn = pl[random.randint(0, len(pl) - 1)]  # 随机抽取代理

        proxies, auth = proxy_fn(False)

        session.proxy_name = proxy_fn.__name__
        session._session.proxies = proxies
        if auth:
            session.add_headers('Proxy-Authorization', auth)

    @staticmethod
    def proxy_horocn(need_ip_port=True):
        """蜻蜓代理"""
        proxyHost = "dyn.horocn.com"
        proxyPort = "50000"

        proxyUser = ""
        proxyPass = ""

        ip_port = "%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        auth = 'Basic ' + base64.b64encode((proxyUser+ ":" + proxyPass).encode('utf-8')).decode()
        if need_ip_port:
            return ip_port, auth
        else:
            return {"http": "http://" + ip_port, "https": "https://" + ip_port}, auth

    @staticmethod
    def proxy_abuyun(need_ip_port=True):
        """阿布云"""
        proxyUser = 'H26205E477ZGQ21D'
        proxyPass = '25D5C0253911D232'

        ip_port = "http-dyn.abuyun.com:9020"
        auth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
        if need_ip_port:
            return ip_port, auth
        else:
            return {"http": "http://" + ip_port, "https": "https://" + ip_port}, auth

    @staticmethod
    def proxy_xdaili(need_ip_port=True):
        """讯代理"""
        orderno = ""
        secret = ""
        ip_port = 'forward.xdaili.cn:80'

        timestamp = str(int(time.time()))  # 计算时间戳
        string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
        md5_string = hashlib.md5(string.encode()).hexdigest()  # 计算sign
        sign = md5_string.upper()  # 转换成大写
        auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
        if need_ip_port:
            return ip_port, auth
        else:
            return {"http": "http://" + ip_port, "https": "https://" + ip_port}, auth

    @staticmethod
    def proxy_mogu(need_ip_port=True):
        """
        蘑菇代理 标准每秒并发10个
        按转发量的 代理池每分钟更新150个，这150个里面有少部分重复，一分钟大于150次请求(1秒钟不要超过2.5次)则有重复IP
        """
        appKey = ""  # 1分钟超过150次则有重复IP# 。
        ip_port = 'transfer.mogumiao.com:9001'
        auth = 'Basic ' + appKey
        if need_ip_port:
            return ip_port, auth
        else:
            return {"http": "http://" + ip_port, "https": "https://" + ip_port}, auth


def get_mogu_balance(appkey):
    """查蘑菇ip余量"""
    url = "http://www.moguproxy.com/proxy/api/leftCount?type=3&appkey={}".format(appkey)
    import requests
    r = requests.get(url)
    if r.status_code == 200:
        return r.json().get("msg")
    else:
        print("查蘑菇ip余量 错误, 状态码: %s, text: %s" % (r.status_code, r.text))
    