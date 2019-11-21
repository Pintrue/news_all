#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 10:25
# @Author  : wjq
# @File    : redis_memory.py


from redis import StrictRedis
from news_all.tools.database_work.ssh_pipe import create_ssh_server, WORK_MACHINE, OUT_NET_HOST
import sys

# 兼容处理Py2 和 Py3 Unicode问题
from news_all.tools.others import check_ip

VERSION = sys.version[0]
USE_UNICODE = False if VERSION == '2' else True

REDIS_ENCODING = 'utf-8'
# Sane connection defaults.
REDIS_PARAMS = {
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
    'retry_on_timeout': True,
    'encoding': REDIS_ENCODING,
}

redis_conf = {
    'local': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
        'encoding': REDIS_ENCODING,
    },
    'test': {
        'host': '10.50.162.243',
        'port': 6379,
        'password': 'XVF6n9xB5L5uN7WxWOTW',
        'db': 0,
    },
    'online': {
        'host': 'r-2zef9c4f9bce7d04.redis.rds.aliyuncs.com',  # todo
        'port': 6379,
        'db': 0,
    },
}


class RedisRW(object):
    """读写redis类"""
    db_config = {}
    
    def __init__(self, env):
        self.db_config = redis_conf[env]
        
        ip = check_ip()
        print("当前主机ip >> %s" % ip)
        # 不在工作机器,或者不是local环境
        if ip not in WORK_MACHINE and self.db_config['host'] not in OUT_NET_HOST:
            # 获取ssh服务并启动
            self.ssh_server = create_ssh_server(
                self.db_config['host'],
                self.db_config['port'])
            self.r = StrictRedis(host='127.0.0.1', port=self.ssh_server.local_bind_port, decode_responses=True)
        else:
            self.ssh_server = None
            self.r = StrictRedis(**redis_conf[env])
    
    def rpush(self, k, v):
        return self.r.rpush(k, v)
    
    def lpush(self, k, v):
        return self.r.lpush(k, v)
    
    def lpop(self, k):
        return self.r.lpop(k)
    
    def llen(self, k):
        return self.r.llen(k)
    
    def get_len(self, k):
        # ty = bytes(self.r.type(k))  # self.r.type(k)  todo why 有时是byte有时是str 发现local库是byte, test online库是字符串
        ty = self.r.type(k)
        if isinstance(ty, bytes):
            ty = ty.decode('utf-8')
        if ty == 'set':
            return self.r.scard(k)
        elif ty == 'zset':
            return self.r.zcard(k)
        elif ty == 'list':
            return self.r.llen(k)
        else:
            return 0
    
    def get(self, k):
        return self.r.get(k)
    
    def del_key(self, k):
        return self.r.delete(k)
    
    def close(self):
        if self.ssh_server:
            self.ssh_server.stop()
    
    def to_safe_len(self, max_count, k):
        # 初始长度
        len_0 = self.get_len(k)
        val = len_0 - max_count
        if val > 0:
            print('key: %s, 初始长度: %s, 要切去长度: %s' % (k, len_0, val))
            if self.r.type(k) != 'list':
                for i in range(val):
                    self.lpop(k)
            else:
                self.del_key(k)
    
    def get_total_len(self):
        keys = self.r.keys()
        
        count = 0
        for k in keys:
            l = self.get_len(k)
            count += l
            print(k, '---' * 10, l)
        print('==========总长度===========\n', count)
        return count


if __name__ == '__main__':
    # rw = RedisRW('test_dispatch')
    rw = RedisRW('local')
    
    # bb = rw.r.zadd(b'salary', {'a': 12000, 'b': 6000, 'c': 4000})  # 新增
    bb = rw.r.zadd(b'abc', {'a': 9000, 'b': 10000, 'c': 10000}, nx=True)  # 新增
    print(bb)  # 返回1
    # rw.close()
    # g = {str(j): i for i, j in enumerate(gmw_all)}
    # bb = rw.r.zadd(b'gmw_all:start_urls', g)
    # print('bb=', bb)  # 若已存在value, zadd返回0(int); 若不存在value,zadd返回1
    
    # aa = rw.r.zpopmax(b'salary', count=2)  # Redis 5的新功能
    # cc = rw.r.zcard(b'salary')  # 集合长度(元素个数)
    # print(bb, cc)
    #
    # count = rw.r.zcount(b'salary', max=8000, min=7000)
    # print(count)
    #
    # al = rw.r.zrange(b"salary", 0, -1)  # 获取有序集合中所有元素 [b'jack', b'tom', b'peter', b'psw']
    # print('al=', al)
    # #
    # # als = rw.r.zrange(b"salary", 0, -1, withscores=True)   # 获取有序集合中所有元素和分数 默认是按照分数升序排序 [(b'jack', 2000.0), (b'tom', 5000.0), (b'peter', 7500.0), (b'psw', 50000.0)]
    # # print(als)
    # #
    # alw = rw.r.zrange(b"salary", 0, 3,
    #                   withscores=True)  # 获取有序集合中3元素  按照分数降序排序 [(b'jack', 2000.0), (b'tom', 5000.0), (b'peter', 7500.0), (b'psw', 50000.0)]
    # print('alw=', alw)
    #
    # ald = rw.r.zrange(b"salary", 0, 0, desc=True,
    #                   withscores=True)  # 获取有序集合中3元素  按照分数降序排序 [(b'jack', 2000.0), (b'tom', 5000.0), (b'peter', 7500.0), (b'psw', 50000.0)]
    # print('ald=', ald)
    #
    # dell = rw.r.zrem(b'salary', *[i for i, _ in ald])  # 一次删除多个元素, 返回删除的个数
    # print(dell)  # 返回个数
    
    # d = rw.r.zrem(b'gmw_all:start_urls', b'1076')
    # print(d)
    # del_one = rw.r.zrem(b'salary', 'wjq')  # 一次删除单个元素
    # print(del_one)   # 返回个数
    #
    # del_score = rw.r.zremrangebyscore(b'salary', min=1000, max=2000)
    # print(del_score)
    
    # rw.get_total_len()
    # rw.close()
    # keys = [
    #              "stcn_kx_spider:requests",
    #              "jh_people:requests",
    #              "sina_wap:dupefilter",
    # "chinaqw_all:dupefilter",
    # "junwang_all:dupefilter",
    # "chnfund:dupefilter",
    # "youth_all:dupefilter",
    # "china5e_all:dupefilter",
    # "msweekly:dupefilter",
    # "stcn_all:dupefilter",
    # ]
    
    # keys = rw.r.keys('*:start_urls')
    # ct = []
    # for k in keys:
    #     a = rw.get_len(k)
    #     ct.append((k, a))
    # ct = sorted(ct, key=lambda x: x[1])
    # for c in ct:
    #     print(c)
    # rw.close()
    # rw.get_total_len()
    
    # rw.close()  # 注意 关闭连接
    # rw.to_safe_len(10000, 'jwview:dupefilter')
    
    # pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    # r = redis.Redis(connection_pool=pool)
    # aa = r.zadd(b'salary', {'psw':40000})
    # print(aa)
