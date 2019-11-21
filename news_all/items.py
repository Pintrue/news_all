# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class NewsAllItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()  # 设置默认值无效
    debugItem = Field()
    id = Field()
    title = Field()  # 新闻标题
    content = Field()  # 正文
    summary = Field()  # 摘要
    pubtime = Field()   # 发布时间
    media = Field()
    srcLink = Field()
    sourceMeta = Field()
    origin = Field()
    createtime = Field()
    extra = Field()
    fetcherType = Field()
    scenes = Field()


class DebugItem(scrapy.Item):
    spider_name = Field()
    source_id = Field()
    title = Field()  # 新闻标题
    pubtime = Field()   # 发布时间
    origin_name_parse = Field()  # 爬虫解析出的新闻来源
    origin_name_mongo = Field()  # mongo source库 name字段
    content = Field()  # 正文
    media = Field()
    cover = Field()
    srcLink = Field()
    start_url_time = Field()  # 列表页请求时间, 也就是首次抽取到这条新闻的start_url的刷新时间
    schedule_time = Field()  # 从redis调度系统获取任务时，带过来的调度时间(时间戳13位)
    news_url_time = Field()   # 新闻详情页请求时间
    pubtime_str = Field()
    crawlTime = Field()
    crawlTimestamps = Field()
    delay_time = Field()
    kfk_pre_time = Field()
    kfk_ok_time = Field()
    reason = Field()
    log_type = Field()  # log 类型 列表页'list'或者详情页'detail' 或者 'get task'获取任务


class UrlSeenItem(scrapy.Item):  # 临时解决方案
    spider_name = Field()
    source_id = Field()
    srcLink = Field()