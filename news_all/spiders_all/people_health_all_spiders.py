# -*- coding: utf-8 -*-
# @Time   : 2019/3/1 下午5:59
# @Author : NewmanZhou
# @Project : news_all
# @FileName: people_gdyw_spider.py
# @Software: PyCharm

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from copy import deepcopy
from news_all.spider_models import otherurl_meta
from news_all.spiders.people import PeopleSpider
import re


# 广度采集人民健康网
class PeopleHealthSpipder(PeopleSpider):
    name = 'people_health_spider'
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update({'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % PeopleSpider.name,})
    # 人民健康网
    mystart_urls = {  # 5月13日数据库中删除了source_id:3220,3221,3222,3224,3226,3227,3228,3229,3230,3231,3232,3235,3238, 另外想删3233, 3234, 3236, 3237没查到
        'http://health.people.com.cn/GB/413642/index.html': 3201,  # 金台养生园--人民健康网--人民网
        'http://health.people.com.cn/GB/408577/index.html': 3202,  # 两性--人民健康网--人民网
        'http://health.people.com.cn/GB/408576/index.html': 3203,  # 心理--人民健康网--人民网
        'http://health.people.com.cn/GB/413644/index.html': 3204,  # “健”识早知道--人民健康网--人民网
        'http://health.people.com.cn/GB/408580/index.html': 3205,  # 慢病预防--人民健康网--人民网
        'http://health.people.com.cn/GB/408578/index.html': 3206,  # 家居--人民健康网--人民网
        'http://health.people.com.cn/GB/408626/index.html': 3207,  # 疾病--人民健康网--人民网
        'http://health.people.com.cn/GB/408573/index.html': 3208,  # 母婴--人民健康网--人民网
        'http://health.people.com.cn/GB/405407/index.html': 3209,  # 中医中药--人民健康网--人民网
        'http://health.people.com.cn/GB/408569/index.html': 3210,  # 食品--人民健康网--人民网
        'http://health.people.com.cn/GB/408647/': 3211,  # 原创稿件--人民健康网--人民网
        'http://health.people.com.cn/GB/408644/index.html': 3212,  # 健康315--人民健康网--人民网
        'http://health.people.com.cn/GB/408568/index.html': 3217,  # 观察评论--人民健康网--人民网
        'http://health.people.com.cn/GB/26466/401878/404200/404225/index.html': 3223,  # 全民营养课--人民健康网--人民网
        'http://health.people.com.cn/GB/420015/420328/index.html': 3225,  # 权威发布--人民健康网--人民网
        'http://health.people.com.cn/GB/420015/420158/index.html': 3239,  # 曝光台--人民健康网--人民网
    }

    # http://health.people.com.cn/n1/2019/0301/c14739-30953006.html
    rules = (Rule(LinkExtractor(allow=r'health.people.com.cn/.*?/%s\d{2}/c\d+-\d+.html'% datetime.today().strftime('%Y/%m'), deny=('video', 'audio'),
                                ),
                  callback='parse_item', follow=False),
             Rule(LinkExtractor(allow=r'people.com.cn/.*?\d+\.html',
                                deny=r'/201[0-8]', ), process_request=otherurl_meta,
                  follow=False),
             )
    custom_settings = {
        'SCHEDULER_DUPEFILTER_KEY': '%s:dupefilter' % PeopleSpider.name,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
   
    def parse_item(self, response):
        xp = response.xpath
        try:
            pubtimeStr = xp('//div[@class="artOri"]').extract()[0]
            pubtime = re.findall(r'\d{2,4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{1,2}', pubtimeStr)[0]
            cv = xp('//div[@class="articleCont"]/div[@class="artDet"]')[0]
            content, media, video, cover = self.content_clean(cv, need_video=True)
            title = xp('//div[@class="title"]/h2/text()').extract()[0]
            origin_name = xp('//div[@class="artOri"]/a/text()').extract()[0]
        except:
            return super(PeopleHealthSpipder, self).parse_item(response)

        return self.produce_item(
            response=response,  # must
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )