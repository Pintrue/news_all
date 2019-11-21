#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/28 18:29
# @Author  : wjq
# @File    : check_big_rate.py


#  db.getCollection('news_all_test_debug').find({kfk_ok_time:{'$gte': ISODate("2019-04-28T18:14:00.00Z")}}) // , '$lt': ISODate("2019-04-28T17:25:00.00Z")
from datetime import datetime
from news_all.db_method import DebugRW


def check_distinct(st, et, env='online_out', db=None):
    if not db:
        db = DebugRW(env)
    res = db.coll.find({'kfk_ok_time': {'$gt': st, '$lt': et}}, {'source_id': 1, 'srcLink': 1, 'kfk_ok_time': 1})
    
    total = 0
    url_set = set()
    sid_urls = {}  # {sid: []}
    
    for i in res:
        total += 1
        print(total)
        url = i.get('srcLink')
        sid = i.get('source_id')
        
        url_set.add(url)
        # sid_urls.setdefault({sid: []})  # todo why TypeError: unhashable type: 'dict'
        if sid not in sid_urls:
            sid_urls[sid] = [url]
        else:
            sid_urls[sid].append(url)
    
    print('==========%s~%s source_id总数: %s, kfk总数: %s, url去重后总数: %s, ===========\n' % (
    st, et, len(sid_urls), total, len(url_set)))
    
    sid_bug = set()  # 有重复新闻的source_id
    for i, j in sid_urls.items():
        t = len(j)
        dt = len(set(j))
        if t > dt:
            print('=========source_id:%s, total:%s, dutotal:%s ==========' % (i, t, dt))
            sid_bug.add(i)
    print('=========有重复新闻的source_id是:%s==========' % sid_bug)
    

if __name__ == '__main__':
    st = datetime(2019, 4, 29, 12, 50)  # 已确定是4月25日开始产生大量重复 解析, 大量发kfk
    et = datetime(2019, 4, 29, 13, 4)
    db = DebugRW('online_out')
    data = check_distinct(st, et, db=db)
