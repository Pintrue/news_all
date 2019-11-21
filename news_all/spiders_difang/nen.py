#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/2 12:37
# @Author  : wjq
# @File    : nen.py

from copy import deepcopy
from datetime import datetime
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from news_all.tools.html_clean import NewsBaseParser, img_fn
from news_all.tools.time_translater import Pubtime
import re


img_pattern = re.compile(r'''<img (?:src=['"](?P<src>.*?)['"])?(?: data-original=['"](?P<ori>.*?)['"])?.*?>''')


class NenParser(NewsBaseParser):
    """东北新闻网  图片链接获取data-original优先于src"""

    def image_clean(self, content, img_re=None):
        fr = re.finditer(img_pattern, content)
        media = {}
        new_content = ''

        for i, j in enumerate(fr):
            media.setdefault("images", {})
            st = content.find(j.group())
            end = st + len(j.group())
            new_content += content[:st] + '<p>${{%s}}$</p>' % (i + 1)
            content = content[end:]
            imgurl = j.group('ori') if j.group('ori') else j.group('src')
            media['images'][str(i + 1)] = {"src": img_fn(imgurl)}

        new_content += content
        new_content.replace('$$', '$<br>$')  # 连续2图片加换行
        return new_content, media


class NenSpider(NewsRCSpider):
    """东北新闻网"""
    name = 'nen'
    parser = NenParser()
    mystart_urls = {
        'http://www.nen.com.cn': 4796,  # 网站-地方网站-东北新闻网
        'http://news.nen.com.cn': 4798,  # 网站-地方网站-东北新闻网-新闻-首页

        'http://finance.nen.com.cn': 4815,  # 网站-地方网站-东北新闻网-财经
        'http://finance.nen.com.cn/cjycjjln/index.shtml': 4817,  # 网站-地方网站-东北新闻网-财经-快讯
        'http://finance.nen.com.cn/cj_top_yw1_new/index.shtml': 4819,  # 网站-地方网站-东北新闻网-财经-要闻
        'http://finance.nen.com.cn/cj_cj_lncj_new/index.shtml': 4821,  # 网站-地方网站-东北新闻网-财经-辽宁
        'http://finance.nen.com.cn/xfsh/index.shtml': 4822,  # 网站-地方网站-东北新闻网-财经-消费生活
        'http://finance.nen.com.cn/qyzx/index.shtml': 4824,  # 网站-地方网站-东北新闻网-财经-企业
        'http://finance.nen.com.cn/cj_cj_bank/index.shtml': 4826,  # 网站-地方网站-东北新闻网-财经-银行
        'http://finance.nen.com.cn/cj_cj_bxzq/index.shtml': 4827,  # 网站-地方网站-东北新闻网-财经-保险
        'http://tech.nen.com.cn': 4828,  # 网站-地方网站-东北新闻网-科技
        'http://tech.nen.com.cn/kjywx/index.shtml': 4829,  # 网站-地方网站-东北新闻网-科技-科技要闻
        'http://tech.nen.com.cn/kjln/index.shtml': 4848,  # 网站-地方网站-东北新闻网-科技-科技辽宁
        'http://tech.nen.com.cn/kqfc/index.shtml': 4851,  # 网站-地方网站-东北新闻网-科技-科企风采
        'http://tech.nen.com.cn/kjxx/index.shtml': 4853,  # 网站-地方网站-东北新闻网-科技-创新政策
        'http://tech.nen.com.cn/smtx/index.shtml': 4855,  # 网站-地方网站-东北新闻网-科技-数码通讯
        'http://tech.nen.com.cn/hlw/index.shtml': 4857,  # 网站-地方网站-东北新闻网-科技-互联网
        'http://tech.nen.com.cn/kyx/index.shtml': 4858,  # 网站-地方网站-东北新闻网-科技-科研秀
        'http://tech.nen.com.cn/kps/index.shtml': 4860,  # 网站-地方网站-东北新闻网-科技-科普说
        'http://tech.nen.com.cn/qycx/index.shtml': 4862,  # 网站-地方网站-东北新闻网-科技-区域创新
        'http://tech.nen.com.cn/kjjr/index.shtml': 4864,  # 网站-地方网站-东北新闻网-科技-科技金融
        'http://tech.nen.com.cn/kyys/index.shtml': 4866,  # 网站-地方网站-东北新闻网-科技-科研院所
        'http://tech.nen.com.cn/kjyq/index.shtml': 4867,  # 网站-地方网站-东北新闻网-科技-科技园区
        'http://tech.nen.com.cn/ysfc/index.shtml': 4869,  # 网站-地方网站-东北新闻网-科技-科报辽宁
        'http://tech.nen.com.cn/kts/index.shtml': 4871,  # 网站-地方网站-东北新闻网-科技-科探索
        'http://tech.nen.com.cn/cyj/index.shtml': 4873,  # 网站-地方网站-东北新闻网-科技-创业记
        'http://tech.nen.com.cn/rgzn/index.shtml': 4874,  # 网站-地方网站-东北新闻网-科技-人工智能
        'http://news.nen.com.cn/gngjnew/index.shtml': 4888,  # 网站-地方网站-东北新闻网-看天下
        'http://news.nen.com.cn/gngjnew/gnnew/index.shtml': 4889,  # 网站-地方网站-东北新闻网-看天下-国内新闻
        'http://news.nen.com.cn/gngjnew/gjnew/index.shtml': 4891,  # 网站-地方网站-东北新闻网-看天下-国际新闻
        'http://news.nen.com.cn/gngjnew/jsywnew/index.shtml': 4893,  # 网站-地方网站-东北新闻网-看天下-即时要闻
        'http://news.nen.com.cn/gngjnew/kxnew/index.shtml': 4896,  # 网站-地方网站-东北新闻网-看天下-科学探索
        'http://news.nen.com.cn/gngjnew/shnew/index.shtml': 4898,  # 网站-地方网站-东北新闻网-看天下-史海钩沉
        'http://news.nen.com.cn/gngjnew/shehuinew/index.shtml': 4920,  # 网站-地方网站-东北新闻网-看天下-社会长镜头
        'http://news.nen.com.cn/gngjnew/txnew/index.shtml': 4923,  # 网站-地方网站-东北新闻网-看天下-图行天下
        'http://news.nen.com.cn/gngjnew/whnew/index.shtml': 4930,  # 网站-地方网站-东北新闻网-看天下-五花八门
        'http://dyxc.nen.com.cn': 4931,  # 网站-地方网站-东北新闻网-辽沈一线
        'http://dyxc.nen.com.cn/hdishui/': 4932,  # 网站-地方网站-东北新闻网-辽沈一线-辽沈要闻
        'http://dyxc.nen.com.cn/zwzs/': 4935,  # 网站-地方网站-东北新闻网-辽沈一线-政务之声
        'http://dyxc.nen.com.cn/jbft/': 4956,  # 网站-地方网站-东北新闻网-辽沈一线-嘉宾访谈
        'http://dyxc.nen.com.cn/qmjz/': 4959,  # 网站-地方网站-东北新闻网-辽沈一线-全民记者
        'http://dyxc.nen.com.cn/jzdc/': 4965,  # 网站-地方网站-东北新闻网-辽沈一线-独立调查
        'http://wenyi.nen.com.cn': 4967,  # 网站-地方网站-东北新闻网-文艺
        'http://wenyi.nen.com.cn/wydt/index.shtml': 4969,  # 网站-地方网站-东北新闻网-文艺-文艺动态
        'http://wenyi.nen.com.cn/wypl/index.shtml': 4976,  # 网站-地方网站-东北新闻网-文艺-文艺评论
        'http://wenyi.nen.com.cn/wymj/index.shtml': 4980,  # 网站-地方网站-东北新闻网-文艺-文艺名家
        'http://wenyi.nen.com.cn/yczx/index.shtml': 4982,  # 网站-地方网站-东北新闻网-文艺-演出资讯
        'http://wenyi.nen.com.cn/pxb/index.shtml': 4989,  # 网站-地方网站-东北新闻网-文艺-校园文艺
        'http://society.nen.com.cn': 4996,  # 网站-地方网站-东北新闻网-社会
        'http://society.nen.com.cn/shehui_shwxgx_new/': 4999,  # 网站-地方网站-东北新闻网-社会-社会万象
        'http://society.nen.com.cn/shehui_aqbg_new/': 5000,  # 网站-地方网站-东北新闻网-社会-法治聚焦
        'http://society.nen.com.cn/shtxpicgx_new/': 5002,  # 网站-地方网站-东北新闻网-社会-奇闻趣事
        'http://society.nen.com.cn/shehui_tpgs_new/': 5004,  # 网站-地方网站-东北新闻网-社会-图片故事
        'http://society.nen.com.cn/shehui_ssx_new/': 5005,  # 网站-地方网站-东北新闻网-社会-时尚秀
        'http://society.nen.com.cn/shry/': 5007,  # 网站-地方网站-东北新闻网-社会-社会热议
        'http://society.nen.com.cn/shshqq_new/': 5008,  # 网站-地方网站-东北新闻网-社会-生活情趣
        'http://jiankang.nen.com.cn': 5010,  # 网站-地方网站-东北新闻网-健康
        'http://jiankang.nen.com.cn/xinwen/index.shtml': 5012,  # 网站-地方网站-东北新闻网-健康-新闻
        'http://jiankang.nen.com.cn/jkzx/index.shtml': 5013,  # 网站-地方网站-东北新闻网-健康-资讯
        'http://jiankang.nen.com.cn/yyjk/index.shtml': 5015,  # 网站-地方网站-东北新闻网-健康-营养
        'http://jiankang.nen.com.cn/qwfb/index.shtml': 5016,  # 网站-地方网站-东北新闻网-健康-权威发布
        'http://jiankang.nen.com.cn/bgt/index.shtml': 5018,  # 网站-地方网站-东北新闻网-健康-曝光台
        'http://jiankang.nen.com.cn/ysbj/index.shtml': 5020,  # 网站-地方网站-东北新闻网-健康-养生保健
        'http://liaoning.nen.com.cn/szyw_new/': 5022,  # 网站-地方网站-东北新闻网-辽宁-时政要闻
        'http://liaoning.nen.com.cn/zwren_new/': 5024,  # 网站-地方网站-东北新闻网-辽宁-权威发布
        'http://liaoning.nen.com.cn/dslife_new/': 5026,  # 网站-地方网站-东北新闻网-辽宁-生活服务
        'http://liaoning.nen.com.cn/jjgc/': 5028,  # 网站-地方网站-东北新闻网-辽宁-经济观察
        'http://liaoning.nen.com.cn/kjww_new/': 5032,  # 网站-地方网站-东北新闻网-辽宁-科教卫生
        'http://liaoning.nen.com.cn/whyl/': 5033,  # 网站-地方网站-东北新闻网-辽宁-文化娱乐
        'http://liaoning.nen.com.cn/shfaz_new/': 5035,  # 网站-地方网站-东北新闻网-辽宁-社会万象
        'http://liaoning.nen.com.cn/scjs/': 5037,  # 网站-地方网站-东北新闻网-辽宁-城市建设
        'http://liaoning.nen.com.cn/lnphotonew_new/': 5039,  # 网站-地方网站-东北新闻网-辽宁-辽宁图汇
        'http://liaoning.nen.com.cn/lndangan_new/': 5041,  # 网站-地方网站-东北新闻网-辽宁-辽宁档案
        'http://video.nen.com.cn/xwlb/': 5043,  # 网站-地方网站-东北新闻网-视频-新闻联播
        'http://video.nen.com.cn/lnxw/': 5044,  # 网站-地方网站-东北新闻网-视频-辽宁新闻
        'http://sports.nen.com.cn': 5046,  # 网站-地方网站-东北新闻网-体育-首页
        'http://sports.nen.com.cn/liaoningtitan/index.shtml': 5048,  # 网站-地方网站-东北新闻网-体育-辽宁体坛
        'http://sports.nen.com.cn/wordfootball_new/index.shtml': 5049,  # 网站-地方网站-东北新闻网-体育-国际足坛
        'http://sports.nen.com.cn/guoneifatball_new/index.shtml': 5051,  # 网站-地方网站-东北新闻网-体育-国内足坛
        'http://sports.nen.com.cn/cbazhuqiang/index.shtml': 5052,  # 网站-地方网站-东北新闻网-体育-CBA
        'http://sports.nen.com.cn/nba_new/index.shtml': 5055,  # 网站-地方网站-东北新闻网-体育-NBA
        'http://sports.nen.com.cn/zhonghe_new/index.shtml': 5057,  # 网站-地方网站-东北新闻网-体育-综合体育
        'http://ms.nen.com.cn': 5059,  # 网站-地方网站-东北新闻网-民生
        'http://ms.nen.com.cn/xwzz/index.shtml': 5060,  # 网站-地方网站-东北新闻网-民生-民生新闻
        'http://ms.nen.com.cn/zwfb/index.shtml': 5062,  # 网站-地方网站-东北新闻网-民生-政务发布
        'http://ms.nen.com.cn/bmfw/index.shtml': 5064,  # 网站-地方网站-东北新闻网-民生-便民服务
        'http://xq.nen.com.cn/xianqu-jiaodian_new/index.shtml': 5065,  # 网站-地方网站-东北新闻网-县区-焦点新闻
        'http://xq.nen.com.cn/dishikandian/index.shtml': 5067,  # 网站-地方网站-东北新闻网-县区-地方看点
        'http://xq.nen.com.cn/xianqu-dongtai_new/index.shtml': 5069,  # 网站-地方网站-东北新闻网-县区-县区动态
        'http://auto.nen.com.cn/news/dujia/': 5071,  # 网站-地方网站-东北新闻网-汽车-最新
        'http://auto.nen.com.cn/news/letters/': 5072,  # 网站-地方网站-东北新闻网-汽车-快报
        'http://auto.nen.com.cn/news/35/1/': 5074,  # 网站-地方网站-东北新闻网-汽车-新车资讯
        'http://auto.nen.com.cn/news/38/1/': 5103,  # 网站-地方网站-东北新闻网-汽车-国内新闻
        'http://auto.nen.com.cn/news/39/1/': 5104,  # 网站-地方网站-东北新闻网-汽车-海外速递
        'http://auto.nen.com.cn/news/15/1/': 5106,  # 网站-地方网站-东北新闻网-汽车-热门SUV
        'http://auto.nen.com.cn/news/43/1/': 5107,  # 网站-地方网站-东北新闻网-汽车-国产车测试
        'http://auto.nen.com.cn/news/46/1/': 5108,  # 网站-地方网站-东北新闻网-汽车-进口车测试
        'http://auto.nen.com.cn/news/2393/1/': 5109,  # 网站-地方网站-东北新闻网-汽车-购车手册
        'http://auto.nen.com.cn/news/2392/1/': 5110,  # 网站-地方网站-东北新闻网-汽车-新老对比
        'http://auto.nen.com.cn/news/9/1/': 5111,  # 网站-地方网站-东北新闻网-汽车-车型对比
        'http://auto.nen.com.cn/news/2417/1/': 5112,  # 网站-地方网站-东北新闻网-汽车-新车实拍
        'http://auto.nen.com.cn/photo_logo/': 5113,  # 网站-地方网站-东北新闻网-汽车-图片
        'http://auto.nen.com.cn/news/29/1/': 5114,  # 网站-地方网站-东北新闻网-汽车-车辆改装
        'http://auto.nen.com.cn/news/32/1/': 5115,  # 网站-地方网站-东北新闻网-汽车-用车指南
        'http://house.nen.com.cn': 5116,  # 网站-地方网站-东北新闻网-房产-首页
        'http://house.nen.com.cn/yclm/index.shtml': 5117,  # 网站-地方网站-东北新闻网-房产-原创栏目
        'http://house.nen.com.cn/fcyw/index.shtml': 5118,  # 网站-地方网站-东北新闻网-房产-房产要闻
        'http://house.nen.com.cn/lszj/index.shtml': 5119,  # 网站-地方网站-东北新闻网-房产-楼市直击
        'http://house.nen.com.cn/lsdc/index.shtml': 5120,  # 网站-地方网站-东北新闻网-房产-楼市调查
        'http://house.nen.com.cn/gddh/index.shtml': 5121,  # 网站-地方网站-东北新闻网-房产-高端对话
        'http://house.nen.com.cn/ppfq/index.shtml': 5123,  # 网站-地方网站-东北新闻网-房产-品牌房企
        'http://home.nen.com.cn': 5124,  # 网站-地方网站-东北新闻网-家居-首页
        'http://home.nen.com.cn/jjpd5/index.shtml': 5125,  # 网站-地方网站-东北新闻网-家居-家居维权
        'http://home.nen.com.cn/jjpd3/index.shtml': 5126,  # 网站-地方网站-东北新闻网-家居-消费陷阱
        'http://home.nen.com.cn/zxsj/index.shtml': 5127,  # 网站-地方网站-东北新闻网-家居-装修设计
        'http://home.nen.com.cn/jjpd9/index.shtml': 5128,  # 网站-地方网站-东北新闻网-家居-行业聚焦
        'http://edu.nen.com.cn': 5129,  # 网站-地方网站-东北新闻网-教育-首页
        'http://edu.nen.com.cn/jiaoyuyaowen/index.shtml': 5130,  # 网站-地方网站-东北新闻网-教育-教育要闻
        'http://edu.nen.com.cn/edu_zt/index.shtml': 5131,  # 网站-地方网站-东北新闻网-教育-明星教师
        'http://edu.nen.com.cn/baoguangtai/index.shtml': 5132,  # 网站-地方网站-东北新闻网-教育-曝光台
        'http://edu.nen.com.cn/xinwenzhongxin/xqjy/index.shtml': 5133,  # 网站-地方网站-东北新闻网-教育-学前教育
        'http://edu.nen.com.cn/xinwenzhongxin/gx/index.shtml': 5134,  # 网站-地方网站-东北新闻网-教育-高校
        'http://edu.nen.com.cn/xinwenzhongxin/zxx/index.shtml': 5135,  # 网站-地方网站-东北新闻网-教育-中小学
        'http://edu.nen.com.cn/kaoshizhongxin/gwyks/index.shtml': 5137,  # 网站-地方网站-东北新闻网-教育-公务员考试
        'http://edu.nen.com.cn/kaoshizhongxin/gk/index.shtml': 5138,  # 网站-地方网站-东北新闻网-教育-报考指南
        'http://edu.nen.com.cn/kaoshizhongxin/ky/index.shtml': 5139,  # 网站-地方网站-东北新闻网-教育-考研
        'http://edu.nen.com.cn/kaoshizhongxin/zk/index.shtml': 5140,  # 网站-地方网站-东北新闻网-教育-中考
        'http://in.nen.com.cn': 5141,  # 网站-地方网站-东北新闻网-时尚生活-首页
        'http://youxi.nen.com.cn': 5142,  # 网站-地方网站-东北新闻网-游戏-首页
        'http://youxi.nen.com.cn/wangyou/index.shtml': 5143,  # 网站-地方网站-东北新闻网-游戏-网游
        'http://youxi.nen.com.cn/dj/index.shtml': 5144,  # 网站-地方网站-东北新闻网-游戏-单机
        'http://youxi.nen.com.cn/sy/index.shtml': 5145,  # 网站-地方网站-东北新闻网-游戏-手游

    }

    rules = (
        # http://video.nen.com.cn/system/2019/09/09/020924499.shtml 视频
        Rule(LinkExtractor(
            allow=(r'video.nen.com.cn/system/%s/\d{2}/\d+.s?htm' % datetime.today().strftime('%Y/%m'),),
        ),
            callback='parse_item_2', follow=False),

        # http://auto.nen.com.cn/news/storys_136073.html
        Rule(LinkExtractor(
            allow=(r'auto.nen.com.cn/news/storys_\d+.htm'),
        ),
            callback='parse_item_3', follow=False),
        # http://www.nen.com.cn/xxjj/system/2019/09/04/020921960.shtml
        # http://liaoning.nen.com.cn/system/2019/09/09/020924240.shtml
        # http://news.nen.com.cn/system/2019/08/13/020909618.shtml
        Rule(LinkExtractor(
            allow=(r'nen.com.cn.*?system/%s/\d{2}/\d+.s?htm' % datetime.today().strftime('%Y/%m'),
                   ),
        ),
            callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'nen.com.cn.*?\d+.s?htm',), deny=(r'/201[0-8]', r'/20190[1-9]/', 'bbs.nen.com.cn/')
                           ),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//div[contains(@class,"text_title")]/h1/text()').extract_first() or \
                    self.get_page_title(response).split('-')[0]
            # 防止多个相同tag class
            pubtime = Pubtime(
                xp('//div[@class="fl" or @class="contenttime"][re:match(text(), "\d{2,}")]/text()').extract_first('')[
                :20] or xp(
                    '//h2[re:match(text(), "\d{2,}")]/text()').extract_first('')[:20])
            content_div = xp('//div[@id="rwb_zw"]/span') or xp(
                '//div[@id="rwb_zw"]/ul/p') or xp('//div[@class="contentcon"]/p') or xp(
                '//div[@class="clearb con_nr"]') or xp('//article[@id="mp-editor"]') or xp('//div[@id="rwb_zw"]')
            ogs = xp('//div[@class="fl"]/text()').re('来源：\w{3,}')
            origin_name = ogs[0] if ogs else ""
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

    def parse_item_2(self, response):
        # http://video.nen.com.cn/system/2019/09/09/020924499.shtml
        xp = response.xpath
        try:
            title = xp('//div[contains(@class,"text_title")]/h1/text()').extract_first() or \
                    self.get_page_title(response).split('-')[0]
            pubtime = Pubtime(xp('//div[@class="fl"]/text()').extract_first(''))

            video_url = \
                xp('//script[contains(text(),"var flashvars")]/text()').re('http://www.nen.com.cn/video/.*?\.mp4')[0]
            content = '<p>#{{1}}#</p>'
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
        # http://auto.nen.com.cn/news/storys_136403.html
        xp = response.xpath
        try:
            title = xp('//div[@class="ina_news_text"]/h1/text()').extract_first() or \
                    self.get_page_title(response).split('-')[0]

            pubtime = xp('//span[@class="ina_data"]/text()').extract()[0]
            content_div = xp('//div[contains(@class,"ina_content")]')
            origin_name = xp('//span[@class="ina_source"]/a/text()').extract_first('')
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )


class NenSpnewsSpider(NenSpider):
    """东北新闻网 时评"""
    name = "nen_spnews"
    mystart_urls = {
        'http://news.nen.com.cn/jinhushiping_new/index.shtml': 4800,  # 网站-地方网站-东北新闻网-金虎时评
        'http://news.nen.com.cn/jinhushiping_new/zhenfengxiangdui/index.shtml': 4802,  # 网站-地方网站-东北新闻网-金虎时评-针锋相对
        'http://news.nen.com.cn/jinhushiping_new/jhshiping-tuijian_new/': 4804,  # 网站-地方网站-东北新闻网-金虎时评-聚焦深度
        'http://news.nen.com.cn/jinhushiping_new/jhshiping-mingjiaminglan_new/': 4805,  # 网站-地方网站-东北新闻网-金虎时评-名家名栏
        'http://news.nen.com.cn/jinhushiping_new/jhshiping-xiaopangkailao_new/index.shtml': 4810,
        # 网站-地方网站-东北新闻网-金虎时评-金虎微评
        'http://news.nen.com.cn/jinhushiping_new/jhshiping-hualihuawai_new/': 4811,  # 网站-地方网站-东北新闻网-金虎时评-话里画外
        'http://news.nen.com.cn/jinhushiping_new/jhspyswj_new/': 4813,  # 网站-地方网站-东北新闻网-金虎时评-以史为鉴
    }

    rules = (
        # http://news.nen.com.cn/cms_udf/2019/0906/index.shtml
        # http://news.nen.com.cn/cms_udf/2019/gtbwmxw/index.shtml
        Rule(LinkExtractor(
            allow=(r'news.nen.com.cn/cms_udf/%s\d{2}/index.s?htm' % datetime.today().strftime('%Y/%m'),
                   r'news.nen.com.cn/cms_udf/%s/[a-z]+/index.s?htm' % datetime.today().strftime('%Y'),
                   ),
        ),
            callback='parse_list', follow=False),

        # http://news.nen.com.cn/system/2019/09/10/020925171.shtml
        Rule(LinkExtractor(
            allow=(r'nen.com.cn.*?system/%s/\d{2}/\d+.s?htm' % datetime.today().strftime('%Y/%m'),
                   ),
        ),
            callback='parse_item', follow=False),

        Rule(LinkExtractor(allow=(r'nen.com.cn.*?.s?htm',), deny=(r'/201[0-8]', r'/20190[1-9]/', 'bbs.nen.com.cn/')
                           ),
             process_request=otherurl_meta, follow=False),
    )
    custom_settings = {
        'DEPTH_LIMIT': 2,  # 若翻页则需要设置深度为0
        "SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % NenSpider.name,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))  # 禁止重定向
    }

    def parse_list(self, response):
        xp = response.xpath
        # http://news.nen.com.cn/system/2018/01/29/020341947.shtml
        news_a = xp('//a[re:match(@href, "news.nen.com.cn/system/%s/\d{2}/\d+.s?htm")]'%datetime.today().strftime('%Y/%m'))
        for next_a in news_a:
            yield response.follow(
                next_a, callback=self.parse_item,
                meta={'source_id': response.meta.get('source_id'),
                      'start_url_time': response.meta.get('start_url_time'),
                      'schedule_time': response.meta.get('schedule_time')
                      }
            )

    def parse_item(self, response):
        return super(NenSpnewsSpider, self).parse_item(response)