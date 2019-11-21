# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.tools.others import to_list
from news_all.spider_models import NewsRCSpider, otherurl_meta


class CeSpider(NewsRCSpider):
    """中国经济网"""
    name = 'ce'

    mystart_urls = {
        'http://finance.ce.cn/': 206,  # 金融证券
        'http://www.ce.cn/cysc/': 207,  # 产业市场

        # 来自spiders_all
        'http://auto.ce.cn/car/cj/': 1090, 'http://book.ce.cn/': 1091,
        'http://city.ce.cn/main/economy/': 1093, 'http://travel.ce.cn/xsy/cy/': 1095,
        'http://city.ce.cn/main/observation/': 1096, 'http://finance.ce.cn/2015home/jj/': 1097,
        'http://finance.ce.cn/rolling/index.shtml': 1098, 'http://finance.ce.cn/sub/cj2009/': 1099,
        'http://finance.ce.cn/stock/gsgdbd/index.shtml': 1104, 'http://finance.ce.cn/10cjsy/ds/': 1106,
        'http://finance.ce.cn/10cjsy/gs/': 1107, 'http://finance.ce.cn/10cjsy/bg/': 1108,
        'http://finance.ce.cn/10cjsy/ss/': 1109, 'http://finance.ce.cn/10cjsy/hy/': 1110,
        'http://finance.ce.cn/10cjsy/bk/': 1111, 'http://finance.ce.cn/10cjsy/zl/': 1112,
        'http://finance.ce.cn/bank/xdfx/': 1113, 'http://finance.ce.cn/bank/lccp/': 1115,
        'http://finance.ce.cn/bank/dzyh/': 1116, 'http://finance.ce.cn/bank/sryh/': 1117,
        'http://finance.ce.cn/bank/yw/index.shtml': 1118, 'http://finance.ce.cn/hlwjr/': 1119,
        'http://finance.ce.cn/shqgc/sc/': 1125, 'http://finance.ce.cn/insurance/ylbx/': 1126,
        'http://finance.ce.cn/rz/rzgd/index.shtml': 1127, 'http://finance.ce.cn/money/2016lc/rdjj/': 1128,
        'http://finance.ce.cn/insurance/ccbx/': 1129, 'http://finance.ce.cn/insurance/jkx/': 1130,
        'http://finance.ce.cn/insurance/ywx/': 1131, 'http://finance.ce.cn/insurance/zbx/': 1132,
        'http://finance.ce.cn/insurance/zcfg/': 1133, 'http://finance.ce.cn/insurance/bxlp/': 1134,
        'http://finance.ce.cn/insurance/jjdt/': 1135,
        'http://finance.ce.cn/insurance1/scrollnews/index.shtml': 2455,
        'http://finance.ce.cn/insurance/yw/index.shtml': 2456, 'http://finance.ce.cn/shqgc/pl/': 2457,
        'http://finance.ce.cn/sub/ggttk/index.shtml': 2458,
        'http://finance.ce.cn/jjpd/jjpddyp/jjpdyw/': 2459, 'http://finance.ce.cn/jjpd/jjpdgd/': 2460,
        'http://finance.ce.cn/jjpd/jjpddyp/zjsd/': 2461, 'http://finance.ce.cn/jjpd/jjpddyp/jjks/': 2462,
        'http://finance.ce.cn/xwjr/gd/index.shtml': 2463,
        'http://finance.ce.cn/sub/cj2009/index.shtml': 2464,
        'http://finance.ce.cn/sub/ssgsrs/index.shtml': 2465, 'http://finance.ce.cn/xsb/xsbrdjj/': 2466,
        'http://finance.ce.cn/fe/gdxw/index.shtml': 2467, 'http://www.ce.cn/cysc/fdc/fc/': 2468,
        'http://www.ce.cn/cysc/newmain/pplm/qyxx/': 2469,
        'http://www.ce.cn/cysc/00/02/index_19191.shtml': 2470, 'http://www.ce.cn/cysc/tech/gd2012/': 2471,
        'http://www.ce.cn/cysc/zljd/qwfb/': 2472, 'http://gongyi.ce.cn/': 2473,
        'http://city.ce.cn/main/build/': 2474, 'http://city.ce.cn/main/ecological/': 2475,
        'http://city.ce.cn/main/exclusive/': 2476, 'http://www.ce.cn/cysc/zljd/hb/': 2477,
        'http://www.ce.cn/cysc/zljd/xfyj/': 2478, 'http://www.ce.cn/cysc/zljd/yqhz/': 2479,
        'http://www.ce.cn/cysc/zljd/fwzl/': 2480, 'http://www.ce.cn/cysc/zljd/gd/': 2481,
        'http://www.ce.cn/cysc/sp/info/': 2482, 'http://www.ce.cn/cysc/sp/bwzg/': 2483,
        'http://www.ce.cn/cysc/zgjd/kx/': 2484, 'http://www.ce.cn/cysc/zgjd/jdsh/': 2485,
        'http://www.ce.cn/cysc/zgjd/yjxw/': 2486, 'http://www.ce.cn/cysc/zgjd/yjcb/': 2487,
        'http://www.ce.cn/cysc/zgjd/hyfx/': 2488, 'http://www.ce.cn/cysc/zgjd/wgsv/': 2489,
        'http://www.ce.cn/cysc/yy/hydt/': 2490, 'http://www.ce.cn/cysc/yy/yyhhb/': 2491,
        'http://www.ce.cn/cysc/yy/qwfb/': 2492, 'http://www.ce.cn/2012sy/gd/index.shtml': 2493,
        'http://www.ce.cn/cysc/ny/gdxw/index.shtml': 2494, 'http://www.ce.cn/cysc/newmain/jdpd/yj/': 2495,
        'http://www.ce.cn/cysc/jtys/yw/': 2496, 'http://www.ce.cn/cysc/jtys/tielu/': 2497,
        'http://www.ce.cn/cysc/jtys/hangkong/': 2498, 'http://www.ce.cn/cysc/jtys/haiyun/': 2499,
        'http://www.ce.cn/cysc/jtys/csjt/': 2500, 'http://www.ce.cn/cysc/newmain/jdpd/fz/': 2501,
        'http://www.ce.cn/cysc/newmain/yc/jjsp/': 2502, 'http://www.ce.cn/cysc/yq/': 2503,
        'http://www.ce.cn/cysc/stwm/zxdt/index.shtml': 2504, 'http://www.ce.cn/xwzx/xinwen/jsyw/': 2505,
        'http://www.ce.cn/xwzx/xinwen/bwzg/index.shtml': 2506, 'http://www.ce.cn/xwzx/gnsz/gdxw/': 2507,
        'http://www.ce.cn/xwzx/xinwen/sz/rdpl/': 2508, 'http://www.ce.cn/xwzx/shgj/gdxw/': 2509,
        'http://www.ce.cn/xwzx/fazhi/': 2510, 'http://www.ce.cn/xwzx/kj/index.shtml': 2511,
        'http://www.ce.cn/xwzx/xinwen/shfz/jjyf/': 2512, 'http://www.ce.cn/xwzx/xinwen/kjjy/kpzs/': 2513,
        'http://www.ce.cn/xwzx/xinwen/kjjy/jyzx/': 2514, 'http://www.ce.cn/xwzx/gnsz/szyw/': 2515,
        'http://www.ce.cn/macro/more/index.shtml': 2516, 'http://views.ce.cn/main/yc/index.shtml': 2517,
        'http://views.ce.cn/main/disc/index_2738.shtml': 2518,
        'http://views.ce.cn/main/jdrp/index.shtml': 2519, 'http://views.ce.cn/main/qy/index.shtml': 2520,
        'http://views.ce.cn/fun/who/': 2521, 'http://views.ce.cn/main/net/index.shtml': 2522,
        'http://views.ce.cn/view/economy/index.shtml': 2523,
        'http://views.ce.cn/view/obs/index.shtml': 2524, 'http://auto.ce.cn/auto/gundong/': 2525,
        'http://auto.ce.cn/car/zx/': 2526, 'http://auto.ce.cn/car/xc/': 2527,
        'http://auto.ce.cn/car/lx/': 2528, 'http://auto.ce.cn/car/hsc/': 2529,
        'http://auto.ce.cn/car/yc/': 2530, 'http://auto.ce.cn/auto/shijia/index.shtml': 2531,
        'http://auto.ce.cn/auto/gundong/index.shtml': 2532,
        'http://www.ce.cn/newmain/right/feature/index.shtml': 2533, 'http://tuopin.ce.cn/yw/': 2534,
        'http://www.ce.cn/culture/gd/': 2535, 'http://www.ce.cn/culture/whcyk/bjtj/': 2536,
        'http://www.ce.cn/culture/whcyk/yaowen/': 2537, 'http://www.ce.cn/culture/whcyk/zg/': 2538,
        'http://shuhua.ce.cn/sy2015/pmxw/': 2539, 'http://book.ce.cn/news/': 2540,
        'http://travel.ce.cn/xsy/fb/': 2541, 'http://travel.ce.cn/xsy/jd/': 2542,
        'http://travel.ce.cn/xsy/yq/': 2543, 'http://travel.ce.cn/gdtj/': 2544,
        'http://gongyi.ce.cn/news/': 2545, 'http://gongyi.ce.cn/gy/gyxd/index.shtml': 2546,
        'http://gongyi.ce.cn/news/index.shtml': 2547, 'http://health.ce.cn/sy2015/jkzx/': 2548,
        'http://health.ce.cn/sy2015/ysbj/': 2549, 'http://health.ce.cn/news/': 2550,
        'http://city.ce.cn/main/focusnews/': 2551, 'http://district.ce.cn/newarea/poll/': 2552,
        'http://district.ce.cn/newarea/jjdt/': 2553, 'http://district.ce.cn/newarea/zsyz/': 2554,
        'http://district.ce.cn/newarea/tscy/': 2555, 'http://district.ce.cn/zt/rwk/rw/renshi/': 2556,
        'http://district.ce.cn/zt/rwk/rw/fanfu/': 2557,
        'http://district.ce.cn/newarea/roll/index.shtml': 2558, 'http://fashion.ce.cn/news/?': 2559,
        'http://ent.ce.cn/news/': 2560, 'http://fashion.ce.cn/mlc/': 2561, 'http://tech.ce.cn/news/': 2562,
        'http://tech.ce.cn/tech2018/kx/': 2563, 'http://tech.ce.cn/tech2018/rgzn/': 2564,
        'http://tech.ce.cn/tech2018/life/': 2565, 'http://tech.ce.cn/tech2018/newtech/': 2566,
        'http://tech.ce.cn/tech2018/safe/': 2567, 'http://www.ce.cn/cysc/yy/gdpl/': 2568,
        'http://cv.ce.cn/xsy/spq/gdxw/index.shtml': 2569, 'http://cv.ce.cn/zxz/zxzbwzg/': 2570,
        'http://cv.ce.cn/zxz/zxzhydt/': 2571, 'http://cv.ce.cn/zxz/zxzqyxw/': 2572,
        'http://cv.ce.cn/fwz/jtxx/': 2573, 'http://cv.ce.cn/fwz/ypss/': 2574,
        'http://www.ce.cn/cysc/zgjd/qycz/': 2575
    }

    # http://finance.ce.cn/bank12/scroll/201901/18/t20190118_31293743.shtml
    rules = (
        # http://m.ce.cn/bwzg/201905/08/t20190508_32023129.shtml
        Rule(LinkExtractor(allow=(r'm.ce.cn/bwzg/%s/\d{2}/t\d+_\d+.s?html' % datetime.today().strftime('%Y%m'),), ),
             callback='parse_item_2',
             follow=False),
        Rule(LinkExtractor(allow=(r'tech.ce.cn/news/%s/\d{2}/t\d+_\d+.s?html' % datetime.today().strftime('%Y%m'),), ),
             callback='parse_item_3',
             follow=False),
        Rule(LinkExtractor(allow=(r'ce.cn.*?/%s/\d{2}/t\d+_\d+.s?html' % datetime.today().strftime('%Y%m'),), ),
             callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=(r'ce.cn.*?\d+.s?html',),
                           deny=(r'index_\d+.s?htm', r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/')),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            head_div = xp('.//div[@class="laiyuan"]')[0]
            content_div = xp('.//div[@id="articleText"]')[0]
            pubtime = head_div.xpath(
                './span[@id="articleTime"]/text()')[0].extract().replace('\n', '').strip()
            origin_name = head_div.xpath(
                './span[@id="articleSource"]/text()').extract_first()
            content, media, *_ = self.content_clean(content_div)
        except IndexError:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('_')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_2(self, response):
        # http://m.ce.cn/bwzg/201905/08/t20190508_32023129.shtml
        xp = response.xpath
        try:
            pubtime = xp(
                '//div[@class="md_ly clearfix"]/span[@class="time"]/text()')[0].extract()
            og = xp(
                '//div[@class="md_ly clearfix"]/span[@class="media_ly"]/text()').extract()
            content_div = xp('//div[@class="TRS_Editor"]')[0]
            content, media, *_ = self.content_clean(content_div)
        except IndexError:
            return self.parse_item_3(response)

        return self.produce_item(
            response=response,
            title=self.get_page_title(response).split('_')[0],
            pubtime=pubtime,
            origin_name=og[0] if og else "",
            content=content,
            media=media
        )

    def parse_item_3(self, response):
        # http://tech.ce.cn/news/201905/14/t20190514_32068957.shtml
        xp = response.xpath
        try:
            head_div = xp('//div[@class="title"]/div[@class="titbar1"]')[0]
            pubtime = head_div.xpath(
                './span[@id="articleTime"]/text()')[0].extract()
            origin_name = head_div.xpath(
                './span[@id="articleSource"]/text()').extract_first('')
            content_div = xp('//div[@class="TRS_Editor"]')[0]
            title = xp('//div[@class="title"]/h1/text()').extract_first('')
            content, media, *_ = self.content_clean(content_div)
        except IndexError:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,  # self.get_page_title(response).split('—')[0],
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def content_clean(self, content_div, need_video=False, kill_xpaths=None):
        kill_xpaths = to_list(kill_xpaths) + [r'//*[contains(text(), "更多精彩内容，请点击进入")]',
                                              r'//*[starts-with(text(), "更多地方人事报道请见")]',
                                              r'//*[starts-with(text(), "更多中央人事任免请见")]']
        return super(CeSpider, self).content_clean(
            content_div, need_video=need_video, kill_xpaths=kill_xpaths)


class CeSzSpider(CeSpider):
    """中国经济网"""
    name = 'ce_sz'
    # allowed_domains = ['ce.cn']
    mystart_urls = {
        'http://www.ce.cn/xwzx/': 208,  # 时政社会
    }
    custom_settings = {
        "SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % CeSpider.name,
        # 'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
    }
    rules = (
        # http://www.ce.cn/xwzx/gnsz/gdxw/201904/23/t20190423_31917101.shtml
        Rule(LinkExtractor(allow=(r'ce.cn.*?/%s/\d{2}/t\d+_\d+.s?html' % datetime.today().strftime('%Y%m'),),
                           deny=r'district\.ce\.cn/zt/rwk/',
                           restrict_xpaths='//div[@class="con"]/div[1]/div[1]//a'),
             callback='parse_item',
             follow=False),)
