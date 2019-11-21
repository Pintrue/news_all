# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime

from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class NcNewsSpider(NewsRCSpider):
    """宁夏新闻网"""
    name = 'nxnews'
    mystart_urls = {
        'http://www.nxnews.net': 3884,  # 网站-地方网站-宁夏新闻网
        'http://www.nxnews.net/dz/': 3885,  # 网站-地方网站-宁夏新闻网-政务
        'http://www.nxnews.net/dz/gchd/': 3886,  # 网站-地方网站-宁夏新闻网-政务-高层活动
        'http://www.nxnews.net/sz/gbgs/': 3887,  # 网站-地方网站-宁夏新闻网-政务-人事公示
        'http://www.nxnews.net/dz/wlwz/': 3888,  # 网站-地方网站-宁夏新闻网-政务-网络问政
        'http://www.nxnews.net/dz/tjld/': 3889,  # 网站-地方网站-宁夏新闻网-政务-厅局亮点
        'http://www.nxnews.net/dz/sxfc/': 3890,  # 网站-地方网站-宁夏新闻网-政务-市县风采
        'http://www.nxnews.net/dz/gddt/': 3991,  # 网站-地方网站-宁夏新闻网-政务-各地动态
        'http://www.nxnews.net/dz/ffcl/': 3892,  # 网站-地方网站-宁夏新闻网-政务-反腐倡廉
        'http://www.nxnews.net/dz/jswm/': 3893,  # 网站-地方网站-宁夏新闻网-政务-精神文明
        'http://www.nxnews.net/dz/gqf/': 3894,  # 网站-地方网站-宁夏新闻网-政务-工青妇
        'http://www.nxnews.net/dz/zcjd/': 3895,  # 网站-地方网站-宁夏新闻网-政务-政策解读
        'http://www.nxnews.net/dz/hshy/': 3896,  # 网站-地方网站-宁夏新闻网-政务-红色回忆
        'http://www.nxnews.net/dz/dsyj/': 3897,  # 网站-地方网站-宁夏新闻网-政务-党史研究
        'http://www.nxnews.net/dz/tpbd/': 3898,  # 网站-地方网站-宁夏新闻网-政务-图片报道
        'http://www.nxnews.net/sz/': 3899,  # 网站-地方网站-宁夏新闻网-时政
        'http://www.nxnews.net/sz/nxmfxgc/': 3900,  # 网站-地方网站-宁夏新闻网-时政-宁夏民风新观察
        'http://www.nxnews.net/sz/nxdj/': 3901,  # 网站-地方网站-宁夏新闻网-时政-宁夏点击
        'http://www.nxnews.net/sz/ssjj/': 3902,  # 网站-地方网站-宁夏新闻网-时政-时事聚焦
        'http://www.nxnews.net/sz/gnsm/': 3903,  # 网站-地方网站-宁夏新闻网-时政-国内扫描
        'http://www.nxnews.net/sz/gjss/': 3904,  # 网站-地方网站-宁夏新闻网-时政-国际搜索
        'http://www.nxnews.net/sz/gdjn/': 3906,  # 网站-地方网站-宁夏新闻网-时政-观点集纳
        'http://www.nxnews.net/sz/rdts/': 3907,  # 网站-地方网站-宁夏新闻网-时政-热点推送
        'http://www.nxnews.net/sz/zcjd/': 3908,  # 网站-地方网站-宁夏新闻网-时政-政策焦点
        'http://www.nxnews.net/sz/wmwz/': 3909,  # 网站-地方网站-宁夏新闻网-时政-网民论证
        'http://www.nxnews.net/sh/': 3910,  # 网站-地方网站-宁夏新闻网-社会
        'http://www.nxnews.net/sh/jjcz/': 3911,  # 网站-地方网站-宁夏新闻网-社会-警界传真
        'http://www.nxnews.net/sh/fztd/': 3912,  # 网站-地方网站-宁夏新闻网-社会-法制天地
        'http://www.nxnews.net/sh/jfdt/': 3913,  # 网站-地方网站-宁夏新闻网-社会-检法动态
        'http://www.nxnews.net/sh/shwx/': 3914,  # 网站-地方网站-宁夏新闻网-社会-社会万象
        'http://www.nxnews.net/sh/pl/': 3915,  # 网站-地方网站-宁夏新闻网-社会-评论
        'http://www.nxnews.net/sh/lsdy/': 3916,  # 网站-地方网站-宁夏新闻网-社会-律师答疑
        'http://www.nxnews.net/sh/rdtp_14254/': 3917,  # 网站-地方网站-宁夏新闻网-社会-热点图片
        'http://www.nxnews.net/ds/': 3918,  # 网站-地方网站-宁夏新闻网-地方
        'http://www.nxnews.net/ds/ldhd/': 3919,  # 网站-地方网站-宁夏新闻网-地方-领导活动
        'http://www.nxnews.net/ds/sxld/': 3920,  # 网站-地方网站-宁夏新闻网-地方-市县亮点
        'http://www.nxnews.net/ds/wszw/': 3921,  # 网站-地方网站-宁夏新闻网-地方-五市政务
        'http://www.nxnews.net/ds/ycdt/': 3922,  # 网站-地方网站-宁夏新闻网-地方-银川动态
        'http://www.nxnews.net/ds/szsdt/': 3923,  # 网站-地方网站-宁夏新闻网-地方-石嘴山动态
        'http://www.nxnews.net/ds/wzdt/': 3924,  # 网站-地方网站-宁夏新闻网-地方-吴忠动态
        'http://www.nxnews.net/ds/gydt/': 3925,  # 网站-地方网站-宁夏新闻网-地方-固原动态
        'http://www.nxnews.net/ds/zwdt/': 3926,  # 网站-地方网站-宁夏新闻网-地方-中卫动态
        'http://www.nxnews.net/yx/': 3927,  # 网站-地方网站-宁夏新闻网-映象
        'http://www.nxnews.net/yx/tpsy/': 3928,  # 网站-地方网站-宁夏新闻网-映象-图片首页
        'http://www.nxnews.net/yx/zxrt/': 3929,  # 网站-地方网站-宁夏新闻网-映象-最新热图
        'http://www.nxnews.net/yx/xwjj/': 3930,  # 网站-地方网站-宁夏新闻网-映象-新闻聚焦
        'http://www.nxnews.net/yx/ljl/': 3931,  # 网站-地方网站-宁夏新闻网-映象-零距离
        'http://www.nxnews.net/yx/yxkt/': 3932,  # 网站-地方网站-宁夏新闻网-映象-映象课堂
        'http://www.nxnews.net/yx/yyyd/': 3933,  # 网站-地方网站-宁夏新闻网-映象-影友园地
        'http://www.nxnews.net/yx/syrj/': 3934,  # 网站-地方网站-宁夏新闻网-映象-摄影日记
        'http://www.nxnews.net/yc/': 3935,  # 网站-地方网站-宁夏新闻网-原创
        'http://www.nxnews.net/yc/tsxc/': 3936,  # 网站-地方网站-宁夏新闻网-原创-图说现场
        'http://www.nxnews.net/yc/jrww/': 3937,  # 网站-地方网站-宁夏新闻网-原创-今日网闻
        'http://www.nxnews.net/yc/rdgz/': 3938,  # 网站-地方网站-宁夏新闻网-原创-热点关注
        'http://www.nxnews.net/yc/ztyx/': 3939,  # 网站-地方网站-宁夏新闻网-原创-直通一线
        'http://www.nxnews.net/sx/': 3940,  # 网站-地方网站-宁夏新闻网-思想
        'http://www.nxnews.net/sx/rdps/': 3941,  # 网站-地方网站-宁夏新闻网-思想-热点评述
        'http://www.nxnews.net/sx/nbzp/': 3942,  # 网站-地方网站-宁夏新闻网-思想-政评微评
        'http://www.nxnews.net/sx/sxzk/': 3943,  # 网站-地方网站-宁夏新闻网-思想-百问百答
        'http://www.nxnews.net/sx/sxdpx/': 3944,  # 网站-地方网站-宁夏新闻网-思想-地平线
        'http://www.nxnews.net/sx/nblt/': 3945,  # 网站-地方网站-宁夏新闻网-思想-智库实践
        'http://www.nxnews.net/sx/wpl/': 3946,  # 网站-地方网站-宁夏新闻网-思想-理论学习
        'http://www.nxnews.net/nxrbzk/': 3947,  # 网站-地方网站-宁夏新闻网-周刊
        'http://www.nxnews.net/nxrbzk/nxgs/': 3948,  # 网站-地方网站-宁夏新闻网-周刊-宁夏故事
        'http://www.nxnews.net/nxrbzk/nxrbsxzk/': 3949,  # 网站-地方网站-宁夏新闻网-周刊-思想周刊
        'http://www.nxnews.net/nxrbzk/mszk/': 3950,  # 网站-地方网站-宁夏新闻网-周刊-民生周刊
        'http://www.nxnews.net/nxrbzk/whzk/': 3951,  # 网站-地方网站-宁夏新闻网-周刊-文化周刊
        'http://www.nxnews.net/nxrbzk/jsmlxnx/': 3952,  # 网站-地方网站-宁夏新闻网-周刊-建设美丽新宁夏
        'http://www.nxnews.net/nxrbzk/bwcx/': 3953,  # 网站-地方网站-宁夏新闻网-周刊-不忘初心
        'http://www.nxnews.net/cj/': 3954,  # 网站-地方网站-宁夏新闻网-财经
        'http://www.nxnews.net/cj/wsclz/': 3955,  # 网站-地方网站-宁夏新闻网-财经-网上菜篮子
        'http://www.nxnews.net/cj/cjdyx/': 3956,  # 网站-地方网站-宁夏新闻网-财经-财经第一线
        'http://www.nxnews.net/cj/tt315/': 3957,  # 网站-地方网站-宁夏新闻网-财经-天天315
        'http://www.nxnews.net/cj/hydt/': 3958,  # 网站-地方网站-宁夏新闻网-财经-行业动态
        'http://www.nxnews.net/cj/scfyl/': 3959,  # 网站-地方网站-宁夏新闻网-财经-市场风云录
        'http://www.nxnews.net/cj/jtlcj/': 3960,  # 网站-地方网站-宁夏新闻网-财经-家庭理财经
        'http://www.nxnews.net/cj/cjpl/': 3961,  # 网站-地方网站-宁夏新闻网-财经-财经评论
        'http://www.nxnews.net/cj/cfgsh/': 3962,  # 网站-地方网站-宁夏新闻网-财经-财富故事会
        'http://www.nxnews.net/wh/': 3963,  # 网站-地方网站-宁夏新闻网-文化
        'http://www.nxnews.net/wh/sd/': 3964,  # 网站-地方网站-宁夏新闻网-文化-视点
        'http://www.nxnews.net/wh/whcd/': 3965,  # 网站-地方网站-宁夏新闻网-文化-文化快递
        'http://www.nxnews.net/wh/yscl/': 3966,  # 网站-地方网站-宁夏新闻网-文化-艺术长廊
        'http://www.nxnews.net/wh/whzl/': 3967,  # 网站-地方网站-宁夏新闻网-文化-文化专栏
        'http://www.nxnews.net/wh/lfjs/': 3968,  # 网站-地方网站-宁夏新闻网-文化-雷锋精神
        'http://www.nxnews.net/wh/whjt/': 3969,  # 网站-地方网站-宁夏新闻网-文化-文化讲堂
        'http://www.nxnews.net/wh/nxrw/': 3970,  # 网站-地方网站-宁夏新闻网-文化-宁夏人文
        'http://www.nxnews.net/wh/wlbk/': 3971,  # 网站-地方网站-宁夏新闻网-文化-网络博客
        'http://www.nxnews.net/wh/md/': 3972,  # 网站-地方网站-宁夏新闻网-文化-慢读
        'http://www.nxnews.net/wh/mrt/': 3973,  # 网站-地方网站-宁夏新闻网-文化-名人堂
        'http://www.nxnews.net/wh/lxs/?spm=zm5078-001.0.0.3.gpNzlf': 3974,  # 网站-地方网站-宁夏新闻网-文化-李星书
        'http://www.nxnews.net/wh/shcl/?spm=zm5078-001.0.0.3.rzySPy': 3975,  # 网站-地方网站-宁夏新闻网-文化-书画长廊
        'http://www.nxnews.net/ly/': 3976,  # 网站-地方网站-宁夏新闻网-旅游
        'http://www.nxnews.net/ly/zx/': 3977,  # 网站-地方网站-宁夏新闻网-旅游-资讯
        'http://www.nxnews.net/stzx/': 3978,  # 网站-地方网站-宁夏新闻网-视听在线
        'http://www.nxnews.net/stzx/nxbb/': 3979,  # 网站-地方网站-宁夏新闻网-视听在线-宁夏播报
    }

    # http://topic.nxnews.net/2019/fdxsd/tdwztt/201909/t20190902_6402183.html
    # http://www.nxnews.net/wj/xhsknx/201909/t20190902_6402304.html
    # http://www.nxnews.net/wj/xhsknx/201909/t20190902_6402304.html
    rules = (
        Rule(LinkExtractor(allow=(r'nxnews.net/.*?/t%s\d{2}_\d+.htm' % datetime.today().strftime('%Y%m')), ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'nxnews.net.*?\.s?htm'),
                           deny=(r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/', '/index.s?htm')),
             process_request=otherurl_meta, follow=False),
    )
    custom_settings = {
        # 禁止重定向
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    # http://topic.nxnews.net/2019/fdxsd/tdwztt/201909/t20190902_6402183.html
    def parse_item(self, response):
        xp = response.xpath
        location = xp('//script[re:match(text(), "document.location = a;")]').re('var a="(http.*?)"')
        if location and 'nxnews.net' not in location[0]:
            return self.produce_debugitem(response, '网页跳转')
        try:
            title = xp('.//div[2]/div/div[@class="zwbt"]/text()').extract_first('') or \
                    self.get_page_title(response).split('-')[0]
            source_div = xp('.//div/div[6]/div[@class="listblackf14h25"]')[0]
            content_div = xp('.//div/div[@class="article"]/div[3]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            origin_name = source_div.xpath('.//a/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True)
        except:
            return self.parse_item2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            videos=videos,
            media=media
        )

    # http://www.nxnews.net/yx/xwjj/201908/t20190819_6387058.html
    def parse_item2(self, response):
        xp = response.xpath
        try:
            title = xp('.//div[@class="piccontext"]/h2/text()').extract_first('') or self.get_page_title(response).split('-')[0]
            source_div = xp("//div[@class='source']/div[@class='source_left']")[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = xp('.//div[@class="picmidmid"]')[0]
            origin_name = source_div.xpath('./a').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True)
        except:
            return self.parse_item3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            videos=videos,
            media=media
        )

    # http://www.nxnews.net/stzx/nxbb/201908/t20190830_6400578.html
    def parse_item3(self, response):
        xp = response.xpath
        try:
            title = xp('.//div[@class="title"]/text()').extract_first('')
            source_div = xp("//div[@class='listblackf14h25']")[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = xp('.//div[@class="TRS_Editor"]')[0]
            origin_name = source_div.xpath('./a').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True)
        except:
            return self.parse_item4(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            videos=videos,
            media=media
        )

    # http://www.nxnews.net/stzx/xwzx/gj/201909/t20190902_6402450.html
    def parse_item4(self, response):
        xp = response.xpath
        try:
            title = xp('.//div[@class="TRS_Editor"]/p[2]/text()').extract_first('') or self.get_page_title(response).split('-')[0]
            source_div = xp("//div[@id='header']/div[@class='other']")[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
            content_div = xp('.//div[@class="TRS_Editor"]')[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            videos=videos,
            media=media
        )
