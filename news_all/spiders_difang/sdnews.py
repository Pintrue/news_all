#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/4 11:08
# @Author  : mez
# @File    : sdcn.py


from datetime import datetime
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from news_all.tools.time_translater import Pubtime


class SDspider(NewsRCSpider):
    """鲁网 中国山东网"""
    name = 'sdnews'
    mystart_urls = {
        'http://www.sdnews.com.cn': 4578,  # 网站-地方网站-鲁网
        'http://news.sdnews.com.cn/m/': 4579,  # 网站-地方网站-鲁网-新闻
        'http://www.sdnews.com.cn/m/': 4580,  # 网站-地方网站-鲁网-头条
        'http://sd.sdnews.com.cn/m/': 4581,  # 网站-地方网站-鲁网-山东
        'http://f.sdnews.com.cn/m/': 4582,  # 网站-地方网站-鲁网-财经
        'http://lushang.sdnews.com.cn/xz/m/': 4583,  # 网站-地方网站-鲁网-特色小镇
        'http://gov.sdnews.com.cn/m/': 4584,  # 网站-地方网站-鲁网-政务
        'http://news.sdnews.com.cn/lzpd/': 4585,  # 网站-地方网站-鲁网-廉政
        'http://news.sdnews.com.cn/lzpd/lzyw/': 4586,  # 网站-地方网站-鲁网-廉政-要闻动态
        'http://news.sdnews.com.cn/lzpd/tslz/': 4587,  # 网站-地方网站-鲁网-廉政-图说廉政
        'http://news.sdnews.com.cn/lzpd/zyjs/': 4588,  # 网站-地方网站-鲁网-廉政-中央精神
        'http://news.sdnews.com.cn/lzpd/dflz/': 4589,  # 网站-地方网站-鲁网-廉政-地方廉政
        'http://news.sdnews.com.cn/lzpd/lzsp/': 4590,  # 网站-地方网站-鲁网-廉政-廉政时评
        'http://news.sdnews.com.cn/lzpd/qlqf/': 4591,  # 网站-地方网站-鲁网-廉政-齐鲁清风
        'http://news.sdnews.com.cn/lzpd/2014lzsp/': 4592,  # 网站-地方网站-鲁网-廉政-廉政视频
        'http://news.sdnews.com.cn/lzpd/dhpy/': 4593,  # 网站-地方网站-鲁网-廉政-打虎拍蝇
        'http://news.sdnews.com.cn/lzpd/lzkm/': 4594,  # 网站-地方网站-鲁网-廉政-廉政楷模
        'http://news.sdnews.com.cn/lzpd/jzcm/': 4595,  # 网站-地方网站-鲁网-廉政-警钟长鸣
        'http://news.sdnews.com.cn/lzpd/lzzs/': 4596,  # 网站-地方网站-鲁网-廉政-廉政知识
        'http://news.sdnews.com.cn/lzpd/lzwx/': 4597,  # 网站-地方网站-鲁网-廉政-廉政文学
        'http://news.sdnews.com.cn/lzpd/lzmh/': 4599,  # 网站-地方网站-鲁网-廉政-廉政漫画
        'http://news.sdnews.com.cn/lzpd/lzgy/': 4601,  # 网站-地方网站-鲁网-廉政-廉政格言
        'http://news.sdnews.com.cn/lzpd/shjj/': 4602,  # 网站-地方网站-鲁网-廉政-史海借鉴
        'http://news.sdnews.com.cn/lzpd/lzgq/': 4603,  # 网站-地方网站-鲁网-廉政-廉政歌曲
        'http://ent.sdnews.com.cn/m/': 4604,  # 网站-地方网站-鲁网-娱乐
        'http://sports.sdnews.com.cn/m/': 4605,  # 网站-地方网站-鲁网-体育
        'http://jy.sdnews.com.cn': 4606,  # 网站-地方网站-鲁网-教育
        'http://jy.sdnews.com.cn/yw/': 4607,  # 网站-地方网站-鲁网-教育-要闻
        'http://jy.sdnews.com.cn/gk/': 4608,  # 网站-地方网站-鲁网-教育-高考
        'http://jy.sdnews.com.cn/jyft/': 4609,  # 网站-地方网站-鲁网-教育-教育访谈
        'http://jy.sdnews.com.cn/jxlw/': 4610,  # 网站-地方网站-鲁网-教育-教学论文
        'http://jy.sdnews.com.cn/xyzx/': 4612,  # 网站-地方网站-鲁网-教育-校园资讯
        'http://fazhi.sdnews.com.cn/m/': 4615,  # 网站-地方网站-鲁网-法制
        'http://pinglun.sdnews.com.cn/m/': 4617,  # 网站-地方网站-鲁网-评论
        'http://video.sdnews.com.cn/m/': 4619,  # 网站-地方网站-鲁网-视频
        'http://gov.sdnews.com.cn/qwfb/': 4622,  # 网站-地方网站-鲁网-权威发布
        'http://gov.sdnews.com.cn/qwfb/cftz/': 4623,  # 网站-地方网站-鲁网-权威发布-采访通知
        'http://gov.sdnews.com.cn/qwfb/fbhsl/': 4625,  # 网站-地方网站-鲁网-权威发布-发布实录
        'http://gov.sdnews.com.cn/qwfb/sdyw/': 4627,  # 网站-地方网站-鲁网-权威发布-山东要闻
        'http://gov.sdnews.com.cn/qwfb/zwxx/': 4626,  # 网站-地方网站-鲁网-权威发布-政务信息
        'http://gov.sdnews.com.cn/qwfb/17sxwfbh/jn/': 4628,  # 网站-地方网站-鲁网-权威发布-17市新闻发布会
        'http://gov.sdnews.com.cn/qwfb/fyrpx/': 4629,  # 网站-地方网站-鲁网-权威发布-发言人培训
        'http://gov.sdnews.com.cn/qwfb/dwjs/': 4630,  # 网站-地方网站-鲁网-权威发布-队伍建设
        'http://gov.sdnews.com.cn/qwfb/llwz/': 4631,  # 网站-地方网站-鲁网-权威发布-理论文章
        'http://sd.sdnews.com.cn/gysd/': 4632,  # 网站-地方网站-鲁网-公益山东
        'http://sd.sdnews.com.cn/gysd/xwjj/': 4634,  # 网站-地方网站-鲁网-公益山东-新闻聚焦
        'http://sd.sdnews.com.cn/gysd/yxd/': 4635,  # 网站-地方网站-鲁网-公益山东-益行动
        'http://sd.sdnews.com.cn/gysd/wll/': 4636,  # 网站-地方网站-鲁网-公益山东-微力量
        'http://f.sdnews.com.cn/ssgsxx/': 4637,  # 网站-地方网站-鲁网-财经-上市公司
        'http://f.sdnews.com.cn/sdcsx/': 4638,  # 网站-地方网站-鲁网-金融-银行
        'http://f.sdnews.com.cn/sypd/xwjj/': 4639,  # 网站-地方网站-鲁网-商业-新闻聚焦
        'http://f.sdnews.com.cn/sypd/ppzs/': 4640,  # 网站-地方网站-鲁网-商业-品牌展示
        'http://f.sdnews.com.cn/sypd/shkx/': 4642,  # 网站-地方网站-鲁网-商业-生活快讯
        'http://f.sdnews.com.cn/sypd/xfwq/': 4643,  # 网站-地方网站-鲁网-商业-消费维权
        'http://f.sdnews.com.cn/sypd/hdtj/': 4644,  # 网站-地方网站-鲁网-商业-活动推荐
        'http://f.sdnews.com.cn/sypd/msmk/': 4646,  # 网站-地方网站-鲁网-商业-美食美客
        'http://f.sdnews.com.cn/fc/': 4648,  # 网站-地方网站-鲁网-房产
        'http://f.sdnews.com.cn/fc/yw/': 4651,  # 网站-地方网站-鲁网-房产-要闻
        'http://f.sdnews.com.cn/fc/lshq/': 4653,  # 网站-地方网站-鲁网-房产-楼市
        'http://f.sdnews.com.cn/fc/dcjr/': 4654,  # 网站-地方网站-鲁网-房产-观点
        'http://f.sdnews.com.cn/fc/pingpan/': 4655,  # 网站-地方网站-鲁网-房产-房企
        'http://f.sdnews.com.cn/fc/kandian/': 4656,  # 网站-地方网站-鲁网-房产-土拍
        'http://f.sdnews.com.cn/fc/lpxx/': 4668,  # 网站-地方网站-鲁网-房产-热搜
        'http://f.sdnews.com.cn/fc/wq/': 4670,  # 网站-地方网站-鲁网-房产-维权
        'http://f.sdnews.com.cn/fc/ch/': 4672,  # 网站-地方网站-鲁网-房产-策划
        'http://f.sdnews.com.cn/ppsd/': 4673,  # 网站-地方网站-鲁网-品牌
        'http://f.sdnews.com.cn/ppsd/yw/': 4674,  # 网站-地方网站-鲁网-品牌-要闻
        'http://f.sdnews.com.cn/ppsd/qy/': 4675,  # 网站-地方网站-鲁网-品牌-企业
        'http://f.sdnews.com.cn/ppsd/zc/': 4676,  # 网站-地方网站-鲁网-品牌-政策
        'http://f.sdnews.com.cn/ppsd/cy/': 4677,  # 网站-地方网站-鲁网-品牌-产业
        'http://f.sdnews.com.cn/ppsd/sd/': 4678,  # 网站-地方网站-鲁网-品牌-深度
        'http://f.sdnews.com.cn/ppsd/fc/': 4679,  # 网站-地方网站-鲁网-品牌-风采
        'http://f.sdnews.com.cn/xsbpd/': 4680,  # 网站-地方网站-鲁网-新三板
        'http://f.sdnews.com.cn/xsbpd/gs/': 4681,  # 网站-地方网站-鲁网-新三板-公司
        'http://f.sdnews.com.cn/xsbpd/rw/': 4682,  # 网站-地方网站-鲁网-新三板-人物
        'http://f.sdnews.com.cn/xsbpd/zc/': 4684,  # 网站-地方网站-鲁网-新三板-政策
        'http://f.sdnews.com.cn/sdgzpd/ywlb/': 4686,  # 网站-地方网站-鲁网-山东国资-要闻联播
        'http://f.sdnews.com.cn/sdgzpd/ssgq/': 4688,  # 网站-地方网站-鲁网-山东国资-省属国企
        'http://f.sdnews.com.cn/sdgzpd/sxgz/': 4690,  # 网站-地方网站-鲁网-山东国资-市县国资
        'http://f.sdnews.com.cn/sdgzpd/gzck/': 4692,  # 网站-地方网站-鲁网-山东国资-国资参考
        'http://f.sdnews.com.cn/sdgzpd/dfdj/': 4694,  # 网站-地方网站-鲁网-山东国资-党风当间
        'http://f.sdnews.com.cn/sdgzpd/zcfg/': 4697,  # 网站-地方网站-鲁网-山东国资-政策法规
        'http://t.sdnews.com.cn': 4699,  # 网站-地方网站-鲁网-文旅
        'http://t.sdnews.com.cn/lyjj/': 4701,  # 网站-地方网站-鲁网-文旅-文旅聚焦
        'http://t.sdnews.com.cn/wh/': 4704,  # 网站-地方网站-鲁网-文旅-文化山东
        'http://t.sdnews.com.cn/lyj/': 4705,  # 网站-地方网站-鲁网-文旅-旅游+
        'http://t.sdnews.com.cn/tbch/': 4707,  # 网站-地方网站-鲁网-文旅-特别策划
        'http://t.sdnews.com.cn/tscp/': 4709,  # 网站-地方网站-鲁网-文旅-山东名品
        'http://t.sdnews.com.cn/lyyq/': 4716,  # 网站-地方网站-鲁网-文旅-文旅舆情
        'http://f.sdnews.com.cn/qcpd/': 4718,  # 网站-地方网站-鲁网-汽车
        'http://f.sdnews.com.cn/qcpd/xfwq/': 4720,  # 网站-地方网站-鲁网-汽车-消费维权
        'http://f.sdnews.com.cn/qcpd/ycbk/': 4721,  # 网站-地方网站-鲁网-汽车-用车百科
        'http://f.sdnews.com.cn/qcpd/xccp/': 4722,  # 网站-地方网站-鲁网-汽车-新车测评
        'http://f.sdnews.com.cn/qcpd/xnyqc/': 4723,  # 网站-地方网站-鲁网-汽车-新能源汽车
        'http://f.sdnews.com.cn/qcpd/qcbj/': 4724,  # 网站-地方网站-鲁网-汽车-汽车百家
        'http://f.sdnews.com.cn/qcpd/ctrw/': 4725,  # 网站-地方网站-鲁网-汽车-车坛人物
        'http://f.sdnews.com.cn/zx/hyxw/': 4726,  # 网站-地方网站-鲁网-直销-行业新闻
        'http://f.sdnews.com.cn/zx/qyxw/': 4727,  # 网站-地方网站-鲁网-直销-企业新闻
        'http://f.sdnews.com.cn/zx/gycs/': 4728,  # 网站-地方网站-鲁网-直销-公益慈善
        'http://9.sdnews.com.cn/jyzx/': 4729,  # 网站-地方网站-鲁网-酒水-酒业资讯
        'http://9.sdnews.com.cn/jygc/': 4730,  # 网站-地方网站-鲁网-酒水-酒业观察
        'http://9.sdnews.com.cn/mjjs/': 4731,  # 网站-地方网站-鲁网-酒水-美酒鉴赏
        'http://9.sdnews.com.cn/jyhd/': 4732,  # 网站-地方网站-鲁网-酒水-酒业活动
        'http://9.sdnews.com.cn/jrjs/': 4733,  # 网站-地方网站-鲁网-酒水-酒人酒事
        'http://ws.sdnews.com.cn/ys/': 4734,  # 网站-地方网站-鲁网-健康-医声医事
        'http://ws.sdnews.com.cn/xw/': 4735,  # 网站-地方网站-鲁网-健康-医院点击
        'http://ws.sdnews.com.cn/ft/': 4736,  # 网站-地方网站-鲁网-健康-特色医讯
        'http://ws.sdnews.com.cn/zx/': 4737,  # 网站-地方网站-鲁网-健康-医美在线
        'http://ws.sdnews.com.cn/jkys/': 4738,  # 网站-地方网站-鲁网-健康-健康养生
        'http://ws.sdnews.com.cn/qyxx/': 4739,  # 网站-地方网站-鲁网-健康-前沿信息
        'http://yishu.sdnews.com.cn/m/': 4740,  # 网站-地方网站-鲁网-艺术
        'http://f.sdnews.com.cn/xczx/rlb/': 4742,  # 网站-地方网站-鲁网-乡村振兴-热力榜
        'http://f.sdnews.com.cn/xczx/kql/': 4745,  # 网站-地方网站-鲁网-乡村振兴-看齐鲁
        'http://f.sdnews.com.cn/xczx/zch/': 4746,  # 网站-地方网站-鲁网-乡村振兴-政策汇
        'http://f.sdnews.com.cn/xczx/djt/': 4748,  # 网站-地方网站-鲁网-乡村振兴-大家谈
        'http://f.sdnews.com.cn/xczx/qly/': 4758,  # 网站-地方网站-鲁网-乡村振兴-千里眼
        'http://f.sdnews.com.cn/xczx/yjy/': 4759,  # 网站-地方网站-鲁网-乡村振兴-研究院
        'http://f.sdnews.com.cn/xczx/qjt/': 4760,  # 网站-地方网站-鲁网-乡村振兴-全镜头
        'http://lushang.sdnews.com.cn/xz/jjxz/': 4762,  # 网站-地方网站-鲁网-特色小镇-前沿信息
        'http://lushang.sdnews.com.cn/xz/qzjq/': 4763,  # 网站-地方网站-鲁网-特色小镇-强镇聚焦
        'http://lushang.sdnews.com.cn/xz/zczx/': 4764,  # 网站-地方网站-鲁网-特色小镇-政策在线

    }
    # LimitatedDaysHoursMinutes = (60, 0, 0)

    rules = (
        # http://sd.sdnews.com.cn/photo/201909/t20190909_2608111.htm
        Rule(LinkExtractor(allow=(r'sdnews.com.cn/photo/%s/t\d{8}_\d+.htm' % datetime.today().strftime('%Y%m'),),
                           ),
             callback='parse_item_3', follow=False),
        # http://lushang.sdnews.com.cn/xz/jjxz/201909/t20190905_2606530.html'
        # http://sports.sdnews.com.cn/gnzq/201909/t20190905_2606439.html
        Rule(LinkExtractor(allow=(r'sdnews.com.cn.*?/%s/t\d{8}_\d+.htm' % datetime.today().strftime('%Y%m'),),
                           ),
             callback='parse_item', follow=False),

        # 防止正则覆盖不全
        Rule(LinkExtractor(allow=(r'sdnews.com.cn.*?\d+.htm',), deny=(r'/201[0-8]', r'/20190[1-9]/', '/index_\d+.htm')
                           ),
             process_request=otherurl_meta, follow=False),
    )

    # todo 视频 http://sd.sdnews.com.cn/yw/201909/t20190903_2605407.htm
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//h1/text()').extract_first() or self.get_page_title(response).split('-')[0]
            pubtime = Pubtime(
                xp("//div[@class='bb info']/span").extract_first() or xp('//div[@class="page"]/span').extract_first()
                or xp('//div[@class="info"]').extract_first())
            content_div = xp("//div[@class='TRS_Editor']")
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True)
        except:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media,
            videos=videos,
        )

    def parse_item_2(self, response):
        # http://sd.sdnews.com.cn/wnsd/201909/t20190903_2605575.html
        xp = response.xpath
        try:
            title = ''.join(xp('//div[@class="TRS_Editor"]//p[1]//text()').extract())
            pubtime = xp('//div[@class="TRS_Editor"]//p[2]/strong/text()').re('\d+月\d+日')[0]

            content_div = xp('//div[@class="TRS_Editor"]//p[position()>1]')
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True)
        except:
            return self.parse_item3(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media,
            videos=videos,
        )

    def parse_item3(self, response):
        # http://sd.sdnews.com.cn/photo/201909/t20190909_2608111.htm
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('-')[0]
            content_div = xp('//p[@class="describe-text">')
            content = self.parser.cleaner.clean_html(content_div)
            pubtime = Pubtime(content[:10])

            media = {'images': {}}
            pics = xp('//script[re:match(text(), "picInfosJson.push")]').re(r'"pic_url"\:"(.*?)"')
            for i, j in enumerate(pics):
                media['images'][str(i + 1)] = {"src": urljoin(response.url, j)}
                t = "<p>${{%s}}$</p>" % (i + 1)
            content = t + content
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media,
        )
