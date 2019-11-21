# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from copy import deepcopy
from datetime import datetime
from scrapy.conf import settings
from news_all.db_method import DebugRW
from news_all.tools.database_work.kafka_config import get_kfk
from news_all.items import NewsAllItem, DebugItem
from news_all.tools.logger_util import logger_hive

LOGGER_HIVE_COLS = settings.getlist("LOGGER_HIVE_COLS")


def save_logger_hive(postItem):
    # 打log 必须提供字段: spider_name,source_id, source_id, origin_name_mongo, reason
    info_map = deepcopy(settings.getdict("LOGGER_HIVE_MAP"))
    info_map["spider_name"] = postItem["spider_name"]
    info_map["sourceid"] = str(postItem["source_id"])
    info_map["sitename"] = postItem["origin_name_mongo"]

    if postItem.get("srcLink"):
        info_map["newsurl"] = postItem["srcLink"]

    title = postItem.get("title", "")
    info_map["title"] = title.replace('\r', '').replace('\n', '') if title else ""

    content = postItem.get("content", "")
    info_map["text"] = content.replace('\r', '').replace('\n', '') if content else ""

    reason = postItem["reason"]
    info_map["reason"] = reason
    if reason == "crawler normal":
        info_map["status"] = "normal"
    else:
        # 若log_type="list"则status="normal"也不代表是抓取新闻详情页成功只表明列表页刷新成功
        # 若log_type="gettask"则status="normal"也不代表是抓取新闻详情页成功只表明领取了任务
        info_map["status"] = postItem["status"] if postItem.get("status") else "abnormal"

    if postItem.get("crawlTimestamps"):
        info_map["capturetime"] = postItem["crawlTimestamps"]

    pubtime = postItem.get("pubtime")
    info_map["pubtime_real"] = pubtime if pubtime else ""

    if postItem.get("start_url_time"):  # debug start_url_time存mongo用datetime类型, log hive用13位时间戳
        # info_map["start_url_time"] = str(int(time.mktime(postItem["start_url_time"].timetuple())) * 1000)  # 缺点是被取整数了示例1564471236000
        info_map["start_url_time"] = '%.0f' % (postItem["start_url_time"].timestamp() * 1000)
    info_map["schedule_time"] = postItem["schedule_time"] if postItem.get("schedule_time") else ""

    media = postItem.get("media")
    info_map["media"] = json.dumps(media) if media else ""

    origin_name_parse = postItem.get("origin_name_parse")
    info_map["origin_name_parse"] = origin_name_parse.replace('\r', '').replace('\n', '') if origin_name_parse else ""

    if postItem.get("master_sourceid"):
        info_map["master_sourceid"] = postItem["master_sourceid"]
    if postItem.get("log_type") and postItem["log_type"] != info_map["log_type"]:
        info_map["log_type"] = postItem["log_type"]

    if info_map["status"] == "normal" or info_map["reason"] in (
    "pubtime 24 hours after", "pubtime 1 hours before") or "filter" in info_map["reason"]:
        log_fun = logger_hive.debug
    # elif info_map["reason"] in ("xpath error", "json error"):
    #     log_fun = logger_hive.warn
    else:
        log_fun = logger_hive.error
    log_fun("\u0001".join([info_map[i] for i in LOGGER_HIVE_COLS]))


class DebugPipeline(object):
    def __init__(self):
        self.debug_db = DebugRW(settings.get('DEBUG_DB_ENV', 'local'))  # todo 用新的log监控后del这行

    def open_spider(self, spider):
        print('%s DebugPipeline 开始爬虫' % spider.name)

    def process_item(self, item, spider):
        # KfkPipeline 的process_item,如果return None那么之后环节那个Pipeline就接收到这个None，所以必须return DebugItem
        if not isinstance(item, DebugItem):  # todo 用新的log监控后del这行
            return item
        postItem = dict(item)
        if postItem.get("reason") and postItem["reason"] != "crawler normal":  # todo 用新的log监控后del  if这行
            save_logger_hive(postItem)
        self.debug_db.insert(postItem)  # todo 用新的log监控后del这行
        return item

    def close_spider(self, spider):
        print('%s DebugPipeline 结束爬虫' % spider.name)
        self.debug_db.close()  # todo 用新的log监控后del这行


class KfkPipeline(object):
    def __init__(self):
        self.topic = settings.get('KAFKA_TOPIC', 'feed-1')
        self.producer = get_kfk(settings.get('KAFKA_ENV', 'local'))  # todo 调度测试后改回来

    def open_spider(self, spider):
        print('%s KfkPipeline 开始爬虫' % spider.name)

    def process_item(self, item, spider):
        if not isinstance(item, NewsAllItem):  # todo 改用log监控之后 删这句
            return item
        postItem = dict(item)

        debug_dict = postItem.pop("debugItem", {})  # todo 改用log监控之后 删这句
        print('@' * 20, '\n', postItem)

        # 入kafka之前的时间
        kfk_pre_time = datetime.now()
        self.producer.send(self.topic, postItem)  # todo 调度测试后改回来
        # 入kafka之后的时间
        kfk_ok_time = datetime.now()  # todo 改用log监控之后 废掉mongo debugItem kfk_ok_time
        debug_dict['kfk_pre_time'] = kfk_pre_time
        debug_dict['kfk_ok_time'] = kfk_ok_time

        save_logger_hive(deepcopy(debug_dict))  # 防止去\r\n的content存mongo 干扰备查
        others = ["crawlTimestamps", "pubtime_real", "origin_name_parse"]
        for i in others:
            try:
                postItem["extra"]["DEBUG_INFO"].pop(i)
            except:
                print()
        return DebugItem(debug_dict)  # todo 改用log监控之后 删这句

    def close_spider(self, spider):
        print('%s KfkPipeline 结束爬虫' % spider.name)
        self.producer.close()  # todo 调度测试后改回来


class KfkPipelineTest(KfkPipeline):
    def __init__(self):
        self.topic = settings.get('KAFKA_TOPIC', 'feed-1')
        self.producer = get_kfk(settings.get('KAFKA_ENV', 'test'))

    def process_item(self, item, spider):
        if not isinstance(item, NewsAllItem):
            return item
        item['extra']['etlDontDuplicate'] = True  # 在测试时, 设置etl不去重(方便在审核系统中查看新闻格式是否正确)
        # 在测试环境标识网站的中文名字
        item["title"] += ":" + spider.chinese_name
        return super(KfkPipelineTest, self).process_item(item, spider)


class KfkPipelineLocal(object):  # 本地只用来pop出debugItem todo 用更简单的方式获取debugItem
    def open_spider(self, spider):
        print('%s KfkPipeline 开始爬虫' % spider.name)

    def process_item(self, item, spider):
        if not isinstance(item, NewsAllItem):
            return item
        postItem = dict(item)
        debug_dict = postItem.pop("debugItem", {})
        # 入kafka之前的时间
        kfk_pre_time = datetime.now()
        # 入kafka之后的时间
        kfk_ok_time = datetime.now()  # todo 改用log监控之后 废掉mongo debugItem kfk_ok_time
        debug_dict['kfk_ok_time'] = kfk_ok_time

        save_logger_hive(deepcopy(debug_dict))  # 防止去\r\n的content发给kfk
        others = ["crawlTimestamps", "pubtime_real", "origin_name_parse"]
        for i in others:
            try:
                postItem["extra"]["DEBUG_INFO"].pop(i)
            except Exception as e:
                print(e)
        return DebugItem(debug_dict)  # todo 改用log监控之后 删这句

    def close_spider(self, spider):
        print('%s KfkPipeline 结束爬虫' % spider.name)


def make_source_meta(sid):
    s0 = {'source_id': 273, 'start_url': ['test'], 'site_weight': 8,
          'content_quality': 'HIGH_QUALITY', 'priority': 8, 'mode': None, 'category_first': '10000',
          'category_second': '100010', 'category_third': '', 'time_limitation': 'TIME_LIMITATION',
          'remove_duplicate': None,
          'media_type': ['CENTRAL_MEDIA', 'WHITE_LIST'], 'content_source': 'INTERNAL', 'rmw_copyright': 'NO_COPYRIGHT',
          'sourceType': None, 'name': '测试', 'direct_linkto': None, 'categories': [10100], 'addr': ''}
    s0['source_id'] = sid
    return s0


class KfkPipelineTestS0(KfkPipelineTest):
    # 假的sourceMeta, 在mongo source没有打标时提前 在审核系统测试环境看格式
    def process_item(self, item, spider):
        if not isinstance(item, NewsAllItem):
            return item
        sid = item["sourceMeta"]["source_id"]
        s0 = make_source_meta(sid)
        item['sourceMeta'] = s0
        item['extra']['sourceExtra'] = s0
        return super(KfkPipelineTestS0, self).process_item(item, spider)
