#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 13:01
# @Author  : wjq
# @File    : scheduler_redis.py
import datetime
from scrapy_redis.scheduler import Scheduler
from scrapy.conf import settings
from news_all.pipelines import save_logger_hive

# 不可以在spider中设置 去重key的过期时间, spider.custom_settings['REDIS_DUPEFILTER_KEY_EXPIRE_DAY']无效
# 只可通过settings文件设置, 默认是30天
dupefilter_key_expire_day = settings.getint('REDIS_DUPEFILTER_KEY_EXPIRE_DAY', 30)


class MyScheduler(Scheduler):
    def open(self, spider):
        super(MyScheduler, self).open(spider)
        """
        #  注意父类open中进行了flush操作
        if self.flush_on_start:
            self.flush()
        """
        if not self.flush_on_start:
            self.ttl_and_expire_key(self.df.key)
            self.ttl_and_expire_key(spider.name+':news_url')
    
    def ttl_and_expire_key(self, key):
        """
        :param key:
        :return:        检查并重新设置过期时间
        """
        # -1:没有设置过期时间, -2: 不存在这个key, 其他: 剩余生存时间单位秒
        ttl = self.server.ttl(key)
        if ttl == -1:
            self.server.expire(key, datetime.timedelta(days=dupefilter_key_expire_day))
            print('key: %s, 初次设置过期天数为: %s' % (key, dupefilter_key_expire_day))
            return
        if ttl == -2 or ttl == 0:
            return
        # 放弃: 若不存在key 则插入假定初始值。可使代码简洁, 让SelfFilterScheduler可继承MyScheduler,
        # 不必考虑
        # SELF_FILTER=True时self.df.key是有序集合插入初始值zadd(key, {'0', 0}),而基于source_id的自去重key是集合self.server.sadd(key, 0)。
        # SELF_FILTER=False时self.df.key 是集合 self.server.sadd(key, 0)
        
        ttl_day = round(ttl / (24 * 60 * 60))  # 单位天
        print('key: %s, 现在剩余生存天数是: %s' % (key, ttl_day))
        if ttl_day > dupefilter_key_expire_day:
            self.server.expire(key, datetime.timedelta(days=dupefilter_key_expire_day))
            print('key: %s, 重置过期天数为: %s' % (key, dupefilter_key_expire_day))
    
    def flush(self):
        super(MyScheduler, self).flush()
        self.server.delete(self.spider.name + ':news_url')  # int 1或者0
        # 分布式任务自产自销版本不可以在此处清空start_url,
        # 而在news_all.spider_models.DtbRedisMixin#setup_redis初始化start_url之前清空
        if settings.get('PARENT_CLS') != 'distribute':
            self.server.delete(self.spider.name + ':start_urls')
    
    def next_request(self):
        r = super(MyScheduler, self).next_request()
        if r:
            t = datetime.datetime.now()
            if r.meta.get('isStartUrl') is True:  # 所有在start_url翻页的都要设置为r.meta.get('isStartUrl') = True
                r.meta['start_url_time'] = t
                return r
            
            # todo news_url 通过url_date过滤
            r.meta['news_url_time'] = t
            return r


class SelfFilterScheduler(MyScheduler):
    """基于source_id自更新newsurl去重"""
    # def __init__(self, server, **kwargs):
    #     stats = kwargs.pop('stats', None)
    #     super(SelfFilterScheduler, self).__init__(server, **kwargs)
    #     self.stats = stats if stats else self.stats
        
    def open(self, spider):
        super(SelfFilterScheduler, self).open(spider)
        
        sourceid_df_keys = [self.df.key + ':' + str(i) for i in self.spider.source_id_meta_dict]
        if self.flush_on_start:
            for k in sourceid_df_keys:
                self.server.delete(k)
        else:
            # 基于source_id去重的redis key, 示例 'xinhuanet:dupefilter_zset:123'
            for k in sourceid_df_keys:
                self.ttl_and_expire_key(k)
            
    def enqueue_request(self, request):
        if request.meta.get('isStartUrl'):
            return super(SelfFilterScheduler, self).enqueue_request(request)
        
        # 推入source_id的去重队列 todo check2种方式哪种更好
        #  1. self.url_seen(url, source_id='') 好处：客户端和网站统一 用url去重, key={spider.name}:news_url{source_id}
        #  2. 采用 hash去重, key=self.df.key + ':{source_id}'
        source_id = request.meta['source_id']
        fp = self.df.request_fingerprint(request)
        self_added = self.server.sadd(self.df.key + ':' + str(source_id), fp)
        # if self_added == 0:
        #     return  # todo 线上被自己去重就直接返回

        root_added, master_sourceid = self.__enqueue_request(request, fp)
        
        # 四种情况:
        # 1. 被自己去重 被大池子去重(ok pass return)
        # 2. 被自己去重 大池子没去重(bad log)
        # 4. 自己没去重 被大池子去重(ok 如果master_source_id=source_id则打log标识被谁去重了, 否则return None)
        # 3. 自己没去重 大池子没去重(ok return True download)
        
        if not self_added:
            if not root_added:
                return
            else:  # 在大池子key到期被删的情况下产生bug: 被自己去重而没被大池子去重, 但爬虫任务还是入队了
                print('#' * 20, 'bug:  not self_added and root_added')
                return True
        else:
            if root_added:
                return True
            elif master_sourceid != source_id:  # 若source_id的自去重key到期被删, 而self.df.key还没被删。则导致没被自己去重但是被大池子去重了。权且认为是自更新
            # 这里产生debugitem不能进入pipeline
                save_logger_hive(
                    {
                        "spider_name": self.spider.name,
                        "source_id": source_id,
                        "origin_name_mongo": self.spider.source_id_meta_dict[source_id]['name'],
                        "srcLink": request.url,
                        "start_url_time": request.meta.get('start_url_time'),
                        "schedule_time": request.meta.get('schedule_time'),
                        # "news_url_time": '',  # todo check 若news_url_time为None 或没有news_url_time key how
                        "reason": 'duplicate filter',
                        "master_sourceid": str(master_sourceid)
                    }
                )
   
    def __enqueue_request(self, request, fp):
        """
        重写enqueue_request
        :param request:
        :return:    (True, None) 入队;  (False, source_id) 入队失败,被去重的source_id 入队失败被去重
        """
        if not request.dont_filter:
            master_sourceid = self.__request_seen(request, fp)
            if master_sourceid != None:
                self.df.log(request, self.spider)
                return False, int(master_sourceid)
        if self.stats:
            self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        self.queue.push(request)
        return True, None
    
    def __request_seen(self, request, fp):
        source_id = request.meta['source_id']
        added = self.server.zadd(self.df.key, {fp: source_id}, nx=True)  # nx=True不更新score即source_id
        if added == 0:  # 新增个数为0, 返回被去重的master_sourceid
            return self.server.zscore(self.df.key, fp)
