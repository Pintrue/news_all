# -*- coding: utf-8 -*-
import re
from datetime import datetime
from urllib.parse import urlsplit, urljoin
import os
from scrapy.conf import settings
from copy import deepcopy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.spider_models import NewsRCSpider, otherurl_meta


class WorkercnSpider(NewsRCSpider):
    """中工网"""
    name = 'workercn'

    mystart_urls = {
        'http://news.workercn.cn/': 199,  # '新闻',
        'http://finance.workercn.cn/': 203,  # '财经',
        'http://world.workercn.cn/': 204,  # '国际',
        'http://job.workercn.cn/': 205,  # '创业·就业',
        # 'http://news.workercn.cn/32846/32846.shtml': 0,  # '测试图集'

        # 来自spiders_all
        'http://ent.workercn.cn/30021/30021.shtml': 5078,
        'http://ent.workercn.cn/30031/30031.shtml': 5079,
        'http://hb.workercn.cn/32699/32699.shtml': 5122,
        'http://news.workercn.cn//32847/32847.shtml': 5136,
        'http://news.workercn.cn/32839/32839.shtml': 5160,
        'http://finance.workercn.cn/33012/33012.shtml': 5162,

        'http://sports.workercn.cn/32785/32785.shtml': 5200,
        'http://sports.workercn.cn/32784/32784.shtml': 5201,
        'http://sports.workercn.cn/32782/32782.shtml': 5202,
        'http://sports.workercn.cn/32781/32781.shtml': 5203,
        'http://sports.workercn.cn/32780/32780.shtml': 5204,
        'http://sports.workercn.cn/32778/32778.shtml': 5205,
        'http://sports.workercn.cn/32776/32776.shtml': 5206,
        'http://sports.workercn.cn/32775/32775.shtml': 5207,
        'http://sports.workercn.cn/32786/32786.shtml': 5246,

        'http://tour.workercn.cn/32883/32883.shtml': 5208,
        'http://www.workercn.cn/28261/28261.shtml': 5242,
        'http://blog.workercn.cn/home.php?mod=index': 5245,

        'http://cq.workercn.cn/32075/32075.shtml': 5270,
        'http://cq.workercn.cn/32065/32065.shtml': 5272,
        'http://ah.workercn.cn/32548/32548.shtml': 5291,
        'http://ah.workercn.cn/32543/32543.shtml': 5292,
        'http://auto.workercn.cn/28441/28441.shtml': 5320,
        'http://auto.workercn.cn/28429/28429.shtml': 5264,
    }

    # http://news.workercn.cn/32841/201901/18/190118124637372.shtml
    # http://job.workercn.cn/312/201902/01/190201135234776.shtml
    rules = (
            Rule(LinkExtractor(allow=(r'workercn.cn/\d+/%s/\d{2}/\d{10,}\.s?html' % datetime.today().strftime('%Y%m'),)),
                  callback='parse_item', follow=False),
             Rule(LinkExtractor(allow=(r'workercn.cn.*?\d{10,}\.s?html',), deny=(r'/201[0-8]', r'/20190[1-9]/')),
                  process_request=otherurl_meta, follow=False),
             )
 
    custom_settings = {
        'DEPTH_LIMIT': 0,
        # 禁止重定向
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))}

    time_pat = re.compile(r'\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}')
        
    def parse_item(self, response):
        if '博客通讯' in self.get_page_title(response):
            return self.produce_debugitem(response, '博客通讯 not news')
        xp = response.xpath
        try:
            content_div = xp('//div[@class="ccontent"]')[0]  # 特别注意: 加. 导致选择了全部网页 todo review其他spider code
            source_div = xp('//div[@class="signdate"]')[0]
            origin = xp('//div[@class="from"]/span/text()').extract() or source_div.xpath('./span[2]/text()').extract()
            origin_name = origin[0].strip()
            # tail_div = xp('//div[@class="editor"')[0]
            # pubtime = source_div.xpath('.//text()').extract_first('').strip()
            pubtime = self.time_pat.findall(source_div.extract())[0]
        except:
            return self.parse_item_2(response)

        title = self.get_page_title(response).split('-')[0]
        total_page = content_div.xpath('.//div/p/input[@name="__totalpage"]/@value').extract_first()

        if total_page:
            total = int(total_page)
            if total > 1:
                url = self._next_url(response.url, 2)
                return response.follow(url, callback=self.parse_page,
                                       meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                             'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                             'content': content_div.extract(), 'page_num': 2,
                                             'start_url_time': response.meta.get('start_url_time'),
                                             'schedule_time': response.meta.get('schedule_time')
                                             })
        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_2(self, response):
        # http://auto.workercn.cn/28441/201904/19/190419171717318.shtml
        xp = response.xpath
        try:
            pubtime = xp('//div[@class="from mt10"]/span[@class="font-black1-12"]/text()')[0].extract()
            cv = xp('//div[@class="article"]')[0]
            content_div = cv.xpath('./p')
            origin_name = xp('//div[@class="from mt10"]/span[@class="font-black_12"]/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.parse_item_3(response)

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('-')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item_3(self, response):
        # http://cq.workercn.cn/32065/201904/16/190416082736996.shtml
        xp = response.xpath
        try:
            pubtime = xp('//span[@class="font-black1_12"][1]/text()').extract_first()
            content_div = xp('//div[@class="detail_con"]/div[@class="font-black_16 hangao"]')[0]
            origin_name = xp('//span[@class="font-black1_12"][2]/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

        title = self.get_page_title(response).split('-')[0]
        total_page = content_div.xpath('.//div/p/input[@name="__totalpage"]/@value').extract_first()

        if total_page:
            total = int(total_page)
            if total > 1:
                url = self._next_url(response.url, 2)
                return response.follow(url, callback=self.parse_page,
                                       meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                             'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                             'content': content_div.extract(), 'page_num': 2,
                                             'start_url_time': response.meta.get('start_url_time'),
                                             'schedule_time': response.meta.get('schedule_time')
                                             })
            
        content, media, videos, video_cover = self.content_clean(content_div)

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
            cvs = xp('//div[@class="ccontent"]') or xp('//div[@class="detail_con"]/div[@class="font-black_16 hangao"]')
            content_div = cvs[0]
        except:
            return self.produce_debugitem(response, 'xpath error')

        meta_new['content'] += content_div.extract()

        turn_div = content_div.xpath('.//div/p/input[@name="__totalpage"]/parent::p/following-sibling::center')
        meta_new['page_num'] += 1
        next_a = turn_div.xpath('.//a[text()="%s"]' % meta_new['page_num'])
        if next_a:
            # next_a 是js
            next_url = self._next_url(meta_new['first_url'], meta_new['page_num'])
            return response.follow(next_url, callback=self.parse_page, meta=meta_new)

        # http://news.workercn.cn/32847/201903/13/190313131127880.shtml
        # 广告图片
        content, media, videos, video_cover = self.content_clean(meta_new['content'],
                                                                 kill_xpaths=[
                                                                     './/div/p/input[@name="__totalpage"]/parent::p/parent::div',
                                                                     './/img[contains(@src|@href,"U194P4T47D44005F978DT20190304082423.jpg")]'])

        return self.produce_item(
            response=response,
            title=meta_new['title'],
            pubtime=meta_new['pubtime'],
            origin_name=meta_new['origin_name'],
            content=content,
            media=media,
            srcLink=meta_new['first_url']
        )

    @staticmethod
    def _next_url(url, idx, tail='', sufx=''):
        """
        http://world.workercn.cn/32836/201903/14/190314070852665_2.shtml
        http://world.workercn.cn/32836/201903/14/190314070852665_3.shtml
        :param url:         当前页的url
        :param idx:   int   第几页>1
        :return:             下一页的url
        """
        if not tail or not sufx:
            url_parse = urlsplit(url)
            tail, sufx = os.path.basename(url_parse.path).split('.')
        return urljoin(url, tail + '_%s.' % idx + sufx)