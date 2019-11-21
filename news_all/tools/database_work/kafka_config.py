#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 18:40
# @Author  : wjq
# @File    : kafka_config.py
import json
from kafka import KafkaProducer


KFKConfig = {
    'test': '10.10.10.2:9092,10.10.10.3:9092,10.10.10.4:9092'.split(','),
    'local': ['127.0.0.1:9092',],
    'psw': ['172.30.4.55:9092',],
    'online':'172.16.0.74:9092,172.16.0.75:9092,172.16.0.76:9092'.split(','),
    'online_out':'39.96.5.102:9092,39.96.35.62:9092,39.96.34.104:9092'.split(','),
}


def get_kfk(env):
    return KafkaProducer(bootstrap_servers=KFKConfig[env],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8')
                         # key_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'),
                         # value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
                         )