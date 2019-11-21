#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/1 下午1:05
# @Author  : wjq
# @File    : cookie_tools


def cookies_dict_to_str(cookie_dict):
    ss = ''
    for i, j in cookie_dict.items():
        ss += i + '=' + j + ';'
    ss = ss[:-1]
    return ss


def cookies_str_to_dict(cookie):
    '''
    将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
    :return:
    '''
    itemDict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        itemDict[key] = value
    return itemDict