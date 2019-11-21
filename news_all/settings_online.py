# -*- coding: utf-8 -*-

# Scrapy settings for news_all project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

from datetime import datetime

BOT_NAME = 'news_all'

# SPIDER_MODULES = ['news_all.spiders', 'news_all.spiders_wap', 'news_all.spiders_four', 'news_all.spiders_video',
#                   'news_all.spiders_all', 'news_all.spiders_all2', 'news_all.spiders_old', 'news_all.spiders_old2',
#                   'news_all.spiders_ydyl', 'news_all.spiders_meiwen', 'news_all.spiders_difang']

NEWSPIDER_MODULE = 'news_all.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'news_all (+http://www.yourdomain.com)'
# Obey robots.txt rules
ROBOTSTXT_OBEY = False  # 默认True
DEPTH_LIMIT = 1  # 与start_urls中定义url的相对值
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 5  # 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 5  # 16
CONCURRENT_REQUESTS_PER_IP = 1  # 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }
"""
scrapy 原始headers  
{
b'Accept': [b'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'], 
b'Accept-Language': [b'en'], 
b'Accept-Encoding': [b'gzip,deflate']}
"""
# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
# 'news_all.middlewares.NewsAllSpiderMiddleware': 543,

# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
PC_DWON = {
    # 'news_all.middlewares.PhantomJSMiddleware': 10,
    'news_all.middlewares.UserAgentMiddleware': 20,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None,
    # 'news_all.middlewares.ProxyMiddleware': 100,
}

APP_DOWN = {
    # 'news_all.middlewares.PhantomJSMiddleware': 10,
    # 'news_all.middlewares.APPUserAgentMiddleware': 20,  # 不一定全是okhttp/3.10.0请求框架  海客是的
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None,
    # 'news_all.middlewares.ProxyMiddleware': 100,
}

DOWNLOADER_MIDDLEWARES = PC_DWON
from copy import deepcopy

DOWNLOADER_MIDDLEWARES_NOREDICT = deepcopy(DOWNLOADER_MIDDLEWARES)
DOWNLOADER_MIDDLEWARES_NOREDICT['scrapy.downloadermiddlewares.redirect.RedirectMiddleware'] = None

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


to_day = datetime.now()
# LOG_FILE = '../log/scrapy_{}_{}_{}_{}_{}.log'.format(to_day.year, to_day.month, to_day.day, to_day.hour, to_day.minute)
LOG_ENCODING = 'utf-8'

# 只抓最近1天的新闻（LimitatedDaysHoursMinutes） settings文件只认大写
LDHM = (1, 0, 0)

IMG_PREFIX = 'http://43.250.238.143/pic/article/'

COMMANDS_MODULE = 'news_all.commands'  # 项目名称.目录名称

# 是否需要基于source_id自去重 只有基于自去重模式才可以在hive 统计出log_type='stats'获取update_news_count
# todo 否则表示基于大池子去重的更新量  news_all.scheduler_redis.MyScheduler 重写enqueue函数进行统计
SELF_FILTER = True

# RUNNING_MODE = "once"        # 单机跑一轮
# RUNNING_MODE = "single"      # 单机增量不间断
# RUNNING_MODE = "distribute"  # 分布式, 任务自产自销
RUNNING_MODE = "dispatch"    # 分布式调度版
KAFKA_ENV = 'online'  # ’local’, 'psw', 'test', 'online', 'online_out'
if RUNNING_MODE != "once":
    ITEM_PIPELINES = {
        # 'scrapy_redis.pipelines.RedisPipeline': 100,
        'news_all.pipelines.DebugPipeline': 350,  # 存debug_item:各环节时间、数量记录
        'news_all.pipelines.KfkPipeline': 300,
    }
    
    SCHEDULER = 'news_all.scheduler_redis.MyScheduler'  # 原生的scrapy redis"scrapy_redis.scheduler.Scheduler"
    SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'
    DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
    if SELF_FILTER:
        SCHEDULER = 'news_all.scheduler_redis.SelfFilterScheduler'
        SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter_zset'
    
    SCHEDULER_QUEUE_KEY = '%(spider)s:requests'  # 调度器中请求存放在redis中的key
    # LifoQueue 默认使用优先级队列（默认），其他：SpiderPriorityQueue,PriorityQueue（有序集合），FifoQueue（列表）、LifoQueue（列表）
    SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
    # 是否==h在关闭时候保留原来的调度器和去重记录，True=保留，False=清空 # 默认值False todo 关闭程序之前Requests queue入redis了？
    SCHEDULER_PERSIST = True
    # 是否在开始之前清空 调度器和去重记录，True=清空，False=不清空
    SCHEDULER_FLUSH_ON_START = False
    # 注意分布式尽量 SCHEDULER_PERSIST = True, SCHEDULER_FLUSH_ON_START = False
    # SCHEDULER_IDLE_BEFORE_CLOSE = 0  # 去调度器中获取数据时，如果为空，最多等待时间（最后没数据，未获取到）。 default 0
    DUPEFILTER_DEBUG = True
    # 去重队列过期天数 day*24*60*60
    REDIS_DUPEFILTER_KEY_EXPIRE_DAY = 30


DEBUG_DB_ENV = 'online'

SOURCE_ENV = 'online'

KAFKA_TOPIC = 'feed-1'

REDIS_HOST = "r-2zef9c4f9bce7d04.redis.rds.aliyuncs.com"  # online
REDIS_PORT = 6379

LOG_LEVEL = 'ERROR'
OTHERS_URL_LOG_FILE_ENABLED = False   # 不保存各spider的others_url的log文件
PARSE_ERROR_LOG_FILE_ENABLED = False   # 不保存各spider的parse_error的log文件
TELNETCONSOLE_USERNAME = 'scrapy'
TELNETCONSOLE_PASSWORD = 'scrapy'

STATS_KEYS = ['downloader/request_count', 'downloader/response_count', 'downloader/response_status_count/200',
              'item_scraped_count']

# logger 格式用'\u0001'拼接顺次这些字段
LOGGER_HIVE_COLS = ["systemname", "sourceid", "sitename", "newsurl", "title", "text", "reason", "status", "capturetime",
                    "pubtime_kafka", "pubtime_real", "media", "origin_name_parse", "spider_name", "start_url_time",
                    "master_sourceid", "log_type", "schedule_time"]
# logger 字段默认值
LOGGER_HIVE_MAP = {
    "systemname": "core_crawler",   # 'core_crawler':核心爬虫
    "sourceid": "",
    "sitename": "",                 # 运营人员打标的和source_id相应的来源网站名称(mongo数据库的source表)
    "newsurl": "",                  # 新闻网址
    "title": "",                    # 新闻标题(去\n\r)
    "text": "",                     # 新闻正文(去\n\r)
    "reason": "",
    "status": "",
    "capturetime": "",
    "pubtime_kafka": "",
    "pubtime_real": "",
    "media": "",
    "origin_name_parse": "",  # 爬虫解析拿到的新闻来源
    "start_url_time": "",     # 爬虫获取这条新闻的来自于哪次刷新列表的时间(时间戳13位)
    "master_sourceid": "",    # 当reason="duplicate filter"时, 被哪个source_id的新闻去重了
    "log_type": "detail",     # "gettask"从redis调度系统获取1次任务;"list"列表页; "detail"新闻详情页
    "schedule_time": "",      # 从redis调度系统获取任务时，带过来的调度时间(时间戳13位)
    # "update_news_count": "",  # 当log_type="list"
}

DOWNLOAD_TIMEOUT = 120  # 秒, 默认180秒
REDIRECT_ENABLED = False
COOKIES_ENABLED = False
TELNETCONSOLE_PORT = [6023, 7423]


# 工程所有warning级日志接入sentry
# DSN = 'http://d8823f6329204194b8ccd400188574e4@39.105.14.86:9000/2'  # 线上环境
DSN = 'http://d8823f6329204194b8ccd400188574e4@172.16.0.111:9000/2'  # 线上环境 因为堡垒机所以用内网IP
if DSN:
    import logging
    from scrapy.utils.log import configure_logging

    configure_logging(install_root_handler=False)    # 可以没有，不过推荐加上

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,

        'formatters': {
            'console': {
                'format': '[%(asctime)s][%(levelname)s] %(name)s '
                          '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
                'datefmt': '%H:%M:%S',
            },
        },

        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'console'
            },
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.handlers.logging.SentryHandler',
                'dsn': DSN,
            },
        },

        'loggers': {
            '': {
                'handlers': ['console', 'sentry'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }
    logging.config.dictConfig(LOGGING)
