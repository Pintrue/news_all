#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/3 10:08
# @Author  : mez
# @File    : gscn.py
from copy import deepcopy
from datetime import datetime

from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from news_all.tools.time_translater import Pubtime


class GscnSpider(NewsRCSpider):
    """中国甘肃网"""
    name = 'gscn'
    mystart_urls = {
        'http://lyys.gscn.com.cn/yscs/index.shtml': 4901,  # 网站-地方网站-中国甘肃网-养生-养生杂谈
        'http://lyys.gscn.com.cn/lymy/index.shtml': 4902,  # 网站-地方网站-中国甘肃网-养生-养生名人名医
        'http://lyys.gscn.com.cn/mqmy/index.shtml': 4903,  # 网站-地方网站-中国甘肃网-养生-养生医馆
        'http://www.gscn.com.cn/food/': 4904,  # 网站-地方网站-中国甘肃网-美食
        'http://www.gscn.com.cn/food/msys/index.shtml': 4905,  # 网站-地方网站-中国甘肃网-美食-美食养生
        'http://www.gscn.com.cn/food/lsfw/index.shtml': 4906,  # 网站-地方网站-中国甘肃网-美食-陇上味道
        'http://www.gscn.com.cn/food/mswh/index.shtml': 4907,  # 网站-地方网站-中国甘肃网-美食-美食文化
        'http://www.gscn.com.cn/food/lsms/index.html': 4908,  # 网站-地方网站-中国甘肃网-美食-陇上特产
        'http://theory.gscn.com.cn': 4909,  # 网站-地方网站-中国甘肃网-理论
        'http://theory.gscn.com.cn/xxls/index.shtml': 4913,  # 网站-地方网站-中国甘肃网-理论-学习路上
        'http://theory.gscn.com.cn/dsdj/index.shtml': 4914,  # 网站-地方网站-中国甘肃网-理论-党建政治
        'http://theory.gscn.com.cn/lldt/index.shtml': 4916,  # 网站-地方网站-中国甘肃网-理论-理论动态
        'http://theory.gscn.com.cn/llqy/index.shtml': 4918,  # 网站-地方网站-中国甘肃网-理论-理论前沿
        'http://theory.gscn.com.cn/gspl/index.shtml': 4921,  # 网站-地方网站-中国甘肃网-理论-评论甘肃
        'http://theory.gscn.com.cn/zxrp/index.shtml': 4936,  # 网站-地方网站-中国甘肃网-理论-最新热评
        'http://www.gscn.com.cn/ent/': 4938,  # 网站-地方网站-中国甘肃网-娱乐
        'http://www.gscn.com.cn/ent/ys/index.shtml': 4939,  # 网站-地方网站-中国甘肃网-娱乐-影视
        'http://www.gscn.com.cn/ent/mx/index.shtml': 4940,  # 网站-地方网站-中国甘肃网-娱乐-明星
        'http://www.gscn.com.cn/ent/ss/index.shtml': 4941,  # 网站-地方网站-中国甘肃网-娱乐-时尚资讯
        'http://www.gscn.com.cn/ent/yy/index.shtml': 4942,  # 网站-地方网站-中国甘肃网-娱乐-音乐
        'http://www.gscn.com.cn/province/jjsh/index.html': 4954,  # 网站-地方网站-中国甘肃网-省情-经济社会发展
        'http://www.gscn.com.cn/province/sczl/': 4955,  # 网站-地方网站-中国甘肃网-省情-丝绸之路
        'http://www.gscn.com.cn/province/hh/': 4960,  # 网站-地方网站-中国甘肃网-省情-黄河
        'http://www.gscn.com.cn/province/fx/': 4966,  # 网站-地方网站-中国甘肃网-省情-伏羲
        'http://www.gscn.com.cn/province/jjsh/szgs/': 4968,  # 网站-地方网站-中国甘肃网-省情-数字甘肃
        'http://www.gscn.com.cn/province/jjsh/hgjj/': 4975,  # 网站-地方网站-中国甘肃网-省情-宏观经济
        'http://www.gscn.com.cn/province/jjsh/hmfm/': 4981,  # 网站-地方网站-中国甘肃网-省情-惠民富民
        'http://www.gscn.com.cn/province/jjsh/shsy/': 4987,  # 网站-地方网站-中国甘肃网-省情-社会事业
        'http://www.gscn.com.cn/province/jjsh/dwkf/': 4988,  # 网站-地方网站-中国甘肃网-省情-对外开放
        'http://dili.gscn.com.cn': 4991,  # 网站-地方网站-中国甘肃网-地理
        'http://www.gscn.com.cn/geography/gstx/': 4998,  # 网站-地方网站-中国甘肃网-地理-甘肃探索
        'http://www.gscn.com.cn/geography/xghl/': 5001,  # 网站-地方网站-中国甘肃网-地理-峡谷河流
        'http://www.gscn.com.cn/geography/dlzx/': 5003,  # 网站-地方网站-中国甘肃网-地理-地理资讯
        'http://www.gscn.com.cn/geography/tsdm/': 5006,  # 网站-地方网站-中国甘肃网-地理-特殊地貌
        'http://www.gscn.com.cn/geography/spzq/': 5009,  # 网站-地方网站-中国甘肃网-地理-视频专区
        'http://www.gscn.com.cn/geography/sydz/': 5011,  # 网站-地方网站-中国甘肃网-地理-山岳地质
        'http://www.gscn.com.cn/geography/cxlx/': 5014,  # 网站-地方网站-中国甘肃网-地理-出行路线
        'http://www.gscn.com.cn/geography/hwbd/': 5017,  # 网站-地方网站-中国甘肃网-地理-户外宝典
        'http://www.gscn.com.cn/geography/hwsc/': 5019,  # 网站-地方网站-中国甘肃网-地理-户外商城
        'http://www.gscn.com.cn/geography/': 5021,  # 网站-地方网站-中国甘肃网-地理-野外家园
        'http://www.gscn.com.cn/geography/dlrw/': 5023,  # 网站-地方网站-中国甘肃网-地理-地理人物
        'http://www.gscn.com.cn/geography/gskg/': 5025,  # 网站-地方网站-中国甘肃网-地理-甘肃考古
        'http://www.gscn.com.cn/geography/qh/': 5027,  # 网站-地方网站-中国甘肃网-地理-气候土壤
        'http://www.gscn.com.cn/geography/msfq/': 5029,  # 网站-地方网站-中国甘肃网-地理-民俗风情
        'http://www.gscn.com.cn/science/': 5030,  # 网站-地方网站-中国甘肃网-科教
        'http://yqpd.gscn.com.cn/index.shtml': 5031,  # 网站-地方网站-中国甘肃网-舆情
        'http://yqpd.gscn.com.cn/yqjj/': 5034,  # 网站-地方网站-中国甘肃网-舆情-舆情聚焦
        'http://yqpd.gscn.com.cn/yqgc/': 5036,  # 网站-地方网站-中国甘肃网-舆情-舆情观察
        'http://yqpd.gscn.com.cn/gsyq/': 5038,  # 网站-地方网站-中国甘肃网-舆情-甘肃舆情
        'http://yqpd.gscn.com.cn/szyq/': 5040,  # 网站-地方网站-中国甘肃网-舆情-市州舆情
        'http://yqpd.gscn.com.cn/zwyq/': 5042,  # 网站-地方网站-中国甘肃网-舆情-政务舆情
        'http://yqpd.gscn.com.cn/qyyq/': 5045,  # 网站-地方网站-中国甘肃网-舆情-企业舆情
        'http://yqpd.gscn.com.cn/jdyp/': 5047,  # 网站-地方网站-中国甘肃网-舆情-焦点舆评
        'http://dxs.gscn.com.cn': 5050,  # 网站-地方网站-中国甘肃网-大学生
        'http://dxs.gscn.com.cn/ywsm/': 5053,  # 网站-地方网站-中国甘肃网-大学生-即时要闻
        'http://dxs.gscn.com.cn/lt/': 5056,  # 网站-地方网站-中国甘肃网-大学生-大学论坛
        'http://dxs.gscn.com.cn/ksdq/': 5058,  # 网站-地方网站-中国甘肃网-大学生-考试大全
        'http://dxs.gscn.com.cn/xxs/': 5061,  # 网站-地方网站-中国甘肃网-大学生-图片精选
        'http://dxs.gscn.com.cn/zpjy/index.shtml': 5063,  # 网站-地方网站-中国甘肃网-大学生-招生就业
        'http://gansu.gscn.com.cn/msrx/sdgc/index.shtml': 5066,  # 网站-地方网站-中国甘肃网-直通车-深度观察
        'http://gansu.gscn.com.cn/msrx/jrjj/index.shtml': 5068,  # 网站-地方网站-中国甘肃网-直通车-今日聚焦
        'http://gansu.gscn.com.cn/msrx/zxhf/index.shtml': 5070,  # 网站-地方网站-中国甘肃网-直通车-最新回复
        'http://gansu.gscn.com.cn/msrx/zcjd/index.shtml': 5073,  # 网站-地方网站-中国甘肃网-直通车-政策解读
        'http://gansu.gscn.com.cn/msrx/bmfw/index.shtml': 5075,  # 网站-地方网站-中国甘肃网-直通车-便民服务
        'http://gansu.gscn.com.cn/msrx/tt315/index.shtml': 5076,  # 网站-地方网站-中国甘肃网-直通车-天天315
        'http://www.gscn.com.cn/gslz/': 5077,  # 网站-地方网站-中国甘肃网-廉政
        'http://www.gscn.com.cn/gslz/lzyw/index.shtml': 5080,  # 网站-地方网站-中国甘肃网-廉政-廉政要闻
        'http://www.gscn.com.cn/gslz/bgt/index.shtml': 5082,  # 网站-地方网站-中国甘肃网-廉政-曝光台
        'http://www.gscn.com.cn/gslz/zcfg/index.shtml': 5083,  # 网站-地方网站-中国甘肃网-廉政-政策法规
        'http://www.gscn.com.cn/gslz/lltt/index.shtml': 5084,  # 网站-地方网站-中国甘肃网-廉政-理论探讨
        'http://www.gscn.com.cn/gslz/szdt/index.shtml': 5085,  # 网站-地方网站-中国甘肃网-廉政-市州动态
        'http://www.gscn.com.cn/gslz/lzwh/index.shtml': 5086,  # 网站-地方网站-中国甘肃网-廉政-廉政文化
        'http://www.gscn.com.cn/gslz/sdfc/index.shtml': 5087,  # 网站-地方网站-中国甘肃网-廉政-时代风采
        'http://shuhua.gscn.com.cn/gssh/': 5088,  # 网站-地方网站-中国甘肃网-书画-甘肃书画
        'http://shuhua.gscn.com.cn/yszx/': 5089,  # 网站-地方网站-中国甘肃网-书画-艺术资讯
        'http://shuhua.gscn.com.cn/mszt/': 5090,  # 网站-地方网站-中国甘肃网-书画-美术展厅
        'http://shuhua.gscn.com.cn/yhgc/': 5091,  # 网站-地方网站-中国甘肃网-书画-艺海钩沉
        'http://photo.gscn.com.cn/gssj/': 5092,  # 网站-地方网站-中国甘肃网-图片-图说甘肃
        'http://photo.gscn.com.cn/shwx/': 5093,  # 网站-地方网站-中国甘肃网-图片-社会万象
        'http://photo.gscn.com.cn/sz/': 5094,  # 网站-地方网站-中国甘肃网-图片-时政热图
        'http://photo.gscn.com.cn/cthc/': 5095,  # 网站-地方网站-中国甘肃网-图片-趣图荟萃
        'http://photo.gscn.com.cn/yl/': 5096,  # 网站-地方网站-中国甘肃网-图片-娱乐
        'http://photo.gscn.com.cn/ss/': 5101,  # 网站-地方网站-中国甘肃网-图片-时尚
        'http://photo.gscn.com.cn/js/': 5102,  # 网站-地方网站-中国甘肃网-图片-军事

    }
    custom_settings = {
        # 禁止重定向
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    # 防止跳转'<meta http-equiv="refresh" content="0; url=https://live.xinhuaapp.com/xcy/reportlist.html?liveId=156687303133411" />
    custom_settings['DOWNLOADER_MIDDLEWARES']['scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware'] = None

    """
    http://www.gscn.com.cn/culture/system/2019/09/03/012219037.shtml
    http://www.gscn.com.cn/ent/system/2019/09/02/012218638.shtml
    http://www.gscn.com.cn/food/system/2019/09/03/012218786.shtml
    http://news.gscn.com.cn/cms_udf/2019/2019cqx/index.shtml

    """
    rules = (
        # http://theory.gscn.com.cn/system/2019/09/02/012218295.shtml
        # http://gansu.gscn.com.cn/system/2019/09/06/012221292.shtml
        Rule(LinkExtractor(allow=(r'gscn.com.cn.*?/system/%s/\d{2}/\d+.s?html?' % datetime.today().strftime('%Y/%m'),),
                           ),
             callback='parse_item', follow=False),
        #http://news.gscn.com.cn/cms_udf/2019/2019cqx/index.shtml
        #http://gansu.gscn.com.cn/cms_udf/2019/pufazerenqingdan2/index.shtml
        Rule(LinkExtractor(allow=(r'gscn.com.cn.*?/%s/.*?/index.s?html?'%datetime.today().strftime('%Y'),),
                           ),
             callback='parse_time_3', follow=False),

        # 防止正则覆盖不全
        Rule(LinkExtractor(allow=(r'gscn.com.cn.*?.s?htm',), deny=(r'/201[0-8]', r'/20190[1-9]/', '/index.s?htm')
                           ),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        if xp('//meta[@http-equiv="refresh" and starts-with(@content,"0;")]'):
            return self.produce_debugitem(response, '网页跳转')

        if "页面没有找到" in self.get_page_title(response):
            return self.produce_debugitem(response, '网页报错: 页面没有找到')

        try:
            title = self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//div[@class='info']/span[@class='m-frt']/text()").extract_first(''))

            content_div = xp("//div[@class='a-container']") or xp("//div[@class='container']")
            content, media, videos, video_cover = self.content_clean(content_div)  # str  list
            origin_name = xp("//div[@class='info']/span[2]").extract_first("")  # None  不要用[0]
        except Exception as e:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,
        )

    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//span[@id='pubtime_baidu']/text()").extract_first(''))
            content_div = xp("//div[@id='content']")
            content, media, videos, video_cover = self.content_clean(content_div)  # str  list
            origin_name = xp("//span[@id='source_baidu']").extract_first("")  # None  不要用[0]
        except:
            return self.parse_item_3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,
        )

    def parse_item_3(self, response):
        """用于图解"""
        #http://gansu.gscn.com.cn/system/2019/09/05/012221063.shtml
        xp = response.xpath
        try:
            title = xp("//div[@id='info']/h1/text()").extract_first('')
            pubtime = Pubtime(xp("//span[@class='source']/text()").extract_first())
            # content_div = xp("//center[1]/div/div/img/@src") or xp("//div[@class='container']")  # pic_mainbox
            content_div = xp("//div[@id='pic_mainbox']/center") or xp("//center[1]/div/div/img") or xp("//div[@class='container']")
            content, media, _, _ = self.content_clean(content_div)  # str  list
            origin_name = xp("//span[@class='source']/a/text()").extract_first("")  # None  不要用[0]
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

