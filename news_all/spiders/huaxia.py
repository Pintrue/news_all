# -*- coding: utf-8 -*-
# @Time   : 2019/10/22 下午4:25
# @Author : mez
# @Project : news_all
# @FileName: huaxia_spider.py
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from news_all.tools.time_translater import Pubtime


class Huaxia(NewsRCSpider):
    name = 'huaxia'

    # 华夏网 ==》 补充全站采集
    mystart_urls = {
        'http://huaxia.com/': 6354,   #  华夏经纬网
        'http://huaxia.com/xw/index.html': 6355,   #  华夏经纬网
        'http://huaxia.com/xw/dlxw/index.html': 6356,   #  华夏经纬网
        'http://huaxia.com/xw/twxw/index.html': 6357,   #  华夏经纬网
        'http://huaxia.com/xw/gaxw/index.html': 6358,   #  华夏经纬网
        'http://huaxia.com/xw/gjxw/index.html': 6359,   #  华夏经纬网
        'http://huaxia.com/xw/zhxw/index.html': 6360,   #  华夏经纬网
        'http://huaxia.com/xw/rmdj/index.html': 6361,   #  华夏经纬网
        'http://huaxia.com/xw/tpxw/index.html': 6362,   #  华夏经纬网
        'http://huaxia.com/thpl/index.html': 6363,   #  华夏经纬网
        'http://huaxia.com/thpl/tdyh/index.html': 6364,   #  华夏经纬网
        'http://huaxia.com/thpl/thqrt/index.html': 6365,   #  华夏经纬网
        'http://huaxia.com/thpl/mtlj/index.html': 6366,   #  华夏经纬网
        'http://huaxia.com/thpl/sdfx/index.html': 6367,   #  华夏经纬网
        'http://huaxia.com/thpl/wyps/index.html': 6368,   #  华夏经纬网
        'http://huaxia.com/thpl/jwgc/index.html': 6369,   #  华夏经纬网
        'http://huaxia.com/thpl/thrdts/index.html': 6370,   #  华夏经纬网
        'http://huaxia.com/jjtw/index.html': 6371,   #  华夏经纬网
        'http://huaxia.com/jjtw/dnjq/index.html': 6372,   #  华夏经纬网
        'http://huaxia.com/jjtw/dnsh/index.html': 6373,   #  华夏经纬网
        'http://huaxia.com/jjtw/rdrw/index.html': 6374,   #  华夏经纬网
        'http://huaxia.com/jjtw/twmh/index.html': 6375,   #  华夏经纬网
        'http://huaxia.com/jjtw/jtzdtw/index.html': 6376,   #  华夏经纬网
        'http://huaxia.com/jjtw/twzm/index.html': 6377,   #  华夏经纬网
        'http://huaxia.com/qqla/index.html': 6378,   #  华夏经纬网
        'http://huaxia.com/qqla/tpkzg/index.html': 6379,   #  华夏经纬网
        'http://huaxia.com/qqla/gdrd/index.html': 6380,   #  华夏经纬网
        'http://huaxia.com/qqla/gdzs/index.html': 6381,   #  华夏经纬网
        'http://huaxia.com/qqla/hxsb/index.html': 6382,   #  华夏经纬网
        'http://huaxia.com/qqla/rdzt/index.html': 6383,   #  华夏经纬网
        'http://huaxia.com/thjq/index.html': 6384,   #  华夏经纬网
        'http://huaxia.com/thjq/jsxw/dl/index.html': 6385,   #  华夏经纬网
        'http://huaxia.com/thjq/jsxw/tw/index.html': 6386,   #  华夏经纬网
        'http://huaxia.com/thjq/jsxw/gj/index.html': 6387,   #  华夏经纬网
        'http://huaxia.com/thjq/jsxw/zb/index.html': 6388,   #  华夏经纬网
        'http://huaxia.com/thjq/jswz/index.html': 6389,   #  华夏经纬网
        'http://huaxia.com/thjq/jsgoucheng/index.html': 6390,   #  华夏经纬网
        'http://huaxia.com/thjq/zzhg/index.html': 6391,   #  华夏经纬网
        'http://huaxia.com/thjq/bqdg/index.html': 6392,   #  华夏经纬网
        'http://huaxia.com/thjq/zxkt/index.html': 6393,   #  华夏经纬网
        'http://huaxia.com/thjq/tjzlk/index.html': 6394,   #  华夏经纬网
        'http://huaxia.com/thjq/jswy/index.html': 6395,   #  华夏经纬网
        'http://huaxia.com/thjq/jsyx/index.html': 6396,   #  华夏经纬网
        'http://huaxia.com/tslj/index.html': 6397,   #  华夏经纬网
        'http://huaxia.com/tslj/lasq/index.html': 6398,   #  华夏经纬网
        'http://huaxia.com/tslj/flsj/index.html': 6399,   #  华夏经纬网
        'http://huaxia.com/tslj/rdqy/index.html': 6400,   #  华夏经纬网
        'http://huaxia.com/tslj/rdgc/index.html': 6401,   #  华夏经纬网
        'http://huaxia.com/tslj/jjsp/index.html': 6402,   #  华夏经纬网
        'http://huaxia.com/tslj/zjts/index.html': 6403,   #  华夏经纬网
        'http://huaxia.com/tslj/rdrw/index.html': 6404,   #  华夏经纬网
        'http://huaxia.com/tslj/cfht/index.html': 6405,   #  华夏经纬网
        'http://huaxia.com/tslj/zcfg/index.html': 6406,   #  华夏经纬网
        'http://huaxia.com/tslj/zsgc/index.html': 6407,   #  华夏经纬网
        'http://huaxia.com/tslj/swzt/index.html': 6408,   #  华夏经纬网
        'http://huaxia.com/hxjk/index.html': 6409,   #  华夏经纬网
        'http://huaxia.com/zhwh/index.html': 6410,   #  华夏经纬网
        'http://huaxia.com/ly/index.html': 6411,   #  华夏经纬网
        'http://huaxia.com/ly/lyzx/index.html': 6412,   #  华夏经纬网
        'http://www.huaxia.com/qqla/wgla/index.html': 6413,   #  华夏经纬网
        'http://blog.huaxia.com/': 6414,   #  华夏经纬网
        'http://huaxia.com/lasd/index.html': 6415,   #  华夏经纬网
        'http://huaxia.com/zk/index.html': 6416,   #  华夏经纬网
        'http://huaxia.com/zt/index.html': 6417,   #  华夏经纬网
        'http://www.huaxia.com/hxjk/jkbb/index.html': 6418,   #  华夏经纬网
        'http://www.huaxia.com/hxjk/jkys/yszd/index.html': 6419,   #  华夏经纬网
        'http://www.huaxia.com/hxjk/jkys/shbj/index.html': 6420,   #  华夏经纬网
        'http://www.huaxia.com/hxjk/zhms/msqt/index.html': 6421,   #  华夏经纬网
        'http://www.huaxia.com/hxjk/zhms/yssl/index.html': 6422,   #  华夏经纬网
        'http://www.huaxia.com/hxjk/zhms/klcf/index.html': 6423,   #  华夏经纬网
        'http://www.huaxia.com/hxjk/sssh/clfs/index.html': 6424,   #  华夏经纬网
        'http://www.huaxia.com/hxjk/sssh/mrss/index.html': 6425,   #  华夏经纬网
        'http://www.huaxia.com/hxjk/sssh/zyzz/index.html': 6426,   #  华夏经纬网
        'http://www.huaxia.com/hxjk/sssh/dsqd/index.html': 6427,   #  华夏经纬网
        'http://www.huaxia.com/thpl/yzry/index.html': 6428,   #  华夏经纬网
        'http://www.huaxia.com/thpl/sdfx/index.html': 6429,   #  华夏经纬网
        'http://www.huaxia.com/thpl/tdyh/index.html': 6430,   #  华夏经纬网
        'http://www.huaxia.com/thpl/wyps/index.html': 6431,   #  华夏经纬网
        'http://www.huaxia.com/thpl/jwgc/index.html': 6432,   #  华夏经纬网

    }

    rules = (
        # http://huaxia.com/jx-tw/zjjx/jrjx/2019/11/6264666.html
        # http://huaxia.com/thpl/mtlj/2019/11/6265322.html
        # http://huaxia.com/thpl/wyps/6271183.html
        # http://huaxia.com/zt/js/19-028/6270795.html
        Rule(LinkExtractor(allow=r'.huaxia.com/.*?/%s/\d+\.html' % datetime.today().strftime('%Y/%m'),),
             callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=r'.huaxia.com/.*?\d+\.html', deny=(r'/201[0-8]', r'/2019/0[1-9]',
                                                                    r'/2019/1[0]', r'index')),
             callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=r'.huaxia.com/.*?\.html', deny=(r'/201[0-8]', r'/2019/0[1-9]',
                                                                 r'/2019/1[0]', r'index'),),
             process_request=otherurl_meta,
             follow=False),
    )

    def parse_item(self, response):
        # http://huaxia.com/thpl/mtlj/2019/11/6265322.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='Ftitle']/strong/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//table[@class='style']//font/text()").extract_first())
              # str  list
            try:
                origin_name = xp("//td[@id='oImg']/p[contains(text(),'来源')]/text()").get()
            except:
                origin_name = {}
            # None  不要用[0]
            content_div = xp("//td[@id='oImg']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)
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
        # http://huaxia.com/ytsc/hnyw/2019/11/6266893.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@align='center']/strong/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//table[@class='style']//div[@align='center']/text()").extract_first())
            # str  list
            try:
                origin_name = xp("//table[@class='style']//div[@align='center']/text()").get().split(' ')[-2]
            except:
                origin_name = {}
            # None  不要用[0]
            try:
                content_div = xp("//td[@class='px14']")[0]
            except:
                content_div = xp("//td[@class='content']").get()
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)
        except Exception as e:
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
        # http://huaxia.com/sd-tw/ltwl/2019/11/6266910.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//title/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//head/meta[@name='turbocmspubdate']/@content").extract_first())
            # str  list
            origin_name = "华夏经纬网"
            # None  不要用[0]
            content_div = xp("//td[@class='content']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)
        except Exception as e:
            return self.parse_item_4(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,
        )

    def parse_item_4(self, response):
        # http://huaxia.com/sd-tw/ltwl/2019/11/6266910.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='B002']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//div[@align='center']/text()").extract()[1])
            # str  list
            try:
                origin_name = xp("//td[@class='B004']/p[contains(text(),'来源')]").get()
            except:
                origin_name = {}
            # None  不要用[0]
            content_div = xp("//td[@class='B004']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)
        except Exception as e:
            return self.parse_item_5(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,
        )

    def parse_item_5(self, response):
        # http://huaxia.com/ah-tw/ahyw/2019/11/6267914.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='Ftitle']/strong/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//table[@class='bd6']//div/text()").get())
            # str  list
            try:
                origin_name = xp("//td[@class='px14']/p[contains(text(),'来源')]").get()
            except:
                origin_name = {}
            # None  不要用[0]
            content_div = xp("//td[@class='px14']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,
        )