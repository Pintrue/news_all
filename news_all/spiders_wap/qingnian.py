# -*- coding: utf-8 -*-

from scrapy import Request
from news_all.spider_models import NewsRSpider
import re


class qingnianSpider(NewsRSpider):
    """中国青年 app"""
    name = 'qingnian_app'
    mystart_urls = {  # todo 用PyExecJS解析。只有http://m.youth.cn/是实际dom 其他都是js dataList.push
        'http://m.youth.cn/': 2926,  # APP端-中央媒体移动端-中国青年-要闻
        'http://m.youth.cn/gqt/': 2927,  # APP端-中央媒体移动端-中国青年-共青团
        'http://m.youth.cn/p/': 2928,  # APP端-中央媒体移动端-中国青年-图片
        'http://m.youth.cn/pl/': 2929,  # APP端-中央媒体移动端-中国青年-评论
        'http://m.youth.cn/f/': 2930,  # APP端-中央媒体移动端-中国青年-娱乐
        'http://m.youth.cn/s/': 2931,  # APP端-中央媒体移动端-中国青年-社会
        'http://m.youth.cn/jy/': 2932,  # APP端-中央媒体移动端-中国青年-教育
        'http://m.youth.cn/ydsp/': 2933,  # APP端-中央媒体移动端-中国青年-短视频
        'http://m.youth.cn/dfyw/': 2934,  # APP端-中央媒体移动端-中国青年-地方
    }
    custom_settings = {
        'DEPTH_LIMIT': 5,  # 翻页需要设置深度为0 或者 >1
    }
    
    def parse(self, response):
        if response.url == 'http://m.youth.cn/ydsp/':
            return self.parse_video(response)
        
        con = response.xpath('//ul[@class="thumb"]/li[@class="thumb-item"]').extract()
        if con == []:
            return self.parse_3(response)
        
        for i in response.xpath('//ul[@class="thumb"]/li[@class="thumb-item"]').extract():
            news_url = re.search('a href="(.*?)" target="_blank">', i).group(1)
            news_url = 'https://t.m.youth.cn/transfer/index/url/' + news_url
            title = re.search('a.*?>(.*?)</a>', i).group(1)
            origin_name = re.search('<span class="keyword">(.*?)</span>', i).group(1)
            print(news_url)
            yield Request(
                url=news_url,
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time'), 'origin_name': origin_name})
    
    def parse_3(self, response):  # http://m.youth.cn/gqt/
        con = re.findall('dataList\.push\((.*?})', response.text)
        for i in con:
            i = eval(i)
            news_url = i['link']
            if response.url != 'http://m.youth.cn/p/':
                news_url = 'https://t.m.youth.cn/transfer/index/url/' + news_url
            title = i['title']
            origin_name = i['source']
            callback = self.parse_item
            if response.url == 'http://m.youth.cn/p/':
                callback = self.parse_image
                news_url = 'https://t.m.youth.cn/transfer/index/url/' + news_url  # 重新生成url方便访问客户端，统一解析
                print(news_url)
            try:
                yield Request(
                    url=news_url,
                    callback=callback,
                    meta={'source_id': response.meta['source_id'], 'title': title,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time'),
                          'origin_name': origin_name})
            except:
                yield Request(
                    url='http:' + news_url,
                    callback=callback,
                    meta={'source_id': response.meta['source_id'], 'title': title,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time'),
                          'origin_name': origin_name})
    
    def parse_image(self, response):
        try:
            rs = response.xpath('//div[@class="content1"]').extract()
            title = response.xpath('//h1[@id="title"]/text()')[0].extract()
            pubtime = response.xpath('//span[@id="pubtime"]/text()')[0].extract().replace(' ', '')
              # 时效性检查
                
            origin_name = response.xpath('//span[@id="source"]/text()')[0].extract()
            content, media, _, _ = self.content_clean(rs, kill_xpaths=['//ul[@class="page_ggw mt15"]',
                                                                       '//ul[@class="page_pic"]'])

        except:
            return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )
    
    def parse_video(self, response):  # http://m.youth.cn/ydsp/,短视频没有新闻内容，只有视频
        video = response.xpath('//div[@class="video_youth"]')
        for i in video:
            try:
                title = i.xpath('./h3/text()')[0].extract()
                video_url = i.xpath('./div[@class="video_k"]//source/@src')[0].extract()
                pubtime = i.xpath('./div[@class="laiyuan"]/span[2]/text()')[0].extract()
                videos = {'1': {'src': video_url}}
                content = '<div>#{{1}}#</div>'
            except:
                return self.produce_debugitem(response, "xpath error")
            yield self.produce_item(
                response=response,
                title=title,
                pubtime=pubtime,
                content=content,
                videos=videos
            )
    
    def parse_item(self, response):
        try:
            rs = response.xpath('//div[@class="content1"]').extract()
            title = response.xpath('//h1[@id="title"]/text()')[0].extract()
            pubtime = response.xpath('//span[@id="pubtime"]/text()')[0].extract().replace(' ', '')
            origin_name = response.xpath('//span[@id="source"]/text()')[0].extract()
            content, media, _, _ = self.content_clean(rs, kill_xpaths=['//ul[@class="page_ggw mt15"]',
                                                                       '//ul[@class="page_pic"]'])
        except:
            return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )
