# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
import re
from urllib.parse import urlsplit, urljoin
import os
# from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class CnrSpider(NewsRCSpider):
    """央广网"""
    name = 'cnr'
    mystart_urls = {
        'http://finance.cnr.cn/': 193,  # '财经',
        'http://military.cnr.cn/': 194,  # '军事',
        'http://www.cnr.cn/chanjing/': 195,  # '产经',
        'http://gongyi.cnr.cn/': 601,  # 公益
        'http://health.cnr.cn/': 602,  # 健康
        'http://news.cnr.cn/native/': 603,  # 国内
        'http://news.cnr.cn/gjxw/': 604,  # 国际
        'http://tech.cnr.cn/': 605,  # 科技
        'http://military.cnr.cn/sdpl/': 606,  # 深度评论
        'http://www.cnr.cn/chanjing/jujiao/': 607,  # 城市聚焦
        'http://www.cnr.cn/chanjing/guancha/': 608,  # 产经观察
        'http://tech.cnr.cn/techit/': 609,  # IT业界
        'http://military.cnr.cn/zgjq/': 610,  # 中国军情
        'http://military.cnr.cn/gjjs/': 611,  # 国际军事
        'http://health.cnr.cn/jkbgt/': 612,  # 曝光台
        'http://tech.cnr.cn/techyd/': 613,  # 移动互联
        'http://auto.cnr.cn/2015xc/': 614,  # 新车
        'http://news.cnr.cn/theory/': 617,  # 理论
        'http://news.cnr.cn/comment/': 618,  # 评论
        'http://finance.cnr.cn/2014jingji/stock/': 619,  # 证券市场
        'http://finance.cnr.cn/2014jingji/djbd/': 620,  # 独家报道
    }
    custom_settings = {
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        # 'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    # http://military.cnr.cn/gz/20190130/t20190130_524498034.html
    # http://military.cnr.cn/wqzb/ddtp/20180710/t20180710_524296222.html
    rules = (
        Rule(LinkExtractor(allow=(r'cnr.cn/.*?/%s\d{2}/t\d+_\d+\.s?html' % datetime.today().strftime('%Y%m'),),
                           # 排除视频r'tv.cnr.cn/'
                           deny=(r'\.cnr\.cn/native/city/', r'\.cnr\.cn/(?:js2014/)?jssp', 'cnr_404', r'tv.cnr.cn/')),
             callback='parse_item', follow=False),

        Rule(LinkExtractor(allow=(r'cnr\.cn.*?\d+\.s?htm'),
                           deny=(r'\.cnr\.cn/native/city/', r'\.cnr\.cn/(?:js2014/)?jssp',
                                 'cnr_404', r'/201[0-8]', r'/20190[1-9]/', r'tv.cnr.cn/')),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        pagetype = xp(
            '/html/head/meta[@name="pagetype"]/@content').extract_first("")
        if pagetype == "2":
            return self.parse_images(response)

        try:
            content_div = xp('//div[@class="TRS_Editor" or @class="content" or @class="article-body"]')[0]
            pubtime = xp('//div[@class="source"]/span[1]/text()').extract_first('') or\
                      xp('//span[@id="pubtime_baidu"]/text()').extract_first()
            origin_name = xp('//div[@class="source"]/span[2]/text()').extract_first('')
            content, media, *_ = self.content_clean(content_div)
        except BaseException:
            return self.parse_item2(response)

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('_')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item2(self, response):
        xp = response.xpath
        try:
            # "/html/body/div[1]/div[1]/p[2]"
            title_div = xp(
                "/html/body/div[@class='wh960 margin']/div[1]/p[2]")[0]
            source_div = xp(
                "/html/body/div[@class='wh960 margin']/div[1]/span[1]")[0]
            source = source_div.xpath('./text()').extract()
            pubtime = source[0].strip()
            origin_name = source[1]
            content_div = xp('//div[@class="TRS_Editor" or @class="content"]')[0]
            title = ''.join(i.strip()
                            for i in title_div.xpath('./text()').extract())
            content, media, *_ = self.content_clean(content_div)
        except BaseException:
            return self.parse_item3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item3(self, response):
        xp = response.xpath
        try:
            source_div = xp('.//div[@class="left lh24 f12_5a5a5a"]')[0]
            time_re = source_div.re(
                r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
            content_div = response.xpath('.//div[@class="ScrCont"]')[0]
            og = source_div.re(r'来源：(\w{2,})')
            origin_name = og[0] if og else ""
            content, media, *_ = self.content_clean(content_div)
        except BaseException:
            return self.parse_item24(response)

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('_')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item24(self, response):
        try:
            news_div = response.xpath(
                './/div[@id="Area"]/div[@class="wh635 left"]/div[@class="wh610 left"]')[0]
            head_div = news_div.xpath('.//p')[0]
            content_div = news_div.xpath('.//div[@class="TRS_Editor"]')[0]
            pubtime = head_div.xpath('./span/text()')[0].extract().strip()
            title = ''.join(i.strip()
                            for i in news_div.xpath('./h1/text()').extract())
            origin_name = head_div.xpath(
                './/span[@id="source_baidu"]/text()').extract_first('')
            content, media, *_ = self.content_clean(content_div)
        except BaseException:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_images(self, response):
        # http://military.cnr.cn/zgjq/20190411/t20190411_524573865.html
        # http://military.cnr.cn/jstp/jstph/20190409/t20190409_524571960.html
        xp = response.xpath
        try:
            source_div = xp('.//div[@class="left lh24 f12_5a5a5a"]')[0]
            time_re = source_div.re(
                r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            # createPageHTML(5, 2, "t20190411_524573865", "html")
            total = re.search(
                r'createPageHTML\((\d+), \d+, "\w+", "html"\)',
                response.text).group(1)
            total = int(total)
            content_div = xp(r'//div[@class="TRS_Editor"]')[0]
        except BaseException:
            return self.produce_debugitem(response, "xpath error")
        og = source_div.re(r'来源：(\w{2,})')
        origin_name = og[0] if og else ""
        title = self.get_page_title(response).split('_')[0]
        if total > 1:
            return response.follow(url=self._next_url(response.url, 1),
                                   callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'origin_name': origin_name, 'title': title,
                                         'content': content_div.extract(), 'page_num': 1, 'total': total,
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')})
        content, media, *_ = self.content_clean(content_div)
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_page(self, response):
        meta_new = deepcopy(response.meta)
        xp = response.xpath
        try:
            content_div = xp(r'//div[@class="TRS_Editor"]')[0]
        except BaseException:
            return self.produce_debugitem(response, 'xpath error')

        meta_new['content'] += content_div.extract()
        meta_new['page_num'] += 1
        if meta_new['total'] > meta_new['page_num']:  # 总页数>当前页
            next_url = self._next_url(
                meta_new['first_url'], meta_new['page_num'])
            return response.follow(
                next_url, callback=self.parse_page, meta=meta_new)

        content, media, *_ = self.content_clean(meta_new['content'])

        return self.produce_item(
            response=response,
            title=meta_new['title'],
            pubtime=meta_new['pubtime'],
            origin_name=meta_new['origin_name'],
            content=content,
            media=media
        )

    @staticmethod
    def _next_url(url, idx, tail='', sufx=''):
        """
        比如第2页的下一页url是 http://military.cnr.cn/jstp/jstph/20190409/t20190409_524571960_2.html
        :param url:         当前页的url
        :param idx:    int   第几页>0
        :return:             构造第idx页的下一页的url
        """
        if not tail or not sufx:
            url_parse = urlsplit(url)
            tail, sufx = os.path.basename(url_parse.path).split('.')
        return urljoin(url, tail + '_%s.' % idx + sufx)


class CnrHomePageSpider(CnrSpider):
    name = 'cnr_home'
    mystart_urls = {
        'http://news.cnr.cn/': 192,  # '新闻',
    }
    rules = (
        # http://sports.cnr.cn/news/20190412/t20190412_524575260.shtml
        Rule(LinkExtractor(
            allow=(
                r'(?:news|china|sports)\.cnr\.cn/.*?/%s\d{2}/t\d+_\d+\.s?html' %
                datetime.today().strftime('%Y%m'),),
            deny=(r'military\.cnr\.cn', r'\.cnr\.cn/native/city/', 'cnr_404', r'tv.cnr.cn/')),
             callback='parse_item', follow=False),
    )
    custom_settings = {
        "SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % CnrSpider.name,
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
    }
