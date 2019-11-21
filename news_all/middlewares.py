# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import datetime
import random
import time
from urllib.parse import urlparse
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from scrapy_redis.utils import bytes_to_str
from news_all.tools.agents import USER_AGENTS
from news_all.tools.proxy_work.location_proxy_feiyi import FeiYiProxy
from news_all.tools.proxy_work.proxy_tool import RandomProxy


class PhantomJSMiddleware(object):
    html_begin = r'<!--?xml version="1.0" encoding="UTF-8"?--><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>ok</title></head><body>'
    html_end = r'</body></html>'

    def __init__(self, timeout=30, service_args=None):
        # settings中PHANTOMJS_SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
        # chrome_options设置不缓存和禁用图片加载的功能，提高效率
        self.service_args = service_args
        self.timeout = timeout
        self.browser = None
        self.wait = None

    def open_browser(self):
        chrome_options = webdriver.ChromeOptions()  # todo 简洁写
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')
        self.browser = webdriver.Chrome(service_args=self.service_args,
                                        chrome_options=chrome_options)

        """
        browser初始内容self.browser.page_source是
        <html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>
        <iframe name="chromedriver dummy frame" src="about:blank"></iframe>
        </body></html>
        """

        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, 10)

    def process_request(self, request, spider):
        jstype = request.meta.get('jstype')
        if not jstype:
            return

        try:
            self.my_get(request.url)
        except Exception as e:
            return HtmlResponse(url=request.url, body='', request=request, encoding='utf-8', status=403)
        time.sleep(random.uniform(2, 4))

        if '<iframe name="chromedriver dummy frame" src="about:blank">' in self.browser.page_source:
            return HtmlResponse(url=request.url, body='', request=request, encoding='utf-8', status=403)

        return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                            status=200)

    def my_get(self, url):
        try:
            self.browser.get(url)
        except AttributeError:
            self.open_browser()
            time.sleep(2)
            self.browser.get(url)
        except WebDriverException as e:
            if e.msg == 'chrome not reachable':
                self.open_browser()
                time.sleep(2)
                return self.my_get(url)
            else:
                raise Exception('browser get url: %s, WebDriverException msg: %s' % (url, e.msg))
    
    @classmethod
    def from_crawler(cls, crawler):
        o = cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT', 30),
                service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS',
                                                  ['--load-images=false', '--disk-cache=false', '--ignore-ssl-errors=true', '--ssl-protocol=TLSv1']))
        crawler.signals.connect(o.idle, signal=signals.spider_idle)
        crawler.signals.connect(o.close, signal=signals.spider_closed)
        return o
    
    def close(self):
        try:
            if self.browser:
                self.browser.quit()
        except Exception as e:
            print(e)
        finally:
            self.browser = None
    
    def idle(self):
        self.close()


class UserAgentMiddleware(object):
    """This middleware allows spiders to override the user_agent"""
    
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(USER_AGENTS))


class ProxyMiddleware(object):
    # 随机取代理
    
    def __init__(self):
        self.feiyi = FeiYiProxy()
        
    def process_request(self, request, spider):
        ip_port = self.get_proxy(spider)
        if not ip_port:
            return
        request.meta['proxy'] = "http://" + ip_port

    def get_proxy(self, spider):
        try:
           # data = spider.server.rpop(self.feiyi.redis_key)   # todo 防止并发太大
            datas = spider.server.lrange(self.feiyi.redis_key, 0, 1)
        except Exception as e:
            return
        if datas:
            ip_proxy = bytes_to_str(datas[0], spider.redis_encoding)
        else:
            ip_proxy = self.feiyi.extract_ip_from_api()[0]
            spider.server.lpush(self.feiyi.redis_key, ip_proxy)
            spider.server.expire(self.feiyi.redis_key, datetime.timedelta(seconds=self.feiyi.time_out))
        return ip_proxy


class ProxyRdMiddleware(object):
    # 随机取代理 隧道代理
    
    def process_request(self, request, spider):
        RandomProxy.prepare_scrapy_request(request)   # 隧道代理


class FiddleRMiddleware(object):

    def process_request(self, request, spider):
        ip_port = spider.fiddle_ip_port  # "172.30.6.20:8888"
        request.meta['proxy'] = urlparse(request.url).scheme + "://" + ip_port


class NewsAllSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
