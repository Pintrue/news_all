#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/19 13:16
# @Author  : wjq
# @File    : spider_models.py
import json
import logging
import random
import re
from copy import deepcopy
import time
from datetime import datetime
from twisted.internet.error import *
from scrapy import FormRequest
from scrapy_redis.utils import bytes_to_str
from scrapy.conf import settings
from scrapy.exceptions import DontCloseSpider
from scrapy.http import Request, HtmlResponse
from scrapy.spiders import Spider, CrawlSpider
from scrapy_redis.spiders import RedisMixin
from scrapy.spidermiddlewares.httperror import HttpError
from news_all.db_method import SourceR
from news_all.tools.html_clean import NewsBaseParser, html2text
from news_all.tools.logger_util import get_logger
from news_all.tools.others import to_list
from news_all.tools.time_translater import get_datetime_ago
from news_all.pipelines import save_logger_hive
from news_all.tools.time_translater import nettime_to_pubtime, timestamps, Pubtime
from news_all.items import DebugItem, NewsAllItem, UrlSeenItem


p = re.compile(r'<title.*?>([\s\S]*?)</title>', re.I)
"""
大写
<TITLE>
农妇遭电信诈骗赴银行汇款 “偶遇”民警及时制止
-中国警察网</TITLE>
"""

parent_cls = settings.get("RUNNING_MODE", "once")


class MyTimer:
    def __init__(self, t, func, *vec):
        from twisted.internet import task
        self.lc = task.LoopingCall(func, *vec)
        self.t = t

    def start_thread(self):
        self.lc.start(self.t)


class NewsSpider(Spider):
    """从start_url开始根据parse函数解析，完成1轮就结束"""

    # mystart_urls必填, 示例: {'http://finance.ce.cn/': 206, }
    # 或 {'http://api.admin.cp.cashtoutiao.com/headLine/getVideoAndArticleNoCoverApi': [130, 131, 132, 133]}
    mystart_urls = {}

    # 如果start_url请求是post, 则start_method = "POST", post大小写都可以;
    # 如果不设置start_method或start_method.upper()!="POST", 则把start_url当成get请求处理
    start_method = None

    # 如果start_url需要请求头则填写, 示例: {"Host": "api.admin.cp.cashtoutiao.com", "User-Agent": "okhttp/2.7.1"}
    start_headers = {}

    # 如果start_url需要请求体则填写
    # 示例:{source_id1:(channel1, body1), source_id2:(channel2, body2), ...}   其中body为dict或str
    start_body_map = {}

    # 如果start_url需要提交表单则填写
    # 示例: {source_id1: (channel1,  formdata1), source_id2: (channel2,  formdata2), ...}
    # 其中formdata是列表页的请求行formdata, formdata必须dict
    start_formdata_map = {}

    # 如果start_url中的js必须要用浏览器渲染生成html, 则start_meta = {'jstype': True}
    # 如果start_url要做些标记, 可以设置start_meta
    start_meta = {}

    # 在调试时, 可以设置LimitatedDaysHoursMinutes放宽新闻发布时间限制, 它覆盖settings文件中的LDHM,
    # 示例: 限制只爬取10天15小时0分钟之内的新闻LimitatedDaysHoursMinutes = (10, 15, 0)
    LimitatedDaysHoursMinutes = ()

    parser = NewsBaseParser()

    # 在审核测试时, 可以设置Chinese_name, 方便运营人员走查格式
    chinese_name = ""

    # 调试时用，解析错误新闻详情url列表, 包括xpath、css、json、正则等错误
    url_parse_error = []

    intervals = 3600 * 8  # 每8小时同步一次source打标信息

    def __init__(self, *a, **kw):
        # assert self.mystart_urls, "spider class must set attr mystart_urls!"  # todo 升级为调度版本后 不要注释

        # source_id_channel_body, source_id_channel_formdata 不能同时存在
        assert not (self.start_body_map and self.start_formdata_map), "only one start_body_map or start_formdata_map"

        self.url_seen_set = set()  # 调试用

        # 优先从spider属性LimitatedDaysHoursMinutes中获取时间限制
        self.ldhm = self.LimitatedDaysHoursMinutes or settings.getlist('LDHM')
        if not self.ldhm:
            raise ValueError("%s have not a LimitatedDaysHoursMinutes eg: (1, 0, 0)" % type(self).__name__)
        self.ldhm2s = ((self.ldhm[0] * 24 + self.ldhm[1]) * 60 + self.ldhm[2]) * 60  # 转换为秒
        super(NewsSpider, self).__init__(*a, **kw)

        # 根据mystart_urls, start_method, start_headers, start_body_map, start_formdata_map生成mystart_reqs
        self.mystart_reqs = self.construct_start_requests()

        # 初始化打标信息
        self.source_id_meta_dict = self.construct_source_id_meta_dict()

        self.source_id_start_req_dict = {i.meta['source_id']: [] for i in self.mystart_reqs}
        for i in self.mystart_reqs:
            self.source_id_start_req_dict[i.meta['source_id']].append(i)

        self.log_parse_error = get_logger('parse_error_%s' % self.name,
                                          settings.get('PARSE_ERROR_LOG_FILE_ENABLED', True))

    def construct_start_requests(self):
        meta = deepcopy(self.start_meta)
        meta['isStartUrl'] = True  # 为start_url的刷新时间打点
        source_id_total = sum([len(to_list(j)) for i, j in self.mystart_urls.items()])  # source_id总数量
        method = "POST" if self.start_method and self.start_method.upper() == "POST" else "GET"
        mystart_reqs = []

        if self.start_formdata_map:
            # 优先判断 有无formdata
            assert source_id_total == len(self.start_formdata_map), "mystart_urls中source_id数量必须和start_formdata_map数量相同"

            for url, source_ids in self.mystart_urls.items():
                for source_id in to_list(source_ids):
                    meta['source_id'] = source_id
                    fs = self.start_formdata_map[source_id][1]  # 1个source_id有多种formdata
                    if isinstance(fs, list):
                        mystart_reqs.extend([FormRequest(
                            url,
                            # callback=self.parse, errback=self.catch_err,
                            method=method, headers=self.start_headers,
                            formdata=formdata, dont_filter=True,
                            meta=meta) for formdata in fs])
                    else:
                        r = FormRequest(
                            url,
                            # callback=self.parse, errback=self.catch_err,
                            method=method, headers=self.start_headers,
                            formdata=fs, dont_filter=True,
                            meta=meta)
                        mystart_reqs.append(r)
        else:
            # 允许有的start_url没有request body
            for url, source_ids in self.mystart_urls.items():
                # 兼容： 同样的start_url对应多个source_id
                sids = to_list(source_ids)
                for source_id in sids:
                    meta['source_id'] = source_id
                    if self.start_body_map.get(source_id):
                        bs = self.start_body_map[source_id][1]
                        if isinstance(bs, list):  # 1个source_id有多种body
                            for body_raw in bs:
                                body = json.dumps(body_raw) if isinstance(body_raw, dict) else body_raw
                                r = Request(url,
                                            # callback=self.parse, errback=self.catch_err,
                                            method=method,
                                            headers=self.start_headers, body=body,
                                            dont_filter=True, meta=meta)
                                mystart_reqs.append(r)
                        else:
                            body = json.dumps(bs) if isinstance(bs, dict) else bs
                            r = Request(url,
                                        # callback=self.parse, errback=self.catch_err,
                                        method=method,
                                        headers=self.start_headers, body=body,
                                        dont_filter=True, meta=meta)
                            mystart_reqs.append(r)
                    else:
                        body = None
                        # 不必有callback, 但是Cannot use errback without a callback
                        r = Request(url,
                                    # callback=self.parse, errback=self.catch_err,
                                    method=method,
                                    headers=self.start_headers, body=body,
                                    dont_filter=True, meta=meta)
                        mystart_reqs.append(r)

        return mystart_reqs

    def construct_source_id_meta_dict(self):
        source_id_meta_dict = {}
        try:
            source_reader = SourceR(settings.get('SOURCE_ENV', 'test'))
        except:
            self.log('spider:%s can not connect mongo source!' % self.name, logging.ERROR)
            source_reader = None
        for r in self.mystart_reqs:
            source_id = r.meta['source_id']
            source_id_meta_dict[source_id] = self.get_source_meta(source_reader, source_id)
        if source_reader:
            source_reader.close()

        return source_id_meta_dict

    def get_source_meta(self, source_reader, source_id):
        if source_reader:
            source_reader.update_spider_name(source_id=source_id, spider_name=self.name)
            source_meta = source_reader.get_source_meta(source_id=source_id)
            if source_meta:
                return source_meta
        else:
            self.log('source_id:%s, can not connect mongo' % source_id, logging.ERROR)
        self.log('source_id:%s, have no mongo source_id' % source_id, logging.ERROR)
        return {'name': 'test', "source_id": source_id}

    def start_requests(self):
        for r in self.mystart_reqs:
            yield r

    def catch_err(self, failure):
        """暂只捕获新闻详情页网络请求错误"""
        request = failure.request
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            item = self.produce_debugitem(response, 'HttpError: %s: status code=%s' % (failure.value, response.status))

        elif failure.check(DNSLookupError):
            item = self.produce_debugitem(request, 'DNSLookupError: %s' % failure.value)

        elif failure.check(TimeoutError, TCPTimedOutError):
            item = self.produce_debugitem(request, 'TimeoutError: %s' % failure.value)
        else:
            item = self.produce_debugitem(request, '%s : %s' % (failure.type, failure.value))
        save_logger_hive(item)

    def content_clean(self, content_div, need_video=False, kill_xpaths=None, img_re=None, video_prefix=""):
        """
        :param  content_div Selector, SelectorList, str_list, or str  通过xpath或css规则截取的正文部分
        :param  need_video  bool                   是否可通过html<video >标签src属性来抽取video url和cover属性获取视频封面图
        :param  kill_xpaths str or list            要删除的xpath节点, 比如广告、相关链接、点赞等杂质
        :param  img_re                             获取img标签的正则表达式
        :param  video_prefix                       视频url相对路径前缀
        :return tuple                              content_clean, media, videos, video_cover
        """
        return self.parser.content_clean(content_div, need_video, kill_xpaths, img_re, video_prefix)

    def __period_filter(self, _time):
        """
        弃用
        时效过滤, _time是否过时, 超过时限则返回True
        :param  _time   str or datetime or int
        """
        if isinstance(_time, Pubtime):
            _time = _time.datetime
        else:
            try:
                timestamps_10 = int(nettime_to_pubtime(_time)[:-3])
                _time = datetime.fromtimestamp(timestamps_10)
            except:
                raise TypeError("period_filter _time should be datetime.datetime or str or int or Pubtime")
        return _time < get_datetime_ago(*(self.ldhm))

    def video_filter(self, sel_div):
        return self.parser.video_filter(sel_div)

    def produce_item(self, response, **kwargs):
        """
         过滤掉缺发布时间/正文/标题的新闻
        """
        sourceId = response.meta['source_id']
        if response.meta.get('isStartUrl') is True:
            assert kwargs.get('srcLink'), '从列表页就解析到新闻详情必须传参srcLink=news_url'
            if self.__url_seen(kwargs['srcLink']):
                return UrlSeenItem(spider_name=self.name,
                                   source_id=sourceId,
                                   srcLink=kwargs['srcLink'])
                # todo 怎么解决parse函数yield None让scrapy 调度底层不报错 或者 item = produce_item  if item return item
                # elif parent_cls == 'dispatch':
                # 只有调度版才需要统计累计 每次领取调度任务后source_id产生自更新新闻量
                # schedule_time = response.meta.get('schedule_time')
                # self.crawler.stats.inc_value('update_news_count/%s/%s' % (sourceId, schedule_time), 1)

        videos = kwargs.get('videos')
        media = kwargs.get("media", {})

        sourceMeta = deepcopy(self.source_id_meta_dict.get(sourceId, {}))
        if videos and videos.get('1') and videos['1'].get('src'):
            media['videos'] = videos
            """
            "videos": {
                    "1": {
                        "duration": 0,
                        "video_size": "22.99MB",
                        "src": "http://flv4.people.com.cn/.mp4",
                        "video_type": "mov"
                }
            """
            sourceMeta["displayTemplate"] = {
                "MessageType": {"name": "VIDEO"}
            }
            """
            #  什么情况加文本标识？或者不必要
            #  新闻中有视频就加标识   $..sourceMeta.displayTemplate.MessageType.name = "VIDEO"
            #  新闻中只有图无文字无其他  $..sourceMeta.displayTemplate.MessageType.name = "IMAG"
    
            #  举例
            FeedMessage = {...
                            "sourceMeta": {
                                    "displayTemplate":{
                                            "MessageType": { "name": "VIDEO"}
    
                                    },
                                    ...
                                    }
    
                            }
            """

        title = kwargs.get("title", response.request.meta.get('link_text'))
        title = html2text(title) if title else ""  # 基类清洗来源中的html标签和换行和回车

        content = kwargs.get("content", "")

        srcLink = kwargs.get("srcLink") or response.url  # 若从列表页直接返回新闻详情则srcLink字段
        name = sourceMeta['name']
        time_str = datetime.now()
        crawl_time = datetime.strftime(time_str, '%Y-%m-%d %H:%M:%S')
        crawlTimestamps = '%.0f' % (time_str.timestamp() * 1000)
        origin_parse = kwargs.get("origin_name") if kwargs.get(
            "origin_name") else ""  # 防止kwargs.get("origin_name")为None
        # 有这种来源"经济日报              \r\n               　\r\n              作者\r\n                            林火灿"
        if origin_parse:
            origin_parse = html2text(origin_parse).replace('来源', '').replace(':', '').replace('：',
                                                                                              '').strip()  # 基类清洗来源中的html标签和换行和回车
        if origin_parse and ('\r' in origin_parse or '\n' in origin_parse):
            origin_parse = origin_parse.split()[0].strip()

        debug_item = DebugItem(
            {
                "spider_name": self.name,
                "source_id": sourceId,
                "title": title,
                "pubtime": None,
                "origin_name_parse": origin_parse,
                "origin_name_mongo": name,
                "content": content,
                "media": media,
                "srcLink": srcLink,
                'start_url_time': response.meta.get('start_url_time'),  # start_url刷新的时间
                'schedule_time': response.meta.get('schedule_time'),
                "news_url_time": response.meta.get('news_url_time'),  # 新闻详情页刷新的时间
                "pubtime_str": None,
                "crawlTime": time_str,  # produce_item的时间
                "crawlTimestamps": crawlTimestamps,
                "delay_time": None,  # 爬虫延时单位s
                "reason": "crawler normal",  # 先假定抓取正常再通过判断是否存在发布时间 正文 标题 来修改
            }
        )

        pubtime_kw = kwargs.get("pubtime")
        if pubtime_kw:
            try:
                pubtime = nettime_to_pubtime(pubtime_kw)
            except:
                return self.produce_debugitem(response, reason='pubtime parse error: %s' % pubtime_kw, srcLink=srcLink)
            delay_time = int(time.mktime(time_str.timetuple())) - int(pubtime) // 1000
            if delay_time > self.ldhm2s:
                return self.produce_debugitem(response, 'pubtime 24 hours after', srcLink=srcLink)
            if delay_time < -3600:  # 防止新闻网页发布时间超前超过1个小时
                return self.produce_debugitem(response, 'pubtime 1 hours before', srcLink=srcLink)

            # 方法二
            # dela = time_str-datetime.fromtimestamp(int(pubtime)//1000)
            # get_delay_time = dela.days*86400 + dela.seconds

            debug_item["pubtime"] = pubtime
            debug_item["delay_time"] = delay_time
            debug_item["pubtime_str"] = datetime.fromtimestamp(int(pubtime) // 1000)
        else:
            debug_item["reason"] = 'pubtime is null'
            debug_item["content"] = debug_item.get("content", "")[: 20]  # 如果pubtime没解析到, 打log只取正文前20个字符
            return debug_item

        new_content = re.sub('<[^<]+?>', '', content).replace('\n', '').strip()  # 去除正文中的标签
        if not title or not new_content:
            if not title and not new_content:
                reason = 'title and content is null'
            elif not new_content:
                reason = 'content is null'
            else:
                reason = 'title is null'
                debug_item["content"] = debug_item.get("content", "")[: 20]  # 如果title没解析到, 打log只取正文前20个字符
            debug_item["reason"] = reason
            return debug_item
        item = NewsAllItem(
            {
                "debugItem": dict(debug_item),  # todo 通过log监控之后就del 这行， 因为正常抓取的新闻log已在kfk pipline中打了
                "id": None,
                "title": title,
                "content": content,
                "summary": kwargs.get("summary", ""),  # 暂先不写 之前crawler是取content_text[:100]
                "pubtime": crawlTimestamps,  # pubtime,  5月5日改为抓取时间13位时间戳
                "media": media,
                "srcLink": srcLink,
                "sourceMeta": sourceMeta,
                "origin": {"origin_url": srcLink, "origin_name": origin_parse or name},
                "createtime": timestamps(),
                "extra": {"DEBUG_INFO": {
                    "sourceId": sourceId,
                    "srcLink": srcLink,
                    "CRAWL_ID": "r" + str(int(time.time())) + str(sourceId),  # r+timestamp+sourceId
                    "crawlTime": crawl_time,
                    "crawlTimestamps": crawlTimestamps,
                    "pubtime_real": pubtime,
                    "origin_name_parse": origin_parse,
                    # others = ["crawlTimestamps", "pubtime_real", "origin_name_parse"]不必要发kfk只是为了打hive_log中的爬取时间戳, 解析的新闻发布时间和来源
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",  # 随意
                    "CRAWLER_ENV": "online", },
                    "sourceExtra": sourceMeta},
                "fetcherType": sourceMeta.get("fetcherType"),  # sourceType
                "scenes": sourceMeta.get("scenes")}
        )

        if kwargs.get('cover'):  # 列表页缩略图 todo 暂时没有爬封面图
            item['extra']['cover'] = kwargs.get('cover')
        return item

    def produce_debugitem(self, res_or_req, reason, **kwargs):
        """
        :param reason:   str    "json error" or "xpath error"
        :return:
        """
        sourceId = res_or_req.meta.get('source_id')

        # 直观存log文件 用于本地调试, 测试环境/线上不必要
        if parent_cls in ('once', 'single') and reason in ('json error', 'xpath error'):
            self.saveurl_parse_error(res_or_req.url, sourceId)

        crawlTime = datetime.now()

        return DebugItem(
            {
                "spider_name": self.name,
                "source_id": sourceId,
                "origin_name_mongo": self.source_id_meta_dict[sourceId]['name'],
                "srcLink": kwargs['srcLink'] if kwargs.get('srcLink') else res_or_req.url,
                "start_url_time": res_or_req.meta.get('start_url_time'),
                "schedule_time": res_or_req.meta.get('schedule_time'),
                "news_url_time": res_or_req.meta.get('news_url_time'),
                "crawlTime": crawlTime,
                "crawlTimestamps": '%.0f' % (crawlTime.timestamp() * 1000),
                "reason": reason,
                "log_type": 'list' if (
                        'pubtime' not in reason and res_or_req.meta.get('isStartUrl') is True) else 'detail'
            }
        )

    def get_page_title(self, response):
        """网页标题"""
        ss = p.search(response.text)
        if ss:
            return ss.group(
                1).strip()  # '\n农妇遭电信诈骗赴银行汇款 “偶遇”民警及时制止\n-中国警察网'.strip() ==> '农妇遭电信诈骗赴银行汇款 “偶遇”民警及时制止\n-中国警察网'
        else:
            # '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body><iframe name="chromedriver dummy frame" src="about:blank"></iframe></body></html>'
            print('正则不出 网页标题')

    def saveurl_parse_error(self, url, source_id):
        if url not in self.url_parse_error:
            self.url_parse_error.append(url)
            self.log_parse_error.error('source_id:%s, %s, %s' % (source_id, datetime.now(), url))

    def __url_seen(self, url):
        if parent_cls == "once":  # 或者 if not hasattr(self, server) or not self.server:
            # 写解析调试爬虫用的函数 在解析列表页就解析出新闻详情页时对news_url去重
            if url in self.url_seen_set:
                return True
            self.url_seen_set.add(url)
        else:  # todo url_seen函数放到scheduler中
            added = self.server.sadd('%s:news_url' % self.name, url)
            if added:
                print('是更新了')
            return added == 0


class NewsCrawlSpider(CrawlSpider, NewsSpider):
    """从start_url 根据Rule抽取链接，单次爬虫，完成1轮就结束"""

    def __init__(self, *args, **kwargs):
        super(NewsCrawlSpider, self).__init__()
        self.url_others = set()  # rule
        self.log_others_url = get_logger('others_url_%s' % self.name, settings.get('OTHERS_URL_LOG_FILE_ENABLED', True))

    def saveurl_others(self, response):
        if response.url not in self.url_others:
            self.url_others.add(response.url)
            self.log_others_url.warn(
                'source_id:%s, %s, %s' % (response.meta.get('source_id'), datetime.now(), response.url))

    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            return  # todo self.crawler.sheduler.stats.setvalue('sid/start_url_time/count_requests_to_follow', 0)
        # count_requests_to_follow = 0
        news_reqs = []
        for r in super(NewsCrawlSpider, self)._requests_to_follow(response):
            if not r.meta.get('source_id'):
                r.meta['source_id'] = response.meta.get('source_id')

            # otherurl 不要发网络请求只打log
            if r.meta.get('otherurl'):
                self.saveurl_others(r)
                continue
            if not r.meta.get('isStartUrl'):
                r.errback = self.catch_err  # 暂只对新闻详情页监控网络错误
                news_reqs.append(r)
            r.meta['start_url_time'] = response.meta.get('start_url_time')
            r.meta['schedule_time'] = response.meta.get('schedule_time')
            yield r


class MyRedisMixin(RedisMixin):
    sleep_time = 6

    def next_requests(self):
        """Returns a request to be scheduled or none."""
        for r in self.mystart_reqs:
            time.sleep(random.uniform(2, 8))  # todo check 延时是否足够
            yield r  # 之后入队而不是发请求

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        # XXX: Handle a sentinel to close the spider.
        self.schedule_next_requests()
        print(self.name, 'sleep---' * 10)
        time.sleep(self.sleep_time)
        raise DontCloseSpider


class DtbRedisMixin(MyRedisMixin):
    """分布式爬虫, 爬虫启动时把source_id都推入redis, 每一轮从redis中取几个source_id, 再还回redis"""

    def next_requests(self):
        """Returns a request to be scheduled or none."""
        # redis_key默认列表而不是集合 临时版分布式爬虫必须用列表 lpop rpush
        fetch_one = self.server.lpop
        supply_one = self.server.rpush

        found = 0
        while found < min(self.redis_batch_size, len(self.source_id_start_req_dict)):
            data = fetch_one(self.redis_key)
            if not data:
                break
            source_id = int(bytes_to_str(data, self.redis_encoding))
            reqs = self.source_id_start_req_dict.get(source_id, [])
            for req in reqs:
                yield req
                found += 1
            supply_one(self.redis_key, data)

    def setup_redis(self, crawler=None):
        super(DtbRedisMixin, self).setup_redis(crawler)
        # 每启动爬虫就把mystart_urls中的url存入redis
        if settings.getbool('SCHEDULER_FLUSH_ON_START'):
            self.server.delete(self.redis_key)
        if self.source_id_start_req_dict:
            self.server.rpush(self.redis_key, *list(self.source_id_start_req_dict.keys()))


class DispRedisMixin(MyRedisMixin):
    """
    分布式调度爬虫, 爬虫每一轮都从redis取时间戳最小的那1个source_id, 若能取到就爬虫若不能取到就再取；
    爬完一轮任务之后不等待, 立马从redis获取下一轮任务
    """
    sleep_time = 0

    def next_requests(self):
        """Returns a request to be scheduled or none."""
        source_id = None
        while not source_id:
            source_id, schedule_time = self.fetch_one()
        # todo 升级为超过20分钟还取不到任务就kill进程

        reqs = self.source_id_start_req_dict.get(source_id, [])
        for req in reqs:
            meta = deepcopy(req.meta)
            meta['schedule_time'] = schedule_time
            r = req.replace(url=req.url, meta=meta)
            # req.meta['schedule_time'] = schedule_time
            yield r  # 注意为此时发出的start_req 更新meta['schedule_time'], 则修改了原来的start_req的meta 可用Request.replace避免

    def fetch_one(self):
        source_id_time_in = self.server.zrange(self.redis_key, 0, 0, desc=False, withscores=True)
        if not source_id_time_in:
            return None, None

        sid = source_id_time_in[0][0]
        source_id = int(bytes_to_str(sid, self.redis_encoding))
        time_in = '%0.f' % source_id_time_in[0][1]  # 1565847491130.0
        # 初始化统计 某次source_id调度产生新新闻数量=0
        # self.crawler.stats.set_value('update_news_count/%s/%s' % (source_id, time_in), 0)
        # from scrapy.statscollectors import MemoryStatsCollector
        """
        <scrapy.statscollectors.MemoryStatsCollector object at 0x0000026BE96DD860>
        _dump=True
        _stats = {'log_count/INFO': 8, 'start_time': datetime.datetime(2019, 8, 15, 4, 39, 38, 689034)}
        """
        save_logger_hive({
            "spider_name": self.name,
            "source_id": source_id,
            "origin_name_mongo": self.source_id_meta_dict[source_id]['name'],
            "reason": "get task",
            "status": "normal",
            "log_type": "get task",
            "schedule_time": time_in
        })

        # if self.server.zrem(self.redis_key, *[sid]):  # 这样也可以
        if self.server.zrem(self.redis_key, sid):
            return source_id, time_in
        else:
            return None, None


if parent_cls == "once":
    NewsRSpider = NewsSpider
    NewsRCSpider = NewsCrawlSpider

elif parent_cls in ['single', 'distribute', 'dispatch']:
    if parent_cls == 'single':
        parent_class = MyRedisMixin
    elif parent_cls == "distribute":
        parent_class = DtbRedisMixin
    else:
        parent_class = DispRedisMixin


    class NewsRSpider(parent_class, NewsSpider):
        @classmethod
        def from_crawler(self, crawler, *args, **kwargs):
            obj = super(NewsRSpider, self).from_crawler(crawler, *args, **kwargs)
            obj.setup_redis(crawler)
            return obj


    class NewsRCSpider(parent_class, NewsCrawlSpider):
        @classmethod  # todo why 若不写这个类属性爬取一轮程序就结束
        def from_crawler(self, crawler, *args, **kwargs):
            obj = super(NewsRCSpider, self).from_crawler(crawler, *args, **kwargs)
            obj.setup_redis(crawler)
            return obj

else:
    raise ValueError('RUNNING_MODE set wrong!')


def dont_fr(x):
    x.priority = 1
    x.dont_filter = True
    return x


def js_meta(x):
    x.meta['jstype'] = True
    return x


def otherurl_meta(x):
    """
    标识此request是从列表页抽取出来的其他样式的url
    就不发网络请求
    """
    x.meta['otherurl'] = True
    return x


def isStartUrl_meta(x):
    """
    标识此request是列表页 可能是列表的翻页, 列表页的翻页不能计入列表页更新的新闻url数量
    用于打log记录刷新列表的时间
    """
    x.meta['isStartUrl'] = True
    return dont_fr(x)


__all__ = ['NewsRSpider', 'NewsRCSpider', 'dont_fr', 'otherurl_meta', 'isStartUrl_meta']
