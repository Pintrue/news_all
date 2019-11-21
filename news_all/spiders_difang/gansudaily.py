# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from copy import deepcopy
from scrapy.conf import settings

from news_all.tools.time_translater import Pubtime


class GanSuDailySpider(NewsRCSpider):
    """每日甘肃网"""
    name = 'gansudaily'
    mystart_urls = {
        'http://www.gansudaily.com.cn': 4410,  # 网站-地方网站-每日甘肃网-首页
        'http://gansu.gansudaily.com.cn': 4411,  # 网站-地方网站-每日甘肃网-甘肃频道
        'http://gansu.gansudaily.com.cn/gsbb/index.shtml': 4412,  # 网站-地方网站-每日甘肃网-甘肃-甘肃播报
        'http://gansu.gansudaily.com.cn/renshirenmian/index.shtml': 4413,  # 网站-地方网站-每日甘肃网-甘肃-人事任免
        'http://gansu.gansudaily.com.cn/quanweifabu/index.shtml': 4414,  # 网站-地方网站-每日甘肃网-甘肃-权威发布
        'http://gansu.gansudaily.com.cn/bwyc/index.shtml': 4415,  # 网站-地方网站-每日甘肃网-甘肃-本网原创
        'http://gansu.gansudaily.com.cn/kgs/index.shtml': 4416,  # 网站-地方网站-每日甘肃网-甘肃-省外媒体看甘肃
        'http://gansu.gansudaily.com.cn/bwfb/index.shtml': 4417,  # 网站-地方网站-每日甘肃网-甘肃-综合发布
        'http://gansu.gansudaily.com.cn/rongmeiti/index.shtml': 4418,  # 网站-地方网站-每日甘肃网-甘肃-融媒体
        'http://hn.gansudaily.com.cn': 4419,  # 网站-地方网站-每日甘肃网-政务
        'http://hn.gansudaily.com.cn/sldhdbd/index.shtml': 4420,  # 网站-地方网站-每日甘肃网-政务-省领导活动报道
        'http://hn.gansudaily.com.cn/rsrm/index.shtml': 4421,  # 网站-地方网站-每日甘肃网-政务-人事任免
        'http://hn.gansudaily.com.cn/lzsy/lzsy-pgt/index.shtml': 4422,  # 网站-地方网站-每日甘肃网-政务-曝光台
        'http://hn.gansudaily.com.cn/zcjd/index.shtml': 4423,  # 网站-地方网站-每日甘肃网-政务-政策解读
        'http://hn.gansudaily.com.cn/qwfb/index.shtml': 4424,  # 网站-地方网站-每日甘肃网-政务-权威发布
        'http://hn.gansudaily.com.cn/rd-zx/index.shtml': 4425,  # 网站-地方网站-每日甘肃网-政务-人大政协
        'http://gansu.gansudaily.com.cn/xwfbt/index.shtml': 4426,  # 网站-地方网站-每日甘肃网-政务-新闻发布厅
        'http://hn.gansudaily.com.cn/system/2007/03/28/010302643.shtml': 4427,  # 网站-地方网站-每日甘肃网-任命
        'http://comment.gansudaily.com.cn/index.shtml': 4428,  # 网站-地方网站-每日甘肃网-时评
        'http://comment.gansudaily.com.cn/zt/index.shtml': 4429,  # 网站-地方网站-每日甘肃网-时评-每日论谈
        'http://comment.gansudaily.com.cn/gmgd/index.shtml': 4430,  # 网站-地方网站-每日甘肃网-时评-甘媒视角
        'http://comment.gansudaily.com.cn/zdtj/index.shtml': 4431,  # 网站-地方网站-每日甘肃网-时评-重点推荐
        'http://comment.gansudaily.com.cn/hptx/index.shtml': 4432,  # 网站-地方网站-每日甘肃网-时评-画评天下
        'http://comment.gansudaily.com.cn/mryl/index.shtml': 4433,  # 网站-地方网站-每日甘肃网-时评-国内媒评
        'http://comment.gansudaily.com.cn/plywj/index.shtml': 4434,  # 网站-地方网站-每日甘肃网-时评-作者文集
        'http://photo.gansudaily.com.cn': 4435,  # 网站-地方网站-每日甘肃网-图片频道
        'http://paper.gansudaily.com.cn/basc/index.shtml': 4436,  # 网站-地方网站-每日甘肃网-图片频道-重大报道
        'http://paper.gansudaily.com.cn/zxxw/index.shtml': 4437,  # 网站-地方网站-每日甘肃网-图片频道-编辑推荐
        'http://paper.gansudaily.com.cn/czyz/index.shtml': 4438,  # 网站-地方网站-每日甘肃网-图片频道-专题策划
        'http://paper.gansudaily.com.cn/gc/index.shtml': 4439,  # 网站-地方网站-每日甘肃网-图片频道-图片新闻
        'http://paper.gansudaily.com.cn/gfxwjca/index.shtml': 4440,  # 网站-地方网站-每日甘肃网-图片频道-老照片
        'http://ll.gansudaily.com.cn': 4441,  # 网站-地方网站-每日甘肃网-理论
        'http://ll.gansudaily.com.cn/zcjd/index.shtml': 4442,  # 网站-地方网站-每日甘肃网-理论-政策解读
        'http://ll.gansudaily.com.cn/djjt/index.shtml': 4443,  # 网站-地方网站-每日甘肃网-理论-大家讲坛
        'http://ll.gansudaily.com.cn/zksk/index.shtml': 4444,  # 网站-地方网站-每日甘肃网-理论-智库建言
        'http://ll.gansudaily.com.cn/gdft/index.shtml': 4445,  # 网站-地方网站-每日甘肃网-理论-领导论政
        'http://ll.gansudaily.com.cn/pingl/index.shtml': 4446,  # 网站-地方网站-每日甘肃网-理论-甘肃评论
        'http://ll.gansudaily.com.cn/ljzs/index.shtml': 4447,  # 网站-地方网站-每日甘肃网-理论-陇军之声
        'http://ll.gansudaily.com.cn/tjch/index.shtml': 4448,  # 网站-地方网站-每日甘肃网-理论-理论专刊
        'http://ll.gansudaily.com.cn/csjy/index.shtml': 4449,  # 网站-地方网站-每日甘肃网-理论-参事建言
        'http://culture.gansudaily.com.cn': 4450,  # 网站-地方网站-每日甘肃网-文化
        'http://culture.gansudaily.com.cn/whxw/': 4451,  # 网站-地方网站-每日甘肃网-文化-甘肃文化
        'http://culture.gansudaily.com.cn/rwft/': 4452,  # 网站-地方网站-每日甘肃网-文化-人物访谈
        'http://culture.gansudaily.com.cn/xbdl/': 4453,  # 网站-地方网站-每日甘肃网-文化-西部地理
        'http://culture.gansudaily.com.cn/whbl/': 4454,  # 网站-地方网站-每日甘肃网-文化-文化博览
        'http://culture.gansudaily.com.cn/whzt/': 4455,  # 网站-地方网站-每日甘肃网-文化-文化杂谈
        'http://culture.gansudaily.com.cn/ysdt/': 4456,  # 网站-地方网站-每日甘肃网-文化-艺术动态
        'http://culture.gansudaily.com.cn/whysh/index.shtml': 4457,  # 网站-地方网站-每日甘肃网-文化-戏剧影视
        'http://culture.gansudaily.com.cn/hmdq/': 4458,  # 网站-地方网站-每日甘肃网-文化-书画鉴赏
        'http://culture.gansudaily.com.cn/scpm/': 4459,  # 网站-地方网站-每日甘肃网-文化-收藏拍卖
        'http://culture.gansudaily.com.cn/wtdt/': 4460,  # 网站-地方网站-每日甘肃网-文化-文坛动态
        'http://culture.gansudaily.com.cn/ds/': 4461,  # 网站-地方网站-每日甘肃网-文化-文学书评
        'http://culture.gansudaily.com.cn/wxzp/': 4462,  # 网站-地方网站-每日甘肃网-文化-美文欣赏
        'http://culture.gansudaily.com.cn/shfz/': 4463,  # 网站-地方网站-每日甘肃网-文化-历史揭秘
        'http://culture.gansudaily.com.cn/whkg/': 4464,  # 网站-地方网站-每日甘肃网-文化-文化考古
        'http://culture.gansudaily.com.cn/lzgs/': 4465,  # 网站-地方网站-每日甘肃网-文化-陇原故事
        'http://culture.gansudaily.com.cn/lsmr/': 4466,  # 网站-地方网站-每日甘肃网-文化-历史名人
        'http://tour.gansudaily.com.cn': 4467,  # 网站-地方网站-每日甘肃网-旅游
        'http://tour.gansudaily.com.cn/lyzx/index.shtml': 4468,  # 网站-地方网站-每日甘肃网-旅游-旅游快讯
        'http://tour.gansudaily.com.cn/hdzhq/': 4469,  # 网站-地方网站-每日甘肃网-旅游-活动专区
        'http://tour.gansudaily.com.cn/lxs/': 4470,  # 网站-地方网站-每日甘肃网-旅游-酒店推荐
        'http://tour.gansudaily.com.cn/jdjs/': 4471,  # 网站-地方网站-每日甘肃网-旅游-甘肃景区推荐
        # 'http://tour.gansudaily.com.cn/lxs/': 4472,  # 网站-地方网站-每日甘肃网-旅游-旅行社
        'http://tour.gansudaily.com.cn/lydt/': 4473,  # 网站-地方网站-每日甘肃网-旅游-游在甘肃
        'http://tour.gansudaily.com.cn/klyx/': 4474,  # 网站-地方网站-每日甘肃网-旅游-自驾游
        'http://tour.gansudaily.com.cn/szls/': 4475,  # 网站-地方网站-每日甘肃网-旅游-出行资讯
        'http://tour.gansudaily.com.cn/jpxl/': 4476,  # 网站-地方网站-每日甘肃网-旅游-路线推荐
        'http://tour.gansudaily.com.cn/tour_hr/': 4477,  # 网站-地方网站-每日甘肃网-旅游-投诉爆料
        'http://tour.gansudaily.com.cn/local_snacks/': 4478,  # 网站-地方网站-每日甘肃网-旅游-陇原美食
        'http://tour.gansudaily.com.cn/lycp/': 4479,  # 网站-地方网站-每日甘肃网-旅游-特色产品
        'http://tour.gansudaily.com.cn/photo/': 4480,  # 网站-地方网站-每日甘肃网-旅游-行者达人
        'http://finance.gansudaily.com.cn': 4481,  # 网站-地方网站-每日甘肃网-财经
        'http://finance.gansudaily.com.cn/cjyw/': 4482,  # 网站-地方网站-每日甘肃网-财经-财经要闻
        'http://finance.gansudaily.com.cn/gs/': 4483,  # 网站-地方网站-每日甘肃网-财经-股市
        'http://finance.gansudaily.com.cn/dp/': 4484,  # 网站-地方网站-每日甘肃网-财经-大盘
        'http://finance.gansudaily.com.cn/bk/': 4485,  # 网站-地方网站-每日甘肃网-财经-板块
        'http://finance.gansudaily.com.cn/cyb/': 4486,  # 网站-地方网站-每日甘肃网-财经-创业板
        'http://finance.gansudaily.com.cn/hydt/': 4487,  # 网站-地方网站-每日甘肃网-财经-行业动态
        'http://finance.gansudaily.com.cn/bx/': 4488,  # 网站-地方网站-每日甘肃网-财经-保险
        'http://finance.gansudaily.com.cn/jj/': 4489,  # 网站-地方网站-每日甘肃网-财经-基金
        'http://finance.gansudaily.com.cn/whfy/': 4490,  # 网站-地方网站-每日甘肃网-财经-外汇
        'http://finance.gansudaily.com.cn/qh/': 4491,  # 网站-地方网站-每日甘肃网-财经-期贷
        'http://finance.gansudaily.com.cn/cylc/': 4492,  # 网站-地方网站-每日甘肃网-财经-创业理财
        'http://finance.gansudaily.com.cn/xfwq/': 4493,  # 网站-地方网站-每日甘肃网-财经-消费维权
        'http://finance.gansudaily.com.cn/cjsp/': 4494,  # 网站-地方网站-每日甘肃网-财经-评论
        'http://finance.gansudaily.com.cn/cjrw/': 4495,  # 网站-地方网站-每日甘肃网-财经-人物
        'http://edu.gansudaily.com.cn': 4496,  # 网站-地方网站-每日甘肃网-教育
        'http://edu.gansudaily.com.cn/lgxd/': 4497,  # 网站-地方网站-每日甘肃网-教育-独家策划
        'http://edu.gansudaily.com.cn/jylw/': 4498,  # 网站-地方网站-每日甘肃网-教育-教委快报
        'http://edu.gansudaily.com.cn/jyxw/': 4499,  # 网站-地方网站-每日甘肃网-教育-教育资讯
        'http://edu.gansudaily.com.cn/jyrw/': 4500,  # 网站-地方网站-每日甘肃网-教育-每日会客厅
        'http://edu.gansudaily.com.cn/sdbd/': 4501,  # 网站-地方网站-每日甘肃网-教育-活动专区
        'http://edu.gansudaily.com.cn/jygc/': 4502,  # 网站-地方网站-每日甘肃网-教育-问教平台
        'http://edu.gansudaily.com.cn/xy/': 4503,  # 网站-地方网站-每日甘肃网-教育-校长风采
        'http://edu.gansudaily.com.cn/yxzx/': 4504,  # 网站-地方网站-每日甘肃网-教育-校园巡礼
        'http://edu.gansudaily.com.cn/jycp/': 4505,  # 网站-地方网站-每日甘肃网-教育-教育时评
        'http://edu.gansudaily.com.cn/ks/': 4506,  # 网站-地方网站-每日甘肃网-教育-考试专区
        'http://edu.gansudaily.com.cn/cglx/': 4507,  # 网站-地方网站-每日甘肃网-教育-留学求职
        'http://zgao.gansudaily.com.cn': 4508,  # 网站-地方网站-每日甘肃网-专稿
        'http://zgao.gansudaily.com.cn/djxw/': 4509,  # 网站-地方网站-每日甘肃网-专稿-独家新闻
        'http://zgao.gansudaily.com.cn/tbbd/': 4510,  # 网站-地方网站-每日甘肃网-专稿-特别报道
        'http://zgao.gansudaily.com.cn/qwxwfb/': 4511,  # 网站-地方网站-每日甘肃网-专稿-权威新闻发布
        'http://zgao.gansudaily.com.cn/ztbd/index.shtml': 4512,  # 网站-地方网站-每日甘肃网-专稿-专题报道
        'http://zgao.gansudaily.com.cn/lyjj/index.shtml': 4513,  # 网站-地方网站-每日甘肃网-专稿-陇原聚焦
        'http://zgao.gansudaily.com.cn/lygd/index.shtml': 4514,  # 网站-地方网站-每日甘肃网-专稿-陇原各地
        'http://zgao.gansudaily.com.cn/qyfc/index.shtml': 4515,  # 网站-地方网站-每日甘肃网-专稿-企业风采
        'http://sp.gansudaily.com.cn': 4516,  # 网站-地方网站-每日甘肃网-枣视频
        'http://sp.gansudaily.com.cn/xwzx/index.shtml': 4517,  # 网站-地方网站-每日甘肃网-枣视频-新闻资讯
        'http://sp.gansudaily.com.cn/gxpk/index.shtml': 4518,  # 网站-地方网站-每日甘肃网-枣视频-枣视频
        'http://sp.gansudaily.com.cn/ycsp/index.shtml': 4519,  # 网站-地方网站-每日甘肃网-枣视频-精彩视频
        'http://sp.gansudaily.com.cn/zfsc/index.shtml': 4520,  # 网站-地方网站-每日甘肃网-枣视频-作风视窗
        'http://sp.gansudaily.com.cn/wgy/index.shtml': 4521,  # 网站-地方网站-每日甘肃网-枣视频-微公益
        'http://sp.gansudaily.com.cn/jbft/index.shtml': 4522,  # 网站-地方网站-每日甘肃网-枣视频-嘉宾访谈
        'http://sp.gansudaily.com.cn/shss/index.shtml': 4523,  # 网站-地方网站-每日甘肃网-枣视频-食尚甘肃
        'http://sp.gansudaily.com.cn/sp_yl/index.shtml': 4524,  # 网站-地方网站-每日甘肃网-枣视频-健康讲堂
        'http://sp.gansudaily.com.cn/yxly/index.shtml': 4525,  # 网站-地方网站-每日甘肃网-枣视频-在线直播
        'http://szkb.gansudaily.com.cn': 4526,  # 网站-地方网站-每日甘肃网-通讯员
        'http://szkb.gansudaily.com.cn/jjfz/index.shtml': 4527,  # 网站-地方网站-每日甘肃网-通讯员-经济发展
        'http://szkb.gansudaily.com.cn/szxw/index.shtml': 4528,  # 网站-地方网站-每日甘肃网-通讯员-经济发展
        'http://szkb.gansudaily.com.cn/whcx/index.shtml': 4529,  # 网站-地方网站-每日甘肃网-通讯员-文化创新
        'http://szkb.gansudaily.com.cn/shsy/index.shtml': 4530,  # 网站-地方网站-每日甘肃网-通讯员-社会事业
        'http://szkb.gansudaily.com.cn/stwm/index.shtml': 4531,  # 网站-地方网站-每日甘肃网-通讯员-精准扶贫
        # 'http://szkb.gansudaily.com.cn/stwm/index.shtml': 4532,  # 网站-地方网站-每日甘肃网-通讯员-生态事业
        # 'http://gansu.gansudaily.com.cn/xwfbt/index.shtml': 4533,  # 网站-地方网站-每日甘肃网-新闻发布
        'http://gansu.gansudaily.com.cn/xwfbt/fbsl/index.shtml': 4534,  # 网站-地方网站-每日甘肃网-新闻发布-最新发布
        'http://gansu.gansudaily.com.cn/xwfbt/zxfb/index.shtml': 4535,  # 网站-地方网站-每日甘肃网-新闻发布-发布实录
        'http://gansu.gansudaily.com.cn/xwfbt/zbhf/index.shtml': 4536,  # 网站-地方网站-每日甘肃网-新闻发布-直播回放
        'http://gansu.gansudaily.com.cn/xwfbt/bmfb/index.shtml': 4537,  # 网站-地方网站-每日甘肃网-新闻发布-重要发布会
        'http://gansu.gansudaily.com.cn/xwfbt/mtjj/index.shtml': 4538,  # 网站-地方网站-每日甘肃网-新闻发布-媒体聚焦
        'http://gansu.gansudaily.com.cn/xwfbt/tsgs/index.shtml': 4539,  # 网站-地方网站-每日甘肃网-新闻发布-图说甘肃
        'http://gansu.gansudaily.com.cn/xwfbt/xwfyr/index.shtml': 4540,  # 网站-地方网站-每日甘肃网-新闻发布-新闻发言人

    }

    custom_settings = {
        'DEPTH_LIMIT': 0,
        # 禁止重定向
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    # 防止跳转'<meta http-equiv="refresh" content="0; url=https://live.xinhuaapp.com/xcy/reportlist.html?liveId=156687303133411" />
    custom_settings['DOWNLOADER_MIDDLEWARES']['scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware'] = None

    # http://gansu.gansudaily.com.cn/system/2019/08/30/017254063.shtml
    rules = (
        Rule(LinkExtractor(allow=(r'gansudaily.com.cn/system/%s/\d{2}/\d+.s?htm'% datetime.today().strftime('%Y/%m')), ),
             callback='parse_item', follow=False),

        Rule(LinkExtractor(allow=(r'gansudaily.com.cn.*?/\d+.s?htm'),
                           deny=(r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/')),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        if xp('//meta[@http-equiv="refresh" and starts-with(@content,"0;")]'):
            return self.produce_debugitem(response, '网页跳转')

        if "页面没有找到" in self.get_page_title(response):
            return self.produce_debugitem(response, '网页报错: 页面没有找到')

        try:
            title = xp('.//h1/text()').extract_first('') or self.get_page_title(response).split('-')[0]
            pubtime = Pubtime(xp('.//div[@id="nleft"]').extract_first(''))
            content_div = xp('.//div[@class="artical"]/div[@id="conter2018"]')[0]
            origin_name = xp('.//div[@id="nleft"]/span[2]/a/text()').extract_first('')
            next_a = xp('.//a[contains(text(), "下一页")]')
            if next_a:
                return response.follow(next_a[0], callback=self.parse_page,
                                       meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                             'pubtime': pubtime, 'origin_name': origin_name,
                                             'content': content_div.extract(), 'title': title,
                                             'start_url_time': response.meta.get('start_url_time'),
                                             'schedule_time': response.meta.get('schedule_time')
                                             })
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            videos=videos,
            media=media
        )

    def parse_page(self, response):
        meta_new = deepcopy(response.meta)
        xp = response.xpath
        try:
            content_div = xp('.//div[@class="artical"]/div[@id="conter2018"]')[0]
            meta_new['content'] += content_div.extract()
            next_a = xp('.//a[contains(text(), "下一页")]')
            if next_a:
                return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
            content, media, videos, video_cover = self.content_clean(meta_new['content'],
                                                                     kill_xpaths=["//div[@id='news_more_page_div_id']",
                                                                                  "//div[@class='a-footer']/span[@class='frt']"])
        except:
            return self.produce_debugitem(response, 'xpath error')

        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),
            content=content,
            media=media
        )