#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/16 8:41
# @Author  : wjq
# @File    : mongo_rw.py


import pymongo


class MongoBaseRW(object):
    """基本读写Mongo库工作类"""
    db_config = None  # 数据库配置

    def __init__(self, env='local', host='', port='', user='', password='', db='', collection=''):
        """
        可以配置环境，或输入连接参数
        1.环境
        env 为db_config中的连接配置,如果类属性read_only为True时，无视env直接使用read_only
        local:      myself
        test:       test  db
        online:     online db

        2.自定义连接参数：
        custom:     env 为 custom 使用后面的连接参数的配置
        """
        self.env = env
        if env == 'custom':
            db_config = {
                'host'    : host,
                'port'    : port,
                'user'    : user,
                'password': password,
                'database'      : db,
                'collection'    : collection,
            }
        else:
            db_config = self.db_config.config[env]

        self.client = pymongo.MongoClient(db_config['host'], db_config['port'])
        self.db = self.client[db_config['database']]
        if db_config.get('user') and db_config.get('password'):
            self.db.authenticate(db_config['user'], db_config['password'])
        self.coll = self.db[db_config['collection']]

    def close(self):
        self.client.close()

    def insert(self, dic):
        # print("insert...")
        return self.coll.insert(dic)

    def find(self, dic=None):
        # print("find...")
        if not dic:
            return [i for i in self.coll.find()]
        return [i for i in self.coll.find(dic)]

    def find_one(self, dic):
        # print("find_one...")
        return self.coll.find_one(dic)

