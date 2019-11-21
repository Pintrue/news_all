#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/15 9:33
# @Author  : wjq
# @File    : main.py

from scrapy import cmdline


cmd = 'scrapy crawl ceweekly'


cmdline.execute(cmd.split())
