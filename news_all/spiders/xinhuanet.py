# -*- coding: utf-8 -*-
import random
from datetime import datetime
import re
from scrapy.conf import settings
from copy import deepcopy
from urllib.parse import urljoin
import requests
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.tools.agents import USER_AGENTS
from news_all.tools.others import to_list
from news_all.spider_models import NewsRCSpider, otherurl_meta

p = re.compile(r'<title>([\s\S]*?)</title>')
pt = re.compile(r'property="article:publish_time" content="(20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})')
pc = re.compile(r'<script id="all-pics" type="text/html">([\s\S]*?)</script>')


class XinhuanetSpider(NewsRCSpider):
    """新华网"""
    name = 'xinhuanet'

    mystart_urls = {
        'http://www.xinhuanet.com/xhjj.htm': 168,  # '新华聚焦',
        'http://www.xinhuanet.com/politics/': 169,  # '时政',
        'http://www.xinhuanet.com/gangao/index.htm': 170,  # '港澳',
        'http://www.xinhuanet.com/fortune/': 171,  # '财经',
        'http://www.xinhuanet.com/xhsd/index.htm': 172,  # '深度',
        'http://www.xinhuanet.com/world/index.htm': 173,  # '国际',
        # 'http://www.xinhuanet.com/photo/index.htm': 0,  # '测试图集'
        # 'http://www.news.cn/video/index.htm': 0,  # '测试视频'
        # 来自spiders_all
        # 4月22日 打标的
        'http://www.xinhuanet.com//politics/index.htm': 1414,
        'http://www.xinhuanet.com/politics/xgc.htm': 1415,
        'http://www.xinhuanet.com/local/wgzg.htm': 1416,
        'http://www.xinhuanet.com//local/nxw.htm': 1417,
        'http://www.xinhuanet.com//legal/index.htm': 1418,
        'http://www.xinhuanet.com//legal/fy.htm': 1419,
        'http://www.xinhuanet.com/world/hqlft2017/mrjx.htm': 1420,
        'http://www.xinhuanet.com/world/hqlft2017/hqgc.htm': 1421,
        'http://www.xinhuanet.com/world/hqlft2017/gjfun.htm': 1422,
        'http://www.xinhuanet.com//world/hqgc.htm': 1423,
        'http://www.xinhuanet.com//world/wmyl.htm': 1424,
        'http://www.xinhuanet.com/world/hqbl.htm': 1425,
        'http://www.xinhuanet.com//world/jzzl/index.htm': 1426,
        'http://www.xinhuanet.com/asia/ap/apnewsmore.htm': 1427,
        'http://www.xinhuanet.com/asia/ap/politic.htm': 1428,
        'http://www.xinhuanet.com/asia/ap/economic.htm': 1429,
        'http://www.xinhuanet.com/asia/ap/society.htm': 1430,
        'http://www.xinhuanet.com/asia/ap/culture.htm': 1431,
        'http://www.xinhuanet.com/asia/asia_china.htm': 1432,
        'http://www.xinhuanet.com/asia/overseas_chinese/overseas_chmore.htm': 1433,
        'http://www.xinhuanet.com/asia/opinion.htm': 1434,
        'http://www.xinhuanet.com/asia/aboardstudy/info.htm': 1435,
        'http://www.xinhuanet.com/asia/traveling/index.htm': 1436,
        'http://www.xinhuanet.com/asia/investment/index.htm': 1437,
        'http://www.xinhuanet.com/mil/yaowen.htm': 1438,
        'http://www.xinhuanet.com/mil/shijie.htm': 1439,
        'http://www.xinhuanet.com/mil/guandian.htm': 1440,
        'http://www.xinhuanet.com/mil/ruidu.htm': 1441,
        'http://www.xinhuanet.com/mil/zhongguo.htm': 1442,
        'http://www.xinhuanet.com/mil/yuejunqing.htm': 1443,
        'http://www.xinhuanet.com/mil/guofangdongyuan.htm': 1444,
        'http://www.xinhuanet.com/mil/junminronghe.htm': 1445,
        'http://www.xinhuanet.com/mil/hangtianfangwu.htm': 1446,
        'http://www.xinhuanet.com/mil/junyi.htm': 1447,
        'http://www.xinhuanet.com//fortune/': 111,  # 1448,
        'http://www.xinhuanet.com/fortune/caiyan.htm': 1449,
        'http://www.xinhuanet.com/fortune/bcxc.htm': 1450,
        'http://www.news.cn/finance/': 1451,
        'http://www.news.cn/money/index.htm': 1452,
        'http://www.news.cn/money/dj.htm': 1453,
        'http://www.news.cn/money/jrjs.htm': 1454,
        'http://www.news.cn/money/ssjr.htm': 1455,
        'http://www.news.cn/money/rdzt.htm': 1456,
        'http://www.xinhuanet.com//auto/index.htm': 1457,
        'http://www.xinhuanet.com/auto/xw.htm': 1458,
        'http://www.xinhuanet.com/auto/xc.htm': 1459,
        'http://www.xinhuanet.com/auto/sj.htm': 1460,
        'http://www.xinhuanet.com/auto/zwtx.htm': 1461,
        'http://www.xinhuanet.com/auto/bk.htm': 1462,
        'http://www.xinhuanet.com/auto/syc.htm': 1463,
        'http://www.xinhuanet.com/house/yc.htm': 1464,
        'http://www.xinhuanet.com/chanye/': 1465,
        'http://www.xinhuanet.com/house/24xsjx.htm': 1466,
        'http://www.xinhuanet.com/house/jrgz.htm': 1467,
        'http://www.xinhuanet.com/house/djyc.htm': 1468,
        'http://www.xinhuanet.com/house/lpzx.htm': 1469,
        'http://www.xinhuanet.com/ent/zx.htm': 1470,
        'http://www.xinhuanet.com/ent/mx.htm': 1471,
        'http://www.xinhuanet.com/ent/dy.htm': 1472,
        'http://www.xinhuanet.com/ent/ds.htm': 1473,
        'http://www.xinhuanet.com/ent/yy.htm': 1474,
        'http://www.xinhuanet.com/ent/mt.htm': 1475,
        'http://www.xinhuanet.com/ent/pl.htm': 1476,
        'http://sports.xinhuanet.com/news.htm': 1477,
        'http://sports.xinhuanet.com/x_qmjs.htm': 1478,
        'http://sports.xinhuanet.com/x_tycy.htm': 1479,
        'http://sports.xinhuanet.com/x_bxzg.htm': 1480,
        'http://sports.xinhuanet.com/x_xhdj.htm': 1481,
        'http://sports.xinhuanet.com/x_zq.htm': 1482,
        'http://sports.xinhuanet.com/x_mls.htm': 1483,
        'http://www.xinhuanet.com//info/index.htm': 1484,
        'http://www.news.cn/info/yw.htm': 1485,
        'http://www.news.cn/info/tx.htm': 1486,
        'http://www.news.cn/info/ts.htm': 1487,
        'http://www.xinhuanet.com/info/ydhlw.htm': 1488,
        'http://www.xinhuanet.com/info/egtx.htm': 1489,
        'http://www.xinhuanet.com/info/kw.htm': 1490,
        'http://www.xinhuanet.com/politics/rs.htm': 1491,
        'http://www.xinhuanet.com//politics/xhll.htm': 1492,
        'http://www.xinhuanet.com/politics/lldyw.htm': 1493,
        'http://www.xinhuanet.com//gangao/index.htm': 1494,
        'http://www.xinhuanet.com/gangao/gadj.htm': 1495,
        'http://www.xinhuanet.com/gangao/gaddc.htm': 1496,
        'http://www.xinhuanet.com/gangao/djt.htm': 1497,
        'http://www.xinhuanet.com/gangao/gtmrf.htm': 1498,
        'http://www.xinhuanet.com/gangao/gald.htm': 1499,
        'http://www.xinhuanet.com//tw/index.htm': 1500,
        'http://www.xinhuanet.com/tw/2015/xhkt.htm': 1501,
        'http://www.xinhuanet.com/tw/2015/ryt.htm': 1502,
        'http://www.xinhuanet.com/tw/2015/lasx.htm': 1503,
        'http://www.news.cn/tw/2015/mrf.htm': 1504,
        'http://www.news.cn/tw/2015/dlzs.htm': 1505,
        'http://www.news.cn/tw/2015/ppz.htm': 1506,
        'http://www.xinhuanet.com//overseas/index.htm': 1507,
        'http://www.xinhuanet.com/overseas/djyc.htm': 1508,
        'http://www.xinhuanet.com/overseas/hrgs.htm': 1509,
        'http://www.xinhuanet.com/overseas/hgjy.htm': 1510,
        'http://education.news.cn/roll.htm': 1511,
        'http://education.news.cn/djgd.htm': 1512,
        'http://education.news.cn/qw.htm': 112,  # 1513,
        'http://education.news.cn/job.htm': 1514,
        'http://education.news.cn/gaokao/index.htm': 1515,
        'http://education.news.cn/gaokao/gk_xwzx.htm': 1516,
        'http://education.news.cn/gaokao/gk_bkzn.htm': 1517,
        'http://education.news.cn/bschool/zx.htm': 1518,
        'http://www.xinhuanet.com//tech/index.htm': 1519,
        'http://www.xinhuanet.com/tech/hlwj.htm': 1520,
        'http://www.xinhuanet.com/tech/Eyt.htm': 1521,
        'http://www.xinhuanet.com/tech/wgc.htm': 1522,
        'http://www.xinhuanet.com/tech/sxj.htm': 1523,
        'http://www.xinhuanet.com//energy/index.htm': 1524,
        'http://www.xinhuanet.com/energy/dj.htm': 1525,
        'http://www.xinhuanet.com//food/index.htm': 1526,
        'http://www.xinhuanet.com/food/jryw.htm': 1527,
        'http://www.xinhuanet.com/food/sppy/index.htm': 1528,
        'http://www.xinhuanet.com/food/cy/index.htm': 1529,
        'http://www.xinhuanet.com/food/cy/cs.htm': 1530,
        'http://www.xinhuanet.com/food/cy/bgt.htm': 1531,
        'http://www.xinhuanet.com/food/hhb.htm': 1532,
        'http://www.xinhuanet.com/food/gw/gz.htm': 1533,
        'http://www.xinhuanet.com/food/gw/wzy.htm': 1534,
        'http://www.xinhuanet.com/travel/': 1535,
        'http://www.xinhuanet.com/travel/fxb.htm': 1536,

        # 4月24日 打标的
        'http://www.xinhuanet.com/zgjx/jjhw.htm': 2242, 'http://www.xinhuanet.com/zgjx/gcsy/': 2243,
        'http://www.xinhuanet.com/zgjx/sxxxjyhd/': 2244, 'http://www.xinhuanet.com/zgjx/cbyd/zysy.htm': 2245,
        'http://www.xinhuanet.com/zgjx/gjjl/yhwl.htm': 2246, 'http://www.xinhuanet.com/zgjx/mtqy/xxmt.htm': 2247,
        'http://www.xinhuanet.com/zgjx/cmwx.htm': 2248, 'http://www.xinhuanet.com/zgjx/mtqy/cmjj.htm': 2249,
        'http://www.xinhuanet.com/zgjx/cmyj.htm': 2250, 'http://www.xinhuanet.com/zgjx/wp.htm': 2251,
        'http://www.xinhuanet.com/zgjx/gdtt.htm': 2252,
    }

    rules = (
        # http://www.xinhuanet.com/world/2019-07/08/c_1210184057.htm
        Rule(LinkExtractor(allow=r'xinhuanet.com.*?/%s/\d{2}/c_\d+.htm' % datetime.today().strftime('%Y-%m'),
                           deny=('/photo/', '/video/'), ), callback='parse_item',
             follow=False),
        # http://www.xinhuanet.com/photo/2019-03/19/c_1124250770.htm
        Rule(LinkExtractor(allow=r'xinhuanet.com/photo/%s/\d{2}/c_\d{5,}.htm' % datetime.today().strftime('%Y-%m'), ),
             callback='parse_item_2', follow=False),
        Rule(LinkExtractor(allow=r'xinhuanet.com/video/%s/\d{2}/c_\d{5,}.htm' % datetime.today().strftime('%Y-%m'), ),
             callback='parse_videos', follow=False),
        # http://www.xinhuanet.com/asia/2019-05/04/c_1210125179.htm
        Rule(LinkExtractor(allow=r'xinhuanet.com/asia/%s/\d{2}/c_\d{5,}.htm' % datetime.today().strftime('%Y-%m'), ),
             callback='parse_item_6', follow=False),
        Rule(LinkExtractor(allow=r'xinhuanet.com.*?\d{5,}.htm', deny=(r'/201[0-8]', r'/2019-0[1-9]',)),
             process_request=otherurl_meta, follow=False),
    )

    custom_settings = {
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    def parse_item(self, response):
        # http://www.he.xinhuanet.com/xinwen/2019-03/15/c_1124236196.htm
        xp = response.xpath
        try:
            head_div = xp('//div[@class="h-info"]')[0]
            pubtime = head_div.xpath('.//span[@class="h-time"]/text()')[0].extract().strip()
            content_div = xp('//div[@id="p-detail"]')[0]
            title = self.get_title(response)
            origin_name = head_div.xpath('.//span[@class="aticle-src"]/text()').extract_first(
                '').strip() or head_div.xpath('.//span[2]/em[@id="source"]/text()').extract_first(
                '').strip() or head_div.xpath('./span[2]//text()').extract_first('')
            content, media, videos, video_cover = self.content_clean_xinhua(response, content_div)
        except BaseException:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )

    def parse_item_2(self, response):
        # http://www.xinhuanet.com/photo/2019-03/15/c_1210083426.htm 是图集
        # http://www.xinhuanet.com/politics/2019-03/15/c_1124236759.htm 是图集
        # http://www.xinhuanet.com/politics/2019lh/2019-03/08/c_1124209278.htm  不是图集
        # http://www.xinhuanet.com/photo/2019-02/14/c_1210059240.htm
        # http://www.xinhuanet.com/photo/2019-03/27/c_1210092371.htm
        # http://www.xinhuanet.com/mil/2019-04/24/c_1210117296.htm
        xp = response.xpath
        try:
            cvs = xp('//div[@class|@id="content"]') or xp('//span[@class|@id="content"]')
            content_div = cvs[0]
            ps = xp('.//span[@id="pubtime"]/text()').extract() or xp('.//span[@class="h-time"]/text()').extract() or xp(
                './/div[@class="info"]/text()').re('\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}')
            # '2019-05-01 07:00 \r\n来源： 新华网'
            # http://www.xinhuanet.com/science/2019-05/01/c_138024773.htm
            pubtime = ps[0].strip()
        except BaseException:
            return self.parse_item_3(response)

        title = xp('.//*[@id="title"]/text()').extract_first('') or self.get_title(response)
        # http://www.xinhuanet.com/photo/2019-03/15/c_1210083426.htm
        origin_name = xp('.//div[@class="info"]//*[@id="source"]/text()').extract_first('')

        turn_divs = xp('.//div[@id="div_currpage" or contains(@id,"div_page_roll")]/parent::*')
        if turn_divs:  # http://www.xinhuanet.com/photo/static/articler.gif
            next_a = turn_divs[0].xpath('.//a[contains(text(), "下一页")]') or turn_divs[0].xpath(
                './/a/img[contains(@src, "static/articler.gif")]/parent::a')
            if next_a:
                return response.follow(next_a[0], callback=self.parse_page,
                                       meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                             'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                             'content': content_div.extract(),
                                             'start_url_time': response.meta.get('start_url_time'),
                                             'schedule_time': response.meta.get('schedule_time')})

        content, media, videos, video_cover = self.content_clean_xinhua(response, content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )

    def parse_page(self, response):
        meta_new = deepcopy(response.meta)
        xp = response.xpath
        try:
            cvs = xp('//div[@class|@id="content"]') or xp('//span[@class|@id="content"]')
            content_div = cvs[0]
        except BaseException:
            if '已删除或过期的稿件' in self.get_page_title(response):
                return
            return self.produce_debugitem(response, "xpath error")

        meta_new['content'] += content_div.extract()
        turn_divs = xp('.//div[@id="div_currpage"]/parent::*') or xp('.//div[contains(@id,"div_page_roll")]/parent::*')
        if turn_divs:
            turn_div = turn_divs[0]
            next_a = turn_div.xpath('.//a[contains(text(), "下一页")]') or turn_divs[0].xpath(
                './/a/img[contains(@src, "static/articler.gif")]/parent::a')
            if next_a:
                return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)

        content, media, videos, video_cover = self.content_clean(meta_new['content'],
                                                                 kill_xpaths='.//div[@id="div_currpage" or contains(@id,"div_page_roll")]/parent::*')

        return self.produce_item(
            response=response,
            title=meta_new['title'],
            pubtime=meta_new['pubtime'],
            origin_name=meta_new['origin_name'],
            content=content,
            media=media
        )

    def parse_videos(self, response, only_video=False):
        """
        :param response:
        :param only_video:   bool   只需要解视频, 比如在其他parse_item解正文，只在这里解视频
        :return:
        """
        # http://www.xinhuanet.com/video/2019-03/12/c_1210079615.htm
        xp = response.xpath
        try:
            # https://player.v.news.cn/api/v1/getPlayPage?uuid=1_1a20e72966714fc295a9d816818dc691&vid=f2f5d65d8bdb3b63d5b895084e6027f8&playType=0
            ifr = xp('.//iframe[@class="pageVideo"]/@src').extract()[0]
            uuid = re.search('uuid=([0-9a-zA-Z_]+)', ifr).group(1)
            vid = re.search('vid=([0-9a-zA-Z_]+)', ifr).group(1)
            playType = re.search('playType=([0-9]+)', ifr).group(1)
            if playType != "0":
                print('playType!=0~~' * 3, '==', playType, response.url)

        except Exception as e:
            print('video xpath error--' * 5, e)
            return None, None

        url = 'http://player.v.news.cn/api/v1/getConfigs?uuid={}&vid={}'.format(uuid, vid)
        res = requests.get(url, headers={'Cache-Control': 'no-cache', 'Referer': ifr,
                                         'User-Agent': random.choice(USER_AGENTS)}, allow_redirects=False)
        if res.status_code != 200 or res.json().get('code') != 0:
            self.log('video download error, url: %s, video_iframe_src: %s !!' % (response.url, ifr))
            return
        j = res.json()
        videos = {'1': {'src': j['result']["videoInfos"]["src"]}}
        video_cover = to_list(j['result']["videoInfos"]["poster"])

        if only_video:
            return videos, video_cover

        try:
            head_div = xp('//div[@class="h-info"]')[0]
        except:
            return

        pubtime = head_div.xpath('.//span[@class="h-time"]/text()').extract_first('').strip()
        title = ''.join(i.strip() for i in response.xpath('.//div[@class="h-title"]/text()').extract())
        origin_name = head_div.xpath('.//span[@class="aticle-src"]/text()').extract_first('').strip()
        if not origin_name:
            origin_name = head_div.xpath('.//span[2]/em[@id="source"]/text()').extract_first('').strip()
        if not origin_name:
            origin_name = head_div.xpath('./span[2]//text()').extract_first('')
        return self.produce_item(
            response=response,
            title=title if title else self.get_title(response),
            pubtime=pubtime,
            origin_name=origin_name,
            content='<div>#{{1}}#</div>',
            media={},
            videos=videos
        )

    def parse_item_3(self, response):
        # http://www.gd.xinhuanet.com/newscenter/2019-03/14/c_1124230722.htm
        xp = response.xpath
        try:
            content_div = xp('.//div[@class|@id="content"]')[0]
            source_div = xp('.//div[@id="Articlely"]')[0]
            pubtime = source_div.xpath('.//*[@id|@class="laiyuan"]').re('时间： (\d{4}-\d{2}-\d{2} \d{2}:\d{2})')[0]
            title = xp('.//*[@id="ArticleTit"]/text()')[0].extract().strip()
            origin_name = source_div.xpath('.//*[@id|@class="laiyuan"]/a/text()').extract_first()
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True)
        except BaseException:
            return self.parse_item_4(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )

    def parse_item_4(self, response):
        # http://www.xinhuanet.com/politics/2019-02/20/c_1210064167.htm
        # http://sg.xinhuanet.com/2019-02/25/c_1124160546.htm
        xp = response.xpath
        try:
            content_div = xp('//div[@class="article"]')[0]
            pubtime = xp('//*[@class="time"]/text()').extract_first("").strip()
            title = xp('//h1/text()').extract_first("") or self.get_page_title(response).split('-')[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True)
        except BaseException:
            return self.parse_item_5(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media,
            videos=videos
        )

    def parse_item_5(self, response):
        # http://www.hb.xinhuanet.com/2019-03/11/c_1124221757.htm
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="le"]')[0]
            source_div = news_div.xpath('./div[@class="nr_ly"]')[0]
            pubtime = source_div.xpath('./text()')[0].extract().strip()
            title = news_div.xpath('./div[@class="nr_bt"]/text()')[0].extract().strip()
            content_div = news_div.xpath('.//div[@id="nr_wz"]')[0]
            origin_name = source_div.xpath('./em/text()').extract_first("")
            content, media, videos, video_cover = self.content_clean_xinhua(response, content_div)
        except BaseException:
            return self.parse_item_6(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )

    def parse_item_6(self, response):
        # http://www.xinhuanet.com/asia/2019-05/04/c_1210125179.htm
        xp = response.xpath
        try:
            content_div = xp('.//div[@class="ej_box"]/div[@class="bai14"]')[0]
            pubtime = xp('.//span[@id="pubtime"]/text()')[0].extract().strip()
            s = ''.join(xp('.//span[@id="pubtime"]/parent::*/text()').extract())
            og = re.search(r'来源：(.*)', s, re.S)
            origin_name = og.group(1) if og else ""
            content, media, videos, video_cover = self.content_clean_xinhua(response, content_div)
        except BaseException:
            return self.parse_item_7(response)

        return self.produce_item(
            response=response,
            title=self.get_title(response),
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )

    def parse_item_7(self, response):
        # http://sports.xinhuanet.com/c/2019-10/24/c_1125147753.htm
        xp = response.xpath
        try:
            content_div = xp('//div[@class="content"]')[0]
            pubtime = xp("//div[@class='sj']/text()").extract_first("").strip()
            origin_name = xp("//div[@class='ly']/text()").extract_first("")
            content, media, videos, video_cover = self.content_clean_xinhua(response, content_div)
        except BaseException:
            return self.parse_images_2(response)

        return self.produce_item(
            response=response,
            title=self.get_title(response),
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos
        )

    def parse_images_2(self, response):
        title = self.get_title(response)
        pubtime = self.get_pubtime(response)
        content = self.get_content(response)

        if not title or not pubtime or not content:
            if '已删除或过期的稿件' in title:
                return
            else:
                return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="新华网",
            content=content,
            media=media
        )

    def get_title(self, response):
        t = p.search(response.text)
        return re.split(r'-|_', t.group(1))[0] if t else ''

    def get_pubtime(self, response):
        pub = pt.search(response.text)
        # <meta property="article:publish_time" content="2019-03-11T10:18:00+08:00" />
        return pub.group(1).replace('T', ' ') if pub else ''

    def get_content(self, response):
        '''
        http://www.xinhuanet.com/photo/2019-03/11/c_1210078311.htm
        http://www.xinhuanet.com/photo/1210078311_15522705805741n.jpg
        :param response:
        :return:
        '''
        con = pc.search(response.text)
        cont = con.group(1) if con else ''
        cont_new = url_join(cont, response.url)
        return cont_new

    def content_clean_xinhua(self, response, content_div):
        # 1. 判断是否包含video flash 字符串
        if self.video_filter(response.text):  # todo http://www.xinhuanet.com/politics/2019-04/29/c_1124434532.htm
            videos, video_cover = self.parse_videos(response, only_video=True)
            # 2. 判断是否是iframe形式的视频 比如 http://www.hb.xinhuanet.com/2019-03/11/c_1124221757.htm
            if videos:
                # 如果是iframe形式的视频
                content, media, _, _ = self.content_clean(content_div)
                content = '<p>#{{1}}#<p>' + content
                return content, media, videos, video_cover
            else:
                # 如果不是iframe形式的视频, 就假定是<video src=.. poster=..>形式的视频
                content, media, videos, video_cover = self.content_clean(content_div)  # , need_video=True)
                if not videos:
                    print('~*' * 20, 'url: %s, 不是iframe形式的视频, 也不是<video src' % response.url)
                return content, media, videos, video_cover
        return self.content_clean(content_div)

    def content_clean(self, content_div, need_video=False, kill_xpaths=None):
        # 新华网都过滤 点赞
        kill_xpaths = to_list(kill_xpaths) + [r'//div[@class="zan-wap"]', r'//*[text()="图集"]', r'//*[text()="【纠错】"]']
        return super(XinhuanetSpider, self).content_clean(content_div, need_video=need_video, kill_xpaths=kill_xpaths)


def url_join(content, base_url):  # 处理相对链接
    img_fn = lambda x: x if x.startswith('http') else urljoin(base_url, x)
    fr = re.finditer('src="(.*?)"', content)

    new_content = ''

    for i, j in enumerate(fr):
        st = content.find(j.group())
        end = st + len(j.group())
        new_content += content[:st] + 'src=%s' % img_fn(
            j.group(1))  # "../../1210078311_15522705805741n.jpg" todo fix 隐藏bug
        content = content[end:]
    new_content += content
    return new_content


class XinhuanetPhotoSpider(XinhuanetSpider):
    """新华网_photo"""
    name = 'xinhuanet_phote'

    custom_settings = {
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        "SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % XinhuanetSpider.name,
        'DOWNLOADER_MIDDLEWARES':
            {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
             'news_all.middlewares.UserAgentMiddleware': 20,
             'news_all.middlewares.PhantomJSMiddleware': 540,
             }
    }
    start_meta = {'jstype': True}

    mystart_urls = {
        # 7月9日添加
        'http://www.news.cn/photo/zxtp.htm': 19054,
        # 可直接请求http://qc.wa.news.cn/nodeart/list?nid=115481&pgnum=1&cnt=40&tp=1&orderby=0
    }
