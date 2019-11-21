# -*- coding: utf-8 -*-
# @Time   : 2019/7/25 上午10:05
# @Author : NewmanZhou
# @Project : news_all
# @Software: PyCharm
from copy import deepcopy
from datetime import datetime

from scrapy.conf import settings
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.spider_models import otherurl_meta
from news_all.spider_models import NewsRCSpider


class LNDSpider(NewsRCSpider):
    # 北国网 网页端
    name = 'lnd_web'
    mystart_urls = {
                       'http://www.lnd.com.cn': 4052,  # 网站-地方网站-北国网
                       'http://news.lnd.com.cn': 4053,  # 网站-地方网站-北国网-新闻-首页
                       'http://news.lnd.com.cn/sz/index.shtml': 4054,  # 网站-地方网站-北国网-新闻-时政
                       'http://news.lnd.com.cn/xwyw/index.shtml': 4055,  # 网站-地方网站-北国网-新闻-新闻要闻
                       'http://news.lnd.com.cn/gn/index.shtml': 4056,  # 网站-地方网站-北国网-新闻-国内
                       'http://news.lnd.com.cn/gj/index.shtml': 4057,  # 网站-地方网站-北国网-新闻-国际
                       'http://news.lnd.com.cn/wt/index.shtml': 4058,  # 网站-地方网站-北国网-新闻-文体
                       'http://news.lnd.com.cn/cj/index.shtml': 4059,  # 网站-地方网站-北国网-新闻-财经
                       'http://news.lnd.com.cn/ktx/index.shtml': 4060,  # 网站-地方网站-北国网-新闻-看天下
                       'http://news.lnd.com.cn/pl/index.shtml': 4061,  # 网站-地方网站-北国网-新闻-评论
                       'http://liaoning.lnd.com.cn': 4062,  # 网站-地方网站-北国网-地方新闻-首页
                       'http://liaoning.lnd.com.cn/jrln/index.shtml': 4063,  # 网站-地方网站-北国网-地方新闻-今日辽宁
                       'http://liaoning.lnd.com.cn/zydt/index.shtml': 4064,  # 网站-地方网站-北国网-地方新闻-重要动态
                       'http://liaoning.lnd.com.cn/szyw/index.shtml': 4065,  # 网站-地方网站-北国网-地方新闻-时政要闻
                       'http://liaoning.lnd.com.cn/msrd/index.shtml': 4066,  # 网站-地方网站-北国网-地方新闻-民生热点
                       'http://liaoning.lnd.com.cn/shxw/index.shtml': 4067,  # 网站-地方网站-北国网-地方新闻-社会新闻
                       'http://liaoning.lnd.com.cn/qsgd/index.shtml': 4068,  # 网站-地方网站-北国网-地方新闻-全省各地
                       'http://travel.lnd.com.cn': 4069,  # 网站-地方网站-北国网-旅游-首页
                       'http://travel.lnd.com.cn/mlln/index.shtml': 4070,  # 网站-地方网站-北国网-旅游-美丽辽宁
                       'http://travel.lnd.com.cn/wlyw/index.shtml': 4071,  # 网站-地方网站-北国网-旅游-文旅要闻
                       'http://travel.lnd.com.cn/djtj/index.shtml': 4072,  # 网站-地方网站-北国网-旅游-当季推荐
                       'http://travel.lnd.com.cn/lydt/index.shtml': 4073,  # 网站-地方网站-北国网-旅游-旅游目的地
                       'http://travel.lnd.com.cn/yxln/index.shtml': 4074,  # 网站-地方网站-北国网-旅游-影像辽宁
                       'http://travel.lnd.com.cn/yjgl/index.shtml': 4075,  # 网站-地方网站-北国网-旅游-旅游攻略
                       'http://travel.lnd.com.cn/qjln/index.shtml': 4076,  # 网站-地方网站-北国网-旅游-全景辽宁
                       'http://comment.lnd.com.cn': 4077,  # 网站-地方网站-北国网-评论-首页
                       'http://comment.lnd.com.cn/dtcp/index.shtml': 4078,  # 网站-地方网站-北国网-评论-动态潮评
                       'http://comment.lnd.com.cn/lbsp/index.shtml': 4079,  # 网站-地方网站-北国网-评论-辽宁时评
                       'http://comment.lnd.com.cn/llsd/index.shtml': 4080,  # 网站-地方网站-北国网-评论-理论视点
                       'http://comment.lnd.com.cn/wsp/index.shtml': 4081,  # 网站-地方网站-北国网-评论-微视频
                       'http://edu.lnd.com.cn': 4082,  # 网站-地方网站-北国网-教育-首页
                       'http://edu.lnd.com.cn/rdzx/index.shtml': 4083,  # 网站-地方网站-北国网-教育-热点资讯
                       'http://xjzt.lnd.com.cn/index.shtml': 4084,  # 网站-地方网站-北国网-教育-小记者园地
                       'http://edu.lnd.com.cn/ztzgk/index.shtml': 4085,  # 网站-地方网站-北国网-教育-直通中高考
                       'http://edu.lnd.com.cn/zkjxs/index.shtml': 4086,  # 网站-地方网站-北国网-教育-考试进行时
                       'http://edu.lnd.com.cn/zypx/index.shtml': 4087,  # 网站-地方网站-北国网-教育-培训教育
                       'http://edu.lnd.com.cn/lxym/index.shtml': 4088,  # 网站-地方网站-北国网-教育-留学移民
                       'http://edu.lnd.com.cn/jtjy/index.shtml': 4089,  # 网站-地方网站-北国网-教育-家庭教育
                       'http://ent.lnd.com.cn': 4090,  # 网站-地方网站-北国网-娱乐-首页
                       'http://ent.lnd.com.cn/yyzx/index.shtml': 4091,  # 网站-地方网站-北国网-娱乐-音乐
                       'http://ent.lnd.com.cn/yskx/index.shtml': 4092,  # 网站-地方网站-北国网-娱乐-影视
                       'http://ent.lnd.com.cn/mxbg/index.shtml': 4093,  # 网站-地方网站-北国网-娱乐-明星八卦
                       'http://ent.lnd.com.cn/xjzt/index.shtml': 4094,  # 网站-地方网站-北国网-娱乐-戏剧杂谈
                       'http://ent.lnd.com.cn/jctp/index.shtml': 4095,  # 网站-地方网站-北国网-娱乐-图片新闻
                       'http://video.lnd.com.cn': 4096,  # 网站-地方网站-北国网-视频-首页
                       'http://video.lnd.com.cn/node_75003.htm': 4097,  # 网站-地方网站-北国网-视频-辽沈播报
                       'http://video.lnd.com.cn/node_75041.htm': 4098,  # 网站-地方网站-北国网-视频-体育要闻
                       'http://video.lnd.com.cn/node_75063.htm': 4099,  # 网站-地方网站-北国网-视频-娱乐八卦
                       'http://news.lnd.com.cn/fx/index.shtml': 4100,  # 网站-地方网站-北国网-新闻-发现
                       'http://fashion.lnd.com.cn': 4101,  # 网站-地方网站-北国网-时尚-首页
                       'http://fashion.lnd.com.cn/beauty/index.shtml': 4102,  # 网站-地方网站-北国网-时尚-BEAUTY
                       'http://fashion.lnd.com.cn/sy/index.shtml': 4103,  # 网站-地方网站-北国网-时尚-试用
                       'http://fashion.lnd.com.cn/szj/index.shtml': 4104,  # 网站-地方网站-北国网-时尚-时装精
                       'http://fashion.lnd.com.cn/zbwb/index.shtml': 4105,  # 网站-地方网站-北国网-时尚-珠宝腕表
                       'http://fashion.lnd.com.cn/qg/index.shtml': 4106,  # 网站-地方网站-北国网-时尚-情感
                       'http://fashion.lnd.com.cn/xz/index.shtml': 4107,  # 网站-地方网站-北国网-时尚-星座
                       'http://fashion.lnd.com.cn/HOTzxb/index.shtml': 4108,  # 网站-地方网站-北国网-时尚-资讯
                       'http://news.lnd.com.cn/wh/index.shtml': 4109,  # 网站-地方网站-北国网-新闻-文化
                       'http://health.lnd.cn': 4110,  # 网站-地方网站-北国网-健康-首页
                       'http://health.lnd.com.cn/node_59089.htm': 4111,  # 网站-地方网站-北国网-健康-男性
                       'http://health.lnd.com.cn/node_59090.htm': 4112,  # 网站-地方网站-北国网-健康-女性
                       'http://health.lnd.com.cn/node_59091.htm': 4113,  # 网站-地方网站-北国网-健康-性爱
                       'http://health.lnd.com.cn/node_59092.htm': 4114,  # 网站-地方网站-北国网-健康-心理
                       'http://health.lnd.com.cn/node_59093.htm': 4115,  # 网站-地方网站-北国网-健康-老人
                       'http://health.lnd.com.cn/node_59094.htm': 4116,  # 网站-地方网站-北国网-健康-育儿
                       'http://health.lnd.com.cn/node_59095.htm': 4117,  # 网站-地方网站-北国网-健康-美容
                       'http://health.lnd.com.cn/node_59096.htm': 4118,  # 网站-地方网站-北国网-健康-整形
                       'http://health.lnd.com.cn/node_59097.htm': 4119,  # 网站-地方网站-北国网-健康-美体
                       'http://health.lnd.com.cn/node_59098.htm': 4120,  # 网站-地方网站-北国网-健康-瑜伽
                       'http://health.lnd.com.cn/node_59099.htm': 4121,  # 网站-地方网站-北国网-健康-中医
                       'http://health.lnd.com.cn/node_59121.htm': 4122,  # 网站-地方网站-北国网-健康-养生
                       'http://news.lnd.com.cn/dc/index.shtml': 4123,  # 网站-地方网站-北国网-新闻-调查
                       'http://news.lnd.com.cn/ll/index.shtml': 4124,  # 网站-地方网站-北国网-新闻-理论
                       'http://read.lnd.com.cn': 4125,  # 网站-地方网站-北国网-读书-首页
    'http://lnny.lnd.com.cn': 4126,  # 网站-地方网站-北国网-农业-首页
    'http://lnny.lnd.com.cn/node_51282.htm': 4127,  # 网站-地方网站-北国网-农业-政策
    'http://auto.lnd.com.cn': 4128,  # 网站-地方网站-北国网-汽车
    'http://auto.lnd.com.cn/news/dujia/?spm=zm1021-001.0.0.1.YRTkpF': 4129,  # 网站-地方网站-北国网-汽车-最新
    'http://auto.lnd.com.cn/news/letters/?spm=zm1021-001.0.0.1.YRTkpF': 4130,  # 网站-地方网站-北国网-汽车-快报
    'http://auto.lnd.com.cn/news/xinche/?spm=zm1021-001.0.0.1.YRTkpF': 4131,  # 网站-地方网站-北国网-汽车-新车
    'http://auto.lnd.com.cn/news/pingce/?spm=zm1021-001.0.0.1.6IMIVI': 4132,  # 网站-地方网站-北国网-汽车-测评
    'http://auto.lnd.com.cn/news/43/1/?spm=zm1021-001.0.0.1.YRTkpF': 4133,  # 网站-地方网站-北国网-汽车-国产车测试
    'http://auto.lnd.com.cn/news/46/1/?spm=zm1021-001.0.0.2.4CfXCt': 4134,  # 网站-地方网站-北国网-汽车-进口车测试

    }

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    # 防止跳转'<meta http-equiv="refresh" content="0; url=https://live.xinhuaapp.com/xcy/reportlist.html?liveId=156687303133411" />
    custom_settings['DOWNLOADER_MIDDLEWARES']['scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware'] = None

    # LimitatedDaysHoursMinutes = 10
    # http://edu.lnd.com.cn/system/2019/08/28/030047433.shtml
    # http://news.lnd.com.cn/system/2019/09/02/030047699.shtml

    rules = (
        Rule(LinkExtractor(allow=(r'lnd.com.cn/system/%s/\d{2}/\d+\.s?htm' % datetime.today().strftime('%Y/%m')),
                           ), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'lnd.com.cn.*?\.s?htm'),
                           deny=(r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/', r'/index.s?htm')),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        if xp('//meta[@http-equiv="refresh" and starts-with(@content,"0;")]'):
            return self.produce_debugitem(response, '网页跳转')
        try:
            origin_name = xp('//div[@class="float_left"]/span[3]/a/text()').extract_first()
            title = xp('//p[@class="yahei newstittle"]/text()').extract_first()
            pubtime = xp('//div[@class="float_left"]/span[@id="pubtime_baidu"]/text()').extract_first()

            content_div = xp('//div[@class="news"]').extract()
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item1(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )

    def parse_item1(self, response):
        xp = response.xpath
        try:
            origin_name = xp('//div[@class="w1000 imfor"]/div/span[3]/a/text()').extract_first()
            title = xp('//div[@class="w1000 imfor"]/div/p/text()').extract_first()
            pubtime = xp('//div[@class="w1000 imfor"]/div/span[2]/text()').extract_first()
            content_div = xp('//div[@class="yahei "]').extract()
            content, media, _, _ = self.content_clean(content_div)
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
