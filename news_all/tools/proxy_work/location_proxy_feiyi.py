# -*- coding: utf-8 -*-
# @File    : location_proxy_feiyi.py
import hashlib
import threading
import time

import requests

from news_all.tools.proxy_work.others import exception_factory


class ErrorFeiYiUnknown(Exception):
    info = '飞蚁未知错误'


FEIYI_PROVINCE = {"北京": "110000",
                  "天津": "120000",
                  "河北": "130000",
                  "山西": "140000",
                  "内蒙古": "150000",
                  "辽宁": "210000",
                  "吉林": "220000",
                  "黑龙江": "230000",
                  "上海": "310000",
                  "江苏": "320000",
                  "浙江": "330000",
                  "安徽": "340000",
                  "福建": "350000",
                  "江西": "360000",
                  "山东": "370000",
                  "河南": "410000",
                  "湖北": "420000",
                  "湖南": "430000",
                  "广东": "440000",
                  "广西": "450000",
                  "海南": "460000",
                  "重庆": "500000",
                  "四川": "510000",
                  "贵州": "520000",
                  "云南": "530000",
                  "西藏": "540000",
                  "陕西": "610000",
                  "甘肃": "620000",
                  "青海": "630000",
                  "宁夏": "640000",
                  "新疆": "650000"}


class FeiYiProxy():
    """飞蚁代理"""
    # 以下5项 可能因购买情况、供应商切服务器而改变
    user_name = "feiyiproxyap4"  # 1290个 2019-05-14~~06-13 08:16:44到期 时长3分钟
    password = "12345678"
    BaseUrl = "http://183.129.244.16:88/"
    # BaseUrl = "http://183.129.207.77:88/"
    time_out = 180  # 每个ip时长。 可购买时长3、5、10、30分钟的等级
    auth = "Basic" + user_name + ":" + password + "\r\n"
    redis_key = 'proxy_feiyi'
    
    # http://183.129.244.16:88/open?user_name=feiyiproxyap1&timestamp=1554712923&md5=9D92F20F878F766DE660A53CE25EA564&pattern=json&number=5
    """
    { "code": 100, "left_ip": 500, "left_time": 2591783, "number": 5, "domain": "183.129.244.16", "port": [ 11391, 11390, 11389, 11388, 11387 ] }
    """
    GetIpApi = BaseUrl + 'open?user_name=%s&' \
                         'timestamp={}&md5={}&pattern=json&number={}&province={}' % user_name  # 获取 todo &fmt=6
    ALLOW_PROVINCE = FEIYI_PROVINCE  # 允许的省份
    _SgLock = threading.Lock()  # 单例的Lock
    location_proxy = {}

    error_map = {101: "认证不通过",
                 102: "请求格式不正确",
                 103: "IP 耗尽",
                 104: "端口耗尽",
                 105: "要删除的端口未找到（原因：已经释放）",
                 106: "账号到期，请充值",
                 111: "省份ID错误",
                 112: "城市ID错误"}

    def extract_ip_from_api(self, province="浙江", number=1):
        """
        注：
        1、此申请方法为获取ip，实际使用ip时为防止其他人盗用，可选择不同验证方法验证使用；验证方法详见末尾说明；  # todo
        2、客户方测试前期为操作简单，一般会给客户设置提取ip时不验证MD5，保证账号MD5长度一致就可以；
        :param province:     str                省名   示例 '北京'
        :param number        int                提取代理个数（最小为 1，最大 200）
        :return:
        """
        ts, md5_str = self.get_stamp_md5_str()
        url = self.GetIpApi.format(ts, md5_str, number, FEIYI_PROVINCE.get(province, ''))

        res = requests.get(url)
        if res.status_code != 200:
            raise exception_factory('FEIYI', 'extract_ip_from_api' + str(res.status_code))
        rj = res.json()
        # print('======代理:%s抽取ip返回json======\n%s' % (self.user_name, rj))
        """
        正确示例   # 不返回省市和真实请求ip
        { "code": 100, 
        "left_ip": 9996, 
        "left_time": 168441, 
        "number": 1, 
        "domain": "183.129.244.16", 
        "port": [ 17562 ] }        
        """
        """
        正确示例   # 返回省市和真实请求ip
        {'code': 100, 
        'left_ip': 916, 
        'left_time': 2286557, 
        'number': 1, 
        'domain': '183.129.207.77', 
        'data': [{'IP': '27.158.46.151:15484', 'ISP': '电信', 'IpAddress': '福建省漳州市 电信'}]}
        """
        if rj['code'] == 100:
            # 成功返回
            print("飞蚁 剩余ip: %s 个, 账号剩余使用时间: %s" % (rj["left_ip"], rj['left_time']), '\n')
            return [rj['domain'] + ':' + str(i) for i in rj['port']]
        
        elif rj['code'] in self.error_map:
            # 碰到异常状态可进行的操作； 释放代理端口
            # print("飞蚁 提取省:%s, ip失败: 原因%s" % (province, self.error_map[rj['code']]))
            raise exception_factory('FEIYI', self.error_map[rj['code']])
        
        else:
            # print("飞蚁 提取ip失败: 不明原因, 返回%s" % res.text)
            raise ErrorFeiYiUnknown()

    def release_port(self, port):
        """释放端口"""
        ts, md5_str = self.get_stamp_md5_str()
        url = self.BaseUrl + 'close?user_name={}&timestamp={}&md5={}&pattern=json&port={}'.format(self.user_name, ts,
                                                                                                  md5_str, port)
        r = requests.get(url)
        if r.status_code == 200 and r.json()["code"] in [100, 105]:
            return True
        else:
            raise exception_factory('FEIYI', self.error_map[r.json()['code']])

    def _reset_ip(self):
        """重置本用户已使用ip"""
        ts, md5_str = self.get_stamp_md5_str()
        url = self.BaseUrl + "reset_ip?user_name={}&timestamp={}&md5={}&pattern=json".format(self.user_name, ts,
                                                                                             md5_str)
        r = requests.get(url)
        print(r.text)

    @classmethod
    def my_state(cls):
        """
        获取状态:
             上一次申请后剩余IP数,
             账号剩余使用时间,
             当前已使用的ip数量,
             当前正在使用的ip数量,
             当前正使用的端口号列表  注：最多返回 200 个端口号
         """
        ts, md5_str = cls.get_stamp_md5_str()
        url = cls.BaseUrl + 'query?user_name={}&timestamp={}&md5={}&pattern=json'.format(cls.user_name, ts,
                                                                                         md5_str)
        r = requests.get(url, timeout=10)

        if r.status_code == 200 and r.json()["code"] == 100:
            rj = r.json()
            print("上一次申请后剩余IP数:%s, 账号剩余使用时间: %s秒, 当前已使用的ip数量:%s, 当前正在使用的ip数量: %s, 当前正使用的端口号列表: %s" % (
                rj["left_ip"], rj["left_time"], rj["used"], rj["inuse"], rj["port"]))
            return rj["left_ip"], rj["left_time"], rj["used"], rj["inuse"], rj["port"]
        else:
            raise exception_factory('FEIYI', cls.error_map[r.json()['code']])

    @classmethod
    def get_stamp_md5_str(cls):
        timestamp = str(int(time.time() * 1000))
        return timestamp, hashlib.md5((cls.user_name + cls.password + timestamp).encode('utf8')).hexdigest()


if __name__ == '__main__':
    f = FeiYiProxy()
    # print(f.extract_ip_from_api("浙江", 1))  # 测试
    print(FeiYiProxy.my_state())
