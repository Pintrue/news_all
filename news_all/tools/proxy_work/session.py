# -*- coding: utf-8 -*-
# @Time    : 2018/11/20 5:27 PM
# @Author  : wxy
# @File    : session.py
import random

import re
import requests

import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

from others import exception_factory, ErrorHttpProxy
from proxy_tool import RandomProxy


class Session(object):
    """
    封装requests的Session
    处理headers,host等
    注意这个是自带代理的
    参数:
        url         str     url
        data        dict    post数据
        referer     str     从哪来
        use_ajax    bool    是否是ajax请求
        use_proxy   bool    是否用代理
    """

    UA = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)'
    ]

    def __init__(self, target_proxy=''):
        """
        :param target_proxy:    str     指定使用的代理名称,空为随机用
        """
        self.target_proxy = target_proxy
        self._session = requests.Session()
        self.proxy_name = ''  # 代理名称
        self._session.headers['User-Agent'] = self.UA[random.randint(0, len(self.UA) - 1)]

    def add_headers(self, k, v):
        self._session.headers[k] = v

    def set_proxies(self):
        """设置代理"""
        RandomProxy.prepare_session(self, self.target_proxy)

    def get_cookie_data(self, k, not_find=''):
        return self._session.cookies.get(k, not_find)

    def confirm_host(self, url):
        m = re.search('[http|https]:\/\/(.*?)/.*', url)
        if m:
            self.add_headers('Host', m.group(1))
        else:
            Exception('输入的url不正确')

    def get(self, url, referer='', use_ajax=False):
        return self.request('GET', url, None, referer, use_ajax)

    def post(self, url, data, referer='', use_ajax=False):
        return self.request('POST', url, data, referer, use_ajax)

    def request(self, method, url, data=None, referer='', use_ajax=False, use_proxy=True):
        self.confirm_host(url)
        if referer:
            self.add_headers('Referer', referer)
        if use_ajax:
            self.add_headers('X-Requested-With', 'XMLHttpRequest')
        try:
            if use_proxy:
                self.set_proxies()
            print(self._session.proxies)
            r = self._session.request(
                # add_headers('Proxy-Authorization', auth) bug: self._session.headers并没有传入函数headers=None, auth=None, proxies=None
                method, url, data=data, verify=False, allow_redirects=False,
                headers=self._session.headers, proxies=self._session.proxies
                # auth=self._session.get('Proxy-Authorization')  #
            )  # 禁止重定向
            if not r:
                print()

            if not 200 <= r.status_code < 400:
                if r.status_code in (301, 302):
                    print(r.headers.get('Location', ''))
                raise exception_factory(self.proxy_name, str(r.status_code))
            return r
        except requests.exceptions.ProxyError as e:
            if 'To Many Requests' in str(e):  # 请求太快
                raise exception_factory(self.proxy_name, 'tooMany')
            elif 'Cannot connect to proxy' in str(e):  # 代理无法连接
                raise exception_factory(self.proxy_name, 'CannotProxy')
            elif 'Remote end closed connection without response' in str(e):  # 远程拒绝访问
                raise exception_factory(self.proxy_name, 'remoteClosed')
            else:  # 其他代理错误
                print('other proxy error:', e)
                raise exception_factory(self.proxy_name, 'other')
        except Exception as e:  # 其他未知错误
            raise e



from location_proxy_feiyi import FeiYiProxy, FEIYI_PROVINCE


fy_p = FeiYiProxy()


def get_location_session(province_name):
    """获取省份代理"""

    # 站大爷续费停了
    # if province_name in ZHANDAYE_PROVINCE:  # 站大爷
    #     return LocationSession(zdy_p, province_name)

    # if province_name in list(FEIYI_PROVINCE.keys()) + list(TAIYANG_PROVINCE.keys()):
    #     if province_name in TAIYANG_PROVINCE:
    #         p_tool = random.choice([fy_p, ty_p])  # 飞蚁和太阳代理随机
    #         return LocationSession(p_tool, province_name)
    #     elif province_name in FEIYI_PROVINCE:
    #         return LocationSession(fy_p, province_name)  # 飞蚁
    # else:
    #     return Session()
    return LocationSession(fy_p, province_name)


class LocationSession(Session):
    """指定省份的Session"""

    def __init__(self, location_proxy_tool, province_name):
        super().__init__(target_proxy='')
        self.province_name = province_name
        self.location_proxy_tool = location_proxy_tool
        self.proxy_name = self.location_proxy_tool.__class__.__name__
        self.p_obj = None

    def set_proxies(self):
        p_obj = self.location_proxy_tool.get_province_proxy(self.province_name)
        self.p_obj = p_obj
        self._session.proxies = p_obj.proxies

    def request(self, *args, **kwargs):
        """遇到被封的情况或代理不可用，需要换IP"""
        try:
            return super().request(*args, **kwargs)
        except Exception as e:
            if isinstance(e, ErrorHttpProxy) and self.p_obj:
                self.p_obj.remote_close = True
            raise e


if __name__ == '__main__':
    if __name__ == '__main__':
        # ip_port, auth = RandomProxy()
        url = 'https://baidu.com'
        
        ses = Session()
        res = ses.get(url)
        print(res.status_code)
        print(res.text)