#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 19:27
# @Author  : wjq
# @File    : others.py


class ErrorHttpProxy(Exception):
    """代理异常"""
    pass


def exception_factory(proxy_name, error_detail):
    """
    生成代理和原因的错误，用于抛出异常
    :param proxy_name:      str         代理名称
    :param error_detail:    str         错误描述
    :return:                Exception   代理异常类
    """
    exception_name = (proxy_name + '_' + error_detail).upper()
    return type(exception_name, (ErrorHttpProxy,), {'info': exception_name})