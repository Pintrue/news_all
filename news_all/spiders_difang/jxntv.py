# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta, otherurl_meta
from news_all.tools.others import get_sub_str_ex
from news_all.tools.time_translater import Pubtime


class JxnTvSpider(NewsRCSpider):
    """今视网"""
    name = 'jxntv'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        'http://www.jxntv.cn/': 3980,  # 网站-地方网站-今视网-首页
        'http://news.jxntv.cn/': 3981,  # 网站-地方网站-今视网-新闻
        'http://special.jxntv.cn/ymkjx/': 3982,  # 网站-地方网站-今视网-新闻-央媒看江西
        'http://news.jxntv.cn/?ch=61&ca=61,13': 3983,  # 网站-地方网站-今视网-新闻-原创
        'http://news.jxntv.cn/?ch=45&ca=45,156': 3984,  # 网站-地方网站-今视网-新闻-国内
        'http://news.jxntv.cn/?ch=160': 3985,  # 网站-地方网站-今视网-新闻-社会
        'http://news.jxntv.cn/?ch=159': 3986,  # 网站-地方网站-今视网-新闻-国际
        'http://news.jxntv.cn/?ch=163': 3987,  # 网站-地方网站-今视网-新闻-科教
        'http://travel.jxntv.cn/': 3988,  # 网站-地方网站-今视网-新闻-文旅
        'http://news.jxntv.cn/?ch=162': 3989,  # 网站-地方网站-今视网-新闻-财经
        'http://news.jxntv.cn/?ch=166': 3990,  # 网站-地方网站-今视网-新闻-军事
        'http://news.jxntv.cn/?ch=170': 3991,  # 网站-地方网站-今视网-新闻-评论
        'http://news.jxntv.cn/?ch=171': 3992,  # 网站-地方网站-今视网-新闻-纪录片
        'http://news.jxntv.cn/?ch=305': 3993,  # 网站-地方网站-今视网-新闻-专栏活动
        'http://news.jxntv.cn/?ch=411': 3994,  # 网站-地方网站-今视网-新闻-少儿
        'http://news.jxntv.cn/?ch=180': 3995,  # 网站-地方网站-今视网-新闻-公益
        'http://news.jxntv.cn/?ch=301': 3996,  # 网站-地方网站-今视网-新闻-百科
        'http://news.jxntv.cn/?ch=304': 3997,  # 网站-地方网站-今视网-新闻-房产
        'http://news.jxntv.cn/?ch=302': 3998,  # 网站-地方网站-今视网-新闻-情感
        'http://news.jxntv.cn/?ch=303': 3999,  # 网站-地方网站-今视网-新闻-汽车
        'http://opinion.jxntv.cn/': 4000,  # 网站-地方网站-今视网-江右时评
        'http://www.jxntv.cn/list/s355/': 4001,  # 网站-地方网站-今视网-江右时评-江右锐评
        'http://www.jxntv.cn/list/s358/': 4002,  # 网站-地方网站-今视网-江右时评-江右前沿
        'http://www.jxntv.cn/list/s357/': 4003,  # 网站-地方网站-今视网-江右时评-江右视评
        'http://www.jxntv.cn/list/s359/': 4004,  # 网站-地方网站-今视网-江右时评-江右图说
        'http://v.jxntv.cn/': 4005,  # 网站-地方网站-今视网-视频-江西卫视
        'http://v.jxntv.cn/?ch=139': 27,  # 网站-地方网站-今视网-视频-都市频道
        'http://v.jxntv.cn/?ch=140': 4006,  # 网站-地方网站-今视网-视频-经济生活频道
        'http://v.jxntv.cn/?ch=141': 4007,  # 网站-地方网站-今视网-视频-影视旅游频道
        'http://v.jxntv.cn/?ch=142': 4008,  # 网站-地方网站-今视网-视频-公共农业频道
        'http://v.jxntv.cn/?ch=143': 4009,  # 网站-地方网站-今视网-视频-少儿频道
        'http://v.jxntv.cn/?ch=144': 4010,  # 网站-地方网站-今视网-视频-新闻频道
        'http://v.jxntv.cn/?ch=145': 4011,  # 网站-地方网站-今视网-视频-移动电视
        'http://v.jxntv.cn/?ch=408': 4013,  # 网站-地方网站-今视网-视频-新闻广播
        'http://v.jxntv.cn/?ch=389': 4014,  # 网站-地方网站-今视网-视频-网台独播
        'http://v.jxntv.cn/?ch=387': 4015,  # 网站-地方网站-今视网-视频-赣江新闻
        'http://special.jxntv.cn/': 38,  # 网站-地方网站-今视网-专题
        'http://www.jxntv.cn/list/s337/': 39,  # 网站-地方网站-今视网-专题-新闻专题
        'http://www.jxntv.cn/list/s345/': 40,  # 网站-地方网站-今视网-专题-视频专题
        'http://www.jxntv.cn/list/s347/': 41,  # 网站-地方网站-今视网-专题-娱乐专题
        'http://www.jxntv.cn/list/s348/': 4016,  # 网站-地方网站-今视网-专题-H5策划
        'http://www.jxntv.cn/list/s350/': 43,  # 网站-地方网站-今视网-专题-网络专栏
        'http://www.jxntv.cn/list/s1250/': 44,  # 网站-地方网站-今视网-专题-活动专栏
        'http://special.jxntv.cn/jxdxfbt/': 4017,  # 网站-地方网站-今视网-典型发布厅
        'http://news.jxntv.cn/jxxwfbt/': 4018,  # 网站-地方网站-今视网-新闻发布厅
        'http://health.jxntv.cn/': 4019,  # 网站-地方网站-今视网-健康
        'http://www.jxntv.cn/list/s757/': 4020,  # 网站-地方网站-今视网-健康-要闻
        'http://www.jxntv.cn/list/s756/': 4021,  # 网站-地方网站-今视网-健康-曝光台
        'http://www.jxntv.cn/list/s762/': 4022,  # 网站-地方网站-今视网-健康-寻医
        'http://www.jxntv.cn/list/s786/': 4023,  # 网站-地方网站-今视网-健康-养生谈
        'http://www.jxntv.cn/list/s791/': 4024,  # 网站-地方网站-今视网-健康-饮食
        'http://www.jxntv.cn/list/s789/': 4025,  # 网站-地方网站-今视网-健康-两性
        'http://edu.jxntv.cn/': 4026,  # 网站-地方网站-今视网-教育
        'http://www.jxntv.cn/list/s802/': 4027,  # 网站-地方网站-今视网-教育-要闻
        'http://www.jxntv.cn/list/s803/': 4028,  # 网站-地方网站-今视网-教育-快讯
        'http://www.jxntv.cn/list/s808/': 4029,  # 网站-地方网站-今视网-教育-地市动态
        'http://www.jxntv.cn/list/s801/': 4030,  # 网站-地方网站-今视网-教育-视频专题
        'http://www.jxntv.cn/list/s809/': 4031,  # 网站-地方网站-今视网-教育-校园新闻
        'http://www.jxntv.cn/list/s810/': 4032,  # 网站-地方网站-今视网-教育-教育与法
        'http://www.jxntv.cn/list/s814/': 4033,  # 网站-地方网站-今视网-教育-名校展示
        'http://www.jxntv.cn/list/s815/': 4034,  # 网站-地方网站-今视网-教育-图说教育
        'http://fa.jxntv.cn/': 4035,  # 网站-地方网站-今视网-法制
        'http://www.jxntv.cn/list/s836/': 4036,  # 网站-地方网站-今视网-法制-新闻
        'http://www.jxntv.cn/list/s866/': 4037,  # 网站-地方网站-今视网-法制-视频播报
        'http://www.jxntv.cn/list/s837/': 4038,  # 网站-地方网站-今视网-法制-警方行动
        'http://www.jxntv.cn/list/s838/': 4039,  # 网站-地方网站-今视网-法制-法院在线
        'http://www.jxntv.cn/list/s839/': 4040,  # 网站-地方网站-今视网-法制-检察风云
        'http://www.jxntv.cn/list/s840/': 4041,  # 网站-地方网站-今视网-法制-司法天地
        'http://www.jxntv.cn/list/s851/': 4042,  # 网站-地方网站-今视网-法制-案件实录
        'http://www.jxntv.cn/list/s842/': 4043,  # 网站-地方网站-今视网-法制-社会管理
        'http://finance.jxntv.cn/': 4044,  # 网站-地方网站-今视网-金融
        'http://www.jxntv.cn/list/s728/': 4045,  # 网站-地方网站-今视网-金融-金融要闻
        'http://www.jxntv.cn/list/s729/': 4046,  # 网站-地方网站-今视网-金融-股票
        'http://www.jxntv.cn/list/s730/': 4047,  # 网站-地方网站-今视网-金融-曝光台
        'http://www.jxntv.cn/list/s737/': 4048,  # 网站-地方网站-今视网-金融-基金
        'http://www.jxntv.cn/list/s740/': 4049,  # 网站-地方网站-今视网-金融-期货
        'http://www.jxntv.cn/list/s738/': 4050,  # 网站-地方网站-今视网-金融-银行
        'http://www.jxntv.cn/list/s741/': 4051,  # 网站-地方网站-今视网-金融-保险
    }
    # http://news.jxntv.cn/2019/0902/9238509.shtml
    # http://v.jxntv.cn/2019/0725/9213817.shtml
    # 非动态采集
    # http://finance.jxntv.cn/2019/0827/9234960.shtml   经济
    # http://health.jxntv.cn/2019/0903/9239220.shtml    健康
    # http://edu.jxntv.cn/2018/0707/8923577.shtml       教育
    # http://fa.jxntv.cn/2019/0816/9228275.shtml        法制
    # http://finance.jxntv.cn/2019/0903/9239229.shtml   金融
    rules = (
        Rule(LinkExtractor(allow=(r'news.jxntv.cn/%s\d{2}/\d+.s?htm' % datetime.today().strftime('%Y/%m')), ),
             callback='parse_item', follow=False, process_request=js_meta),
        Rule(LinkExtractor(allow=(r'v.jxntv.cn/%s\d{2}/\d+.s?htm' % datetime.today().strftime('%Y/%m')), ),
             callback='parse_item2', follow=False),
        Rule(LinkExtractor(allow=(
                    r'(?:finance|health|edu|fa|opinion).jxntv.cn/%s\d{2}/\d+.s?htm' % datetime.today().strftime(
                '%Y/%m')), ),
             callback='parse_item', follow=False),

        Rule(LinkExtractor(allow=(r'jxntv.cn.*?/\d+.s?htm'),
                           deny=(r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/')),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        # http://news.jxntv.cn/2019/0902/9238509.shtml
        xp = response.xpath
        try:
            title = xp('.//h1/text()').extract_first('') or self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp('.//div[@class="info"]').extract_first(''))
            content_div = xp('.//div[@class="content"]')[0]
            origin_name = xp('//span[@class="source"]/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True,
                                                                     kill_xpaths=["//div[contains(@class,'control')]",
                                                                                  "//div[contains(@class,'playback')]",
                                                                                  "//div[contains(@class,'error')]"])
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

    # http://v.jxntv.cn/2019/0814/9227037.shtml
    def parse_item2(self, response):
        xp = response.xpath
        try:
            title = xp('.//h1/text()').extract_first('') or self.get_page_title(response).split('_')[0]
            js_text = xp('//script[re:match(text(), "cjxtv-html5-player-video")]').extract()[0]
            video_url = next(get_sub_str_ex(js_text, 'preload="" src="', '"', greedy=False))

            pubtime = Pubtime(xp('.//div[@class="info"]/span[@class="date"]/text()').extract_first(''))
            # content_div = xp('.//div[@id="ckplayer"]//video')[0]
            origin_name = xp('//span[@class="source"]/a/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content='<div>#{{1}}#</div>',
            media={},
            videos={'1': {'src': video_url}},
        )

    # http://news.jxntv.cn/2019/0608/9181039.shtml#1_2
    def parse_item3(self, response):
        xp = response.xpath
        try:
            title = xp('.//h1/text()').extract_first('') or self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp('.//div[@class="info"]').extract_first(''))
            content_div = xp('.//div[@class="thumbbox"]')[0]
            origin_name = xp('//span[@class="source"]/text()').extract_first('')
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
