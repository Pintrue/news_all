#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/2 12:37
# @Author  : wjq
# @File    : iqilu.py


from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class IqiluSpider(NewsRCSpider):
    """齐鲁网"""
    name = 'iqilu'
    mystart_urls = {
        'http://news.iqilu.com': 4541,  # 网站-地方网站-齐鲁网-新闻
        'http://www.iqilu.com/html/scroll/': 4542,  # 网站-地方网站-齐鲁网-新闻-最新
        'http://news.iqilu.com/shandong/': 4543,  # 网站-地方网站-齐鲁网-新闻-山东
        'http://news.iqilu.com/china/': 4544,  # 网站-地方网站-齐鲁网-新闻-国内
        'http://news.iqilu.com/guoji/': 4545,  # 网站-地方网站-齐鲁网-新闻-国际
        'http://news.iqilu.com/shehui/': 4546,  # 网站-地方网站-齐鲁网-新闻-社会
        'http://news.iqilu.com/shandong/zhengwu/': 4547,  # 网站-地方网站-齐鲁网-权威发布-政务要闻
        'http://www.iqilu.com/html/shouquan/tongzhi/': 4548,  # 网站-地方网站-齐鲁网-权威发布-采访通知
        'http://www.iqilu.com/html/yangguanglianxian/yangguanglianxian/': 4549,  # 网站-地方网站-齐鲁网-一次办好-最新报道
        'http://pinglun.iqilu.com': 4550,  # 网站-地方网站-齐鲁网-时评
        'http://pinglun.iqilu.com/weipinglun/': 4551,  # 网站-地方网站-齐鲁网-时评-微评论
        'http://pinglun.iqilu.com/yuanchuang/': 4552,  # 网站-地方网站-齐鲁网-时评-原创阵地
        'http://pinglun.iqilu.com/meiti/': 4553,  # 网站-地方网站-齐鲁网-时评-媒体言论
        'http://pinglun.iqilu.com/jiaodian/': 4554,  # 网站-地方网站-齐鲁网-时评-时政焦点
        'http://pinglun.iqilu.com/zatan/': 4555,  # 网站-地方网站-齐鲁网-时评-民生杂谈
        'http://theory.iqilu.com/llcs/lldt/': 4556,  # 网站-地方网站-齐鲁网-理论-理论动态
        'http://theory.iqilu.com/xsx/': 4557,  # 网站-地方网站-齐鲁网-理论-新思想
        'http://theory.iqilu.com/qlpz/': 4558,  # 网站-地方网站-齐鲁网-理论-齐鲁篇章
        'http://theory.iqilu.com/llcs/llyj/': 4559,  # 网站-地方网站-齐鲁网-理论-理论原创
        'http://theory.iqilu.com/llqy/': 4560,  # 网站-地方网站-齐鲁网-理论-理论前沿
        'http://theory.iqilu.com/llcs/llrd/': 4561,  # 网站-地方网站-齐鲁网-理论-理论热点
        'http://sports.iqilu.com': 4562,  # 网站-地方网站-齐鲁网-体育
        'http://sports.iqilu.com/luneng/': 4563,  # 网站-地方网站-齐鲁网-体育-山东鲁能
        'http://sports.iqilu.com/sdnanlan/': 4564,  # 网站-地方网站-齐鲁网-体育-西王男篮
        'http://sports.iqilu.com/news/': 4565,  # 网站-地方网站-齐鲁网-体育-综合体育
        'http://sports.iqilu.com/zuqiu/': 4566,  # 网站-地方网站-齐鲁网-体育-足球
        'http://sports.iqilu.com/lanqiu/': 4567,  # 网站-地方网站-齐鲁网-体育-篮球
        'http://sports.iqilu.com/guojizuqiu/': 4568,  # 网站-地方网站-齐鲁网-体育-国际足球
        'http://sports.iqilu.com/nba/': 4569,  # 网站-地方网站-齐鲁网-体育-NBA
        'http://ent.iqilu.com': 4570,  # 网站-地方网站-齐鲁网-娱乐
        'http://ent.iqilu.com/news/': 4571,  # 网站-地方网站-齐鲁网-娱乐-明星
        'http://ent.iqilu.com/film/news/': 4572,  # 网站-地方网站-齐鲁网-娱乐-电影
        'http://ent.iqilu.com/tv/': 4573,  # 网站-地方网站-齐鲁网-娱乐-电视
        'http://ent.iqilu.com/music/': 4574,  # 网站-地方网站-齐鲁网-娱乐-音乐
        'http://ent.iqilu.com/pic/': 4575,  # 网站-地方网站-齐鲁网-娱乐-图片
        'http://www.iqilu.com/html/zt/picstalk/': 4576,  # 网站-地方网站-齐鲁网-网画连篇
        'http://wurenji.iqilu.com/kxw/': 4577,  # 网站-地方网站-齐鲁网-无人机频道-瞰新闻
        'http://wurenji.iqilu.com/vrqj/': 4598,  # 网站-地方网站-齐鲁网-无人机频道-VR全景
        'http://hongqi.iqilu.com/szyw/': 4600,  # 网站-地方网站-齐鲁网-红旗云-时政要闻
        'http://hongqi.iqilu.com/rd/': 4611,  # 网站-地方网站-齐鲁网-红旗云-热点
        'http://hongqi.iqilu.com/jcdt/': 4613,  # 网站-地方网站-齐鲁网-红旗云-基层动态
        'http://hongqi.iqilu.com/lxyz/': 4614,  # 网站-地方网站-齐鲁网-红旗云-两学一做
        'http://hongqi.iqilu.com': 4616,  # 网站-地方网站-齐鲁网-红旗云
        'http://www.iqilu.com/html/sdzs/sjcf/': 4618,  # 网站-地方网站-齐鲁网-数据控-数据厨房
        'http://www.iqilu.com/html/sdzs/shandongzs/': 4620,  # 网站-地方网站-齐鲁网-数据控-山东指数
        'http://www.iqilu.com/html/sdzs/sjlb/': 4621,  # 网站-地方网站-齐鲁网-数据控-数据联播
        'http://travel.iqilu.com': 4624,  # 网站-地方网站-齐鲁网-旅游
        'http://travel.iqilu.com/xinwen/': 4633,  # 网站-地方网站-齐鲁网-旅游-新闻
        'http://travel.iqilu.com/xinwen/shandong/': 4641,  # 网站-地方网站-齐鲁网-旅游-山东
        'http://travel.iqilu.com/xinwen/guoji/': 4645,  # 网站-地方网站-齐鲁网-旅游-国际
        'http://travel.iqilu.com/xinwen/guonei/': 4647,  # 网站-地方网站-齐鲁网-旅游-国内
        'http://travel.iqilu.com/cyql/': 4649,  # 网站-地方网站-齐鲁网-旅游-畅游齐鲁
        'http://travel.iqilu.com/cyql/jingqu/': 4650,  # 网站-地方网站-齐鲁网-旅游-旅游景区
        'http://travel.iqilu.com/cyql/dongtai/': 4652,  # 网站-地方网站-齐鲁网-旅游-动态
        'http://travel.iqilu.com/cyql/xianlu/': 4657,  # 网站-地方网站-齐鲁网-旅游-线路
        'http://travel.iqilu.com/wanbar/': 4658,  # 网站-地方网站-齐鲁网-旅游-玩吧
        'http://travel.iqilu.com/lyjq/': 4659,  # 网站-地方网站-齐鲁网-旅游-节庆活动
        'http://edu.iqilu.com': 4660,  # 网站-地方网站-齐鲁网-教育
        'http://edu.iqilu.com/news/': 4661,  # 网站-地方网站-齐鲁网-教育-头条
        'http://edu.iqilu.com/zxx/': 4662,  # 网站-地方网站-齐鲁网-教育-中小教育
        'http://edu.iqilu.com/gxbk/gaoxiao/ptgx/': 4663,  # 网站-地方网站-齐鲁网-教育-大学之家
        'http://edu.iqilu.com/ywbk/zfjg/': 4664,  # 网站-地方网站-齐鲁网-教育-权威发布
        'http://edu.iqilu.com/kaosheng/': 4665,  # 网站-地方网站-齐鲁网-教育-教育培训
        'http://caijing.iqilu.com': 4666,  # 网站-地方网站-齐鲁网-财经
        'http://caijing.iqilu.com/cjxw/': 4667,  # 网站-地方网站-齐鲁网-财经-财经新闻
        'http://caijing.iqilu.com/cjxc/': 4669,  # 网站-地方网站-齐鲁网-财经-独家报道
        'http://caijing.iqilu.com/yhxw/': 4671,  # 网站-地方网站-齐鲁网-财经-银行
        'http://caijing.iqilu.com/bxxw/': 4683,  # 网站-地方网站-齐鲁网-财经-保险
        'http://caijing.iqilu.com/zqxw/': 4685,  # 网站-地方网站-齐鲁网-财经-证券
        'http://caijing.iqilu.com/tzjq/': 4687,  # 网站-地方网站-齐鲁网-财经-投资
        'http://caijing.iqilu.com/nengyuan/nynews/': 4689,  # 网站-地方网站-齐鲁网-财经-能源
        'http://caijing.iqilu.com/guancha/': 4691,  # 网站-地方网站-齐鲁网-财经-政策
        'http://caijing.iqilu.com/cjzx/': 4693,  # 网站-地方网站-齐鲁网-财经-资讯
        'http://caijing.iqilu.com/lccp/lccp/': 4695,  # 网站-地方网站-齐鲁网-财经-理财
        'http://ppsd.iqilu.com/#': 4696,  # 网站-地方网站-齐鲁网-品牌
        'http://ppsd.iqilu.com/ywdt/': 4698,  # 网站-地方网站-齐鲁网-品牌-要闻动态
        'http://ppsd.iqilu.com/ppsj/': 4700,  # 网站-地方网站-齐鲁网-品牌-品牌视界
        'http://ppsd.iqilu.com/pprw/': 4702,  # 网站-地方网站-齐鲁网-品牌-品牌人物
        'http://ppsd.iqilu.com/lqfc/': 4703,  # 网站-地方网站-齐鲁网-品牌-鲁企风采
        'http://ppsd.iqilu.com/xmhd/': 4706,  # 网站-地方网站-齐鲁网-品牌-项目活动
        'http://house.iqilu.com': 4708,  # 网站-地方网站-齐鲁网-房产
        'http://house.iqilu.com/ajnfc/hyzx/': 4710,  # 网站-地方网站-齐鲁网-房产-行业资讯
        'http://house.iqilu.com/ajnfc/xyxinwen/': 4711,  # 网站-地方网站-齐鲁网-房产-行业新闻
        'http://house.iqilu.com/ajnfc/dongtai/': 4712,  # 网站-地方网站-齐鲁网-房产-楼盘动态
        'http://house.iqilu.com/ajnfc/wqbg/': 4713,  # 网站-地方网站-齐鲁网-房产-维权曝光
        'http://house.iqilu.com/ajnfc/rmhuodong/': 4714,  # 网站-地方网站-齐鲁网-房产-热门活动
        'http://house.iqilu.com/ajnfc/yldichan/': 4715,  # 网站-地方网站-齐鲁网-房产-娱乐地产
        'http://house.iqilu.com/ajnfc/zxgl/': 4717,  # 网站-地方网站-齐鲁网-房产-装修攻略
        'http://health.iqilu.com': 4719,  # 网站-地方网站-齐鲁网-健康
        'http://health.iqilu.com/stjk/': 4741,  # 网站-地方网站-齐鲁网-健康-身体健康
        'http://health.iqilu.com/stjk/jkyw/': 4743,  # 网站-地方网站-齐鲁网-健康-健康要闻
        'http://health.iqilu.com/jydh/': 4744,  # 网站-地方网站-齐鲁网-健康-就医导航
        'http://health.iqilu.com/zixun/': 4747,  # 网站-地方网站-齐鲁网-健康-卫计新闻
        'http://health.iqilu.com/jkkp/': 4749,  # 网站-地方网站-齐鲁网-健康-健康科普
        'http://health.iqilu.com/jkkp/zhongyi/': 4750,  # 网站-地方网站-齐鲁网-健康-中医
        'http://health.iqilu.com/jkkp/qz/': 4751,  # 网站-地方网站-齐鲁网-健康-母婴
        'http://health.iqilu.com/jkkp/mr/': 4752,  # 网站-地方网站-齐鲁网-健康-医美
        'http://health.iqilu.com/jkkp/xywy/': 4753,  # 网站-地方网站-齐鲁网-健康-疾病
        'http://health.iqilu.com/jkkp/yangsheng/': 4754,  # 网站-地方网站-齐鲁网-健康-保健
        'http://qiche.iqilu.com': 4755,  # 网站-地方网站-齐鲁网-汽车
        'http://qiche.iqilu.com/chewen/': 4756,  # 网站-地方网站-齐鲁网-汽车-山东车闻
        'http://qiche.iqilu.com/xinche/': 4757,  # 网站-地方网站-齐鲁网-汽车-本月新车
        'http://qiche.iqilu.com/shouce/': 4761,  # 网站-地方网站-齐鲁网-汽车-新能源汽车
        'http://qiche.iqilu.com/zixun/': 4765,  # 网站-地方网站-齐鲁网-汽车-汽车资讯
        'http://qiche.iqilu.com/shijia/': 4766,  # 网站-地方网站-齐鲁网-汽车-实拍测评
        'http://qiche.iqilu.com/sjhd/': 4768,  # 网站-地方网站-齐鲁网-汽车-团购图鉴
        'http://qiche.iqilu.com/fangtan/': 4769,  # 网站-地方网站-齐鲁网-汽车-汽车论道
        'http://art.iqilu.com': 4771,  # 网站-地方网站-齐鲁网-艺术
        'http://art.iqilu.com/zixun/': 4773,  # 网站-地方网站-齐鲁网-艺术-新闻
        'http://art.iqilu.com/yishujia/': 4775,  # 网站-地方网站-齐鲁网-艺术-艺术家
        'http://art.iqilu.com/yingxiang/': 4779,  # 网站-地方网站-齐鲁网-艺术-唐三彩
        'http://art.iqilu.com/yishujia/jianshang/': 4780,  # 网站-地方网站-齐鲁网-艺术-展览
        'http://food.iqilu.com': 4781,  # 网站-地方网站-齐鲁网-食安
        'http://food.iqilu.com/fabu/': 4782,  # 网站-地方网站-齐鲁网-食安-权威发布
        'http://food.iqilu.com/ppyl/': 4783,  # 网站-地方网站-齐鲁网-食安-品牌引领
        'http://food.iqilu.com/dongtai/': 4784,  # 网站-地方网站-齐鲁网-食安-城市创建
        'http://food.iqilu.com/xfjs/': 4785,  # 网站-地方网站-齐鲁网-食安-消费警示
        'http://food.iqilu.com/flfg/': 4786,  # 网站-地方网站-齐鲁网-食安-法律法规
        'http://food.iqilu.com/jiangtang/': 4787,  # 网站-地方网站-齐鲁网-食安-食安课堂
        'http://laoxiang.iqilu.com/zixun/': 4788,  # 网站-地方网站-齐鲁网-老乡-老乡资讯
        'http://laoxiang.iqilu.com/lxyx/': 4789,  # 网站-地方网站-齐鲁网-老乡-老乡影像
        'http://yx.iqilu.com': 4790,  # 网站-地方网站-齐鲁网-图片
        'http://yx.iqilu.com/yxl/': 4791,  # 网站-地方网站-齐鲁网-图片-影像力
        'http://yx.iqilu.com/yxql/': 4792,  # 网站-地方网站-齐鲁网-图片-映象齐鲁
        'http://yx.iqilu.com/rec/': 4794,  # 网站-地方网站-齐鲁网-图片-在现场
        'http://yx.iqilu.com/spec/': 4795,  # 网站-地方网站-齐鲁网-图片-探索非遗
    }

    rules = (
        # ent.iqilu.com/film/news/2019/0902/4341906.shtml
        # http://ppsd.iqilu.com/ywdt/20190604/4284858.shtml

        # http://news.iqilu.com/guoji/list_11_3.shtml todo 第3页有当天新闻
        # http://yx.iqilu.com/2019/0830/4340892.shtml#1 图集parse_item_4
        # http://yx.iqilu.com/2019/0906/4344264.shtml#1 图集parse_item_4
        Rule(LinkExtractor(allow=(r'iqilu.com.*?/%s\d{2}/\d+.s?htm' % datetime.today().strftime('%Y%m'),),
                           deny=('v.iqilu.com/', 'sd.iqilu.com/share', 'bbs.iqilu.com')
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'iqilu.com.*?/%s\d{2}/\d+.s?htm' % datetime.today().strftime('%Y/%m'),),
                           deny=('v.iqilu.com/', 'sd.iqilu.com/share', 'bbs.iqilu.com')
                           ),
             callback='parse_item', follow=False),
        # http://v.iqilu.com/shpd/rmxf/2019/0902/4713715.html 有视频
        # http://v.iqilu.com/live/yspd/?spm=zm5094-001.0.0.1.HclaC1 排除直播
        Rule(LinkExtractor(allow=(r'v.iqilu.com.*?/%s\d{2}/\d+.htm' % datetime.today().strftime('%Y/%m'),),
                           ),
             callback='parse_item_2', follow=False),

        # http://sd.iqilu.com/share/article/5895533.html m站新闻
        Rule(LinkExtractor(allow=(r'sd.iqilu.com/share/article/\d+.htm',),
                           ),
             callback='parse_item_3', follow=False),

        Rule(LinkExtractor(allow=(r'iqilu.com.*?\d+.s?htm',),
                           deny=(r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/', 'bbs.iqilu.com')
                           ),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        # http://news.iqilu.com/shandong/yaowen/2019/0602/4283022.shtml 有视频
        xp = response.xpath
        try:
            title = xp('//h1/text()').extract_first() or self.get_page_title(response).split('_')[0]
            pubtime = xp("//div[@class='info']/p[@class='time']/text()").extract()[0]
            content_div = xp("//div[@class='article-main']/p")
            origin_name = xp("//p[@class='resource']/span/text()").extract_first("")
            content, media, videos, _ = self.content_clean(content_div, need_video=True,
                                                           kill_xpaths="//p[@class='contact']")
        except:
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

    def parse_item_2(self, response):
        xp = response.xpath
        try:
            title = xp('//h1/text()').extract_first() or self.get_page_title(response).split('_')[0]
            pubtime = title[:8]
            video_url = xp('//*[@id="copy_mp4text"]/@value or //input[@id="playerId"]/@url').extract()[0]
            content = '<p>#{{1}}#</p><p>%s</p>' % title
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media={},
            videos={'1': {'src': video_url}}
        )

    def parse_item_3(self, response):
        # http://sd.iqilu.com/share/article/5895533.html m站新闻
        xp = response.xpath
        try:
            title = xp("//h1/text()").extract_first() or \
                    self.get_page_title(response).split('-')[0]
            pubtime = xp("//span[@class='time']/text()").extract_first()
            content_div = xp("//div[@class='article_body']")
            origin_name = xp("//span[@class='source']/text()").extract_first("")
            content, media, videos, _ = self.content_clean(content_div, need_video=True,
                                                           kill_xpaths="//p[@class='contact']")
        except:
            return self.produce_debugitem(response, 'xpath error')

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
        # http://yx.iqilu.com/2019/0906/4344264.shtml#1
        xp = response.xpath
        try:
            title = xp("//div[@class='title-main']/h2/text()").extract_first() or \
                    self.get_page_title(response).split('_')[0]
            pubtime = xp("//span[@class='time']/text()").extract()[0]
            content_div = xp('//div[@class="slide-nav clearfix"]')
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, 'xpath error')

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media,
        )
