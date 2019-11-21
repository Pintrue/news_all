#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 上午10:56
# @Author  : wjq
# @File    : others


import os
import socket
from functools import wraps
import time
import threading
from typing import Iterable


class Singleton(object):
    _instance_lock = threading.Lock()
    _instances = {}

    def __new__(cls, *args, **kwargs):
        with Singleton._instance_lock:
            if cls.__name__ not in Singleton._instances:
                Singleton._instances[cls.__name__] = object.__new__(cls)
        return Singleton._instances[cls.__name__]


def get_upper_dir(abs_path, n):
    """获取上n级的路径"""
    if n == 0:
        return abs_path
    path = os.path.dirname(abs_path)
    return get_upper_dir(path, n - 1)


class RetryNoResError(Exception):
    """重试次数太多但无返回"""
    pass


def retry_dec(retry_time, logger):  # 最多执行函数装饰器
    def dec(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            res = None
            _retry_time = retry_time
            while not res and _retry_time > 0:
                _retry_time = _retry_time - 1
                try:
                    res = fn(*args, **kwargs)  # fn是有返回的
                except Exception as e:
                    logger.error("Round:{}, fn: {} raise Exception: %s".format((retry_time-_retry_time), fn.__name__), e)  # 第几轮函数报错
                    # time.sleep(random.uniform(0, 1))
                    time.sleep(3)
            if _retry_time == 0 and not res:
                raise RetryNoResError('fn: %s retry too many times! No res!' % fn.__name__)
            return res

        return wrapper

    return dec


def to_list(cv):
    if cv is None:
        return []
    if isinstance(cv, str):
        return [cv]
    if isinstance(cv, Iterable):
        return cv
    else:
        return [cv]


def get_sub_str_ex(s, start_str, end_str, greedy=True):
    begin_idx = s.find(start_str)
    if begin_idx < 0:
        return
    if greedy:
        end_idx = s.rfind(end_str)
        if end_idx < 0:
            return
        yield s[begin_idx + len(start_str):end_idx]
    else:
        s = s[begin_idx + len(start_str):]
        end_idx = s.find(end_str)
        if end_idx <= 0:
            return
        yield s[:end_idx]
        for value in get_sub_str_ex(s[end_idx:], start_str, end_str, greedy):
            yield value


def check_ip():
    """判断当前主机ip"""
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.connect(('8.8.8.8', 80))
        ip = udp_socket.getsockname()[0]  # 从协议头中获取本机ip
        udp_socket.close()
        return ip
    except Exception as e:
        print("[ERROR] >> %s" % e)
