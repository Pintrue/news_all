# -*- coding:utf-8 -*
# Name:db_config.py
# Author:
# CreateTime:


class DatabaseConfig(object):
    """
    local:      127.0.0.1 db
    test:       test db       测试库
    online:     online db
    """
    class News(object):
        db_type = 'mongo'
        config = {
            'local': {
                'host': '127.0.0.1',
                'user': 'news',
                'port': 27017,
                'password': 'news',
                'database': 'news',
                'collection': 'newsContent'
            },
            'study': {
                'host': '127.0.0.1',
                'user': 'news',
                'port': 27017,
                'password': 'news',
                'database': 'study',
                'collection': 'studycol'
            }
            # 'test'    test清洗系统存test mongodb
            # 'online'  online清洗系统存online mongodb
        }


    class Source(object):
        db_type = 'mongo'
        config = {
            'local': {
                'host': '127.0.0.1',
                'user': 'news',
                'port': 27017,
                'password': 'news',
                'database': 'news',
                'collection': 'source'
            },
            'test': {
                'host': '10.50.162.87',  # 主机可读写
                'user': 'source',
                'port': 27017,
                'password': 'source',
                'database': 'source',
                'collection': 'source'
            },
            'online': {  # 内网
                'host': 'dds-2zeb84d1d33290941.mongodb.rds.aliyuncs.com',
                'user': 'source',
                'port': 3717,
                'password': 'source',
                'database': 'source',
                'collection': 'source'
            },
            'online_out': { # 外网
                'host': 'dds-2zeb84d1d33290941438-pub.mongodb.rds.aliyuncs.com',
                'user': 'source',
                'port': 3717,
                'password': 'source',
                'database': 'source',
                'collection': 'source'
            },
        }

    class Debug(object):
        db_type = 'mongo'
        config = {
            'local': {
                'host': '127.0.0.1',
                'user': 'news',
                'port': 27017,
                'password': 'news',
                'database': 'news',
                'collection': 'news_all_local_debug'
            },
            'test': {
                'host': '10.50.162.87',
                'user': 'source',
                'port': 27017,
                'password': 'source',
                'database': 'source',
                'collection': 'news_all_test_debug'
            },
            'test_dispatch': {
                'host': '10.50.162.87',
                'user': 'source',
                'port': 27017,
                'password': 'source',
                'database': 'source',
                'collection': 'news_all_test_debug_dispatch'
            },
            'online': {
                # 'host': '10.2.113.29',  # 线上机连不上10.2.113.29
                'host': 'dds-2zeb84d1d33290941.mongodb.rds.aliyuncs.com',
                'user': 'source',
                'port': 3717,
                'password': 'source',
                'database': 'source',
                'collection': 'news_all_online_debug'
            },
            'online_out': {  # 外网
                'host': 'dds-2zeb84d1d33290941438-pub.mongodb.rds.aliyuncs.com',
                'user': 'source',
                'port': 3717,
                'password': 'source',
                'database': 'source',
                'collection': 'news_all_online_debug'
            },
        }

    class Cache(object):
        db_type = 'redis'
        config = {
                 'local': {
                     'host': '127.0.0.1',
                     'port': 6379,
                     'db': 3,
                 },
                 'play': {
                     'host': '127.0.0.1',
                     'port': 6379,
                     'db': 3,
                 },
                 'online': {
                     'host': '127.0.0.1',
                     'port': 6379,
                     'db': 3,
                 },
        }