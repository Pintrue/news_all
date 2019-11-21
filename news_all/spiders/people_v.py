# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import isStartUrl_meta
from news_all.spiders.people import PeopleSpider


class PeopleRootSpider(PeopleSpider):
    name = 'root_people'
    mystart_urls = {"http://www.people.cn/": 230, }  # "人民网首页-首屏-时政",
    
    # 头条 滚动 右侧 采集区
    # http://pic.people.com.cn/n1/2019/0213/c1016-30642006.html
    rules = (
        Rule(LinkExtractor(allow=r'people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
                           deny='video',
                           restrict_xpaths=('.//section[@class="w1000 cont_a"]//a',)
                           ),
             callback='parse_item', follow=False),
    )
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeoplePolSpider(PeopleSpider):
    name = 'politics_people'
    mystart_urls = {
        "http://politics.people.com.cn/GB/99014/index.html": 232,
        "http://politics.people.com.cn/GB/1024/index.html": 233,
        "http://politics.people.com.cn/GB/1027/index.html": 234,
        "http://politics.people.com.cn/GB/369059/index.html": 235,
        "http://opinion.people.com.cn/GB/364827/index.html": 236,
        "http://politics.people.com.cn/GB/389979/index.html": 238,
    }
    # http://politics.people.com.cn/n1/2019/0416/c1001-31031619.html
    rules = (Rule(
        LinkExtractor(allow=r'politics.people.com.cn/.*?/%s\d{2}/c\d+-\d+.html' % datetime.today().strftime('%Y/%m'),
                      deny='video'), callback='parse_item',
        follow=False),)
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleOpiSpider(PeopleSpider):
    name = 'opinion_people'
    mystart_urls = {
        "http://opinion.people.com.cn/GB/223228/index.html": 239,
        "http://opinion.people.com.cn/GB/8213/420650/index.html": 240,
        "http://opinion.people.com.cn/GB/364597/index.html": 241,
        "http://opinion.people.com.cn/GB/1036/index.html": 243,
        "http://opinion.people.com.cn/GB/40604/index.html": 244,
        "http://opinion.people.com.cn/GB/159301/index.html": 245,
        "http://opinion.people.com.cn/GB/8213/119388/index.html": 246
    }
    rules = (
        # http://opinion.people.com.cn/n1/2019/0422/c1003-31043351.html
        Rule(LinkExtractor(
            allow=r'opinion.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
            deny='video'), callback='parse_item',
            follow=False),)
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )


class PeopleWorSpider(PeopleSpider):
    name = "world_people"
    mystart_urls = {
        "http://world.people.com.cn/GB/157278/index.html": 248,
        "http://world.people.com.cn/GB/57505/index.html": 249,
        # 首页列表翻页多个http://world.people.com.cn/GB/157278/index4.html
    }
    rules = (
        Rule(LinkExtractor(allow=r'world.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
                           deny='video',
                           restrict_xpaths=("//div[@class='ej_bor']/ul/li/a", "//div[@id='main']/ul/li/i/a")
                           ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(
            allow=(r'world.people.com.cn/GB/157278/index\d+.html', r'world.people.com.cn/GB/57505/index\d+.html'),
            restrict_xpaths=r'//div[@class="ej_page"]/a[text()="下一页"]'),
            follow=True, process_request=isStartUrl_meta))
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleMoneySpider(PeopleSpider):
    name = "money_people"
    mystart_urls = {
        "http://money.people.com.cn/stock/GB/222942/index.html": 250,
        "http://money.people.com.cn/fund/GB/index.html": 251,
        "http://money.people.com.cn/stock/GB/68055/index.html": 252,
        "http://money.people.com.cn/stock/GB/220485/index.html": 253,
        "http://money.people.com.cn/stock/GB/222900/index.html": 254,
        "http://money.people.com.cn/bank/": 255,
        "http://money.people.com.cn/insurance/": 256,
        "http://money.people.com.cn/GB/392426/index.html": 257,
        "http://finance.people.com.cn/fund/": 258,
        "http://money.people.com.cn/GB/397730/index.html": 259,
        "http://money.people.com.cn/GB/67605/index.html": 260,
        "http://ccnews.people.com.cn/GB/142052/index.html": 261,
        "http://finance.people.com.cn/GB/153179/153522/index.html": 262,
        "http://finance.people.com.cn/GB/70846/index.html": 263,
        "http://finance.people.com.cn/GB/1045/index.html": 264,
        "http://finance.people.com.cn/GB/414330/index.html": 265,
    }
    rules = (
        Rule(LinkExtractor(
            allow=r'(?:money|finance|ccnews).people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime(
                '%Y/%m'), deny='video'),
             callback='parse_item',
             follow=False),)
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleTwSpider(PeopleSpider):
    name = "tw_people"
    mystart_urls = {
        "http://tw.people.com.cn/GB/104510/index.html": 266,
        "http://tw.people.com.cn/GB/14811/index.html": 267,
        "http://tw.people.com.cn/GB/14812/14875/index.html": 268
    }
    rules = (
        Rule(LinkExtractor(allow=r'tw.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
                           deny='video',
                           restrict_xpaths="//div[@class='bor']/ul/li/a"), callback='parse_item',
             follow=False),)
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleLeaSpider(PeopleSpider):
    name = "leaders_people"
    mystart_urls = {
        "http://leaders.people.com.cn/GB/70117/index.html": 269,
        "http://leaders.people.com.cn/GB/70118/index.html": 270,
        "http://leaders.people.com.cn/GB/70120/index.html": 271,
    }
    rules = (
        Rule(LinkExtractor(
            allow=r'leaders.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
            deny='video', ), callback='parse_item',
             follow=False),)
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleYdylSpider(PeopleSpider):
    """一带一路"""
    name = "ydyl_people"
    mystart_urls = {
        "http://ydyl.people.com.cn/GB/411947/index.html": 272,
        "http://ydyl.people.com.cn/": 273
    }
    rules = (
        Rule(LinkExtractor(allow=r'ydyl.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
                           deny='video',
                           restrict_xpaths=("//div[@class='fr' or @class='ej_left fl']/ul/li/a",)),
             callback='parse_item',  # 这里都是图集暂不要"//div[@id='box']/ul/li/a"
             follow=False),)
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleMilSpider(PeopleSpider):
    name = "mil_people"
    mystart_urls = {
        "http://military.people.com.cn/GB/172467/index.html": 274
    }
    rules = (
        Rule(LinkExtractor(
            allow=r'military.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
            deny='video', ), callback='parse_item',
             follow=False),)
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleRenSpider(PeopleSpider):
    name = "ren_people"
    mystart_urls = {
        "http://renshi.people.com.cn/": 275
    }
    rules = (
        Rule(
            LinkExtractor(allow=r'renshi.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
                          deny='video', ), callback='parse_item_rs',
            follow=False),)
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    
    def parse_item_rs(self, response):
        # http://renshi.people.com.cn/n1/2019/0306/c139617-30959931.html
        # http://renshi.people.com.cn/n1/2019/0306/c139617-30959931.html
        xp = response.xpath
        try:
            news_div = xp('.//div[contains(@class,"text_con")]')[0]
            content_div = news_div.xpath('//div[@class="show_text"]')[0]
            tail_div = xp('.//div[contains(text(), "责编：")]')[0]
            
            tdiv = news_div.xpath('.//div[@class="text_c"]/h1')[0]
            
            # ['2019年03月08日07:53\xa0\xa0\xa0\xa0来源：', '潍坊日报']
            stexts = xp('.//*[contains(text(),"来源：") or @class="sou"]//text()').extract()
            pubtime = stexts[0].replace("来源：", "").strip()
            ons = re.search('来源：(\w{2,})', stexts[1])
            origin_name = ons.group(1) if ons else stexts[1].strip()
        except:
            return super(PeopleRenSpider, self).parse_item(response)
        
        title = tdiv.xpath('./text()').extract_first('').strip()
        # http://renshi.people.com.cn/n1/2019/0312/c139617-30971573.html kill_xpaths
        content, media, _, _ = self.content_clean(content_div, kill_xpaths=['//*[contains(text(),"相关新闻")]/ancestor::p',
                                                                            '//*[contains(text(),"相关新闻")]/ancestor::p/following-sibling::*'])  # todo 合并写出1个xpath
        
        if "责编：" not in content:
            content += tail_div.extract()
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,

            media=media,
        )


class PeopleTheSpider(PeopleSpider):
    name = "the_people"
    mystart_urls = {
        "http://theory.people.com.cn/": 277,
        "http://theory.people.com.cn/GB/148980/index.html": 280,
        "http://theory.people.com.cn/GB/409497/index.html": 281,
        "http://theory.people.com.cn/GB/409499/": 282,
    }
    rules = (
        Rule(
            LinkExtractor(allow=r'theory.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
                          deny='video',
                          restrict_xpaths=("//div[@class='fr p1_right' or @class='fl']/ul/li/a",)),
            callback='parse_item', follow=False),)
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleLegSpider(PeopleSpider):
    name = "leg_people"
    mystart_urls = {
        "http://legal.people.com.cn/": 283,
        "http://legal.people.com.cn/GB/188502/index.html": 284,
    }
    rules = (
        Rule(LinkExtractor(allow=r'legal.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
                           deny='video',
                           ), callback='parse_item', follow=False),)
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleSocSpider(PeopleSpider):
    name = "soc_people"
    mystart_urls = {
        "http://society.people.com.cn/": 290,
        "http://society.people.com.cn/GB/86800/index.html": 291,
        "http://society.people.com.cn/GB/229589/235996/index.html": 295
    }
    rules = (
        Rule(LinkExtractor(
            allow=r'society.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
            deny='video',
            ), callback='parse_item', follow=False),
        # Rule(LinkExtractor(
        #     allow=(r'society.people.com.cn/index\d+',), ),
        #     follow=True, process_request=isStartUrl_meta)
    )
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleOpiSpider(PeopleSpider):
    """人民时评"""
    name = "opi_people"
    mystart_urls = {
        "http://opinion.people.com.cn/GB/8213/353915/353916/index.html": 296,
    }
    rules = (
        Rule(LinkExtractor(
            allow=r'opinion.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
            deny='video',
            ), callback='parse_item', follow=False),
    )
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleHouSpider(PeopleSpider):
    name = "hou_people"
    mystart_urls = {
        "http://house.people.com.cn/": 297,
        "http://house.people.com.cn/GB/164291/index.html": 96,  # 298,
    }
    rules = (
        Rule(LinkExtractor(allow=r'house.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
                           deny='video',
                           # restrict_xpaths='//td[@class="t11"]/a'
                           ), callback='parse_item', follow=False),
        Rule(LinkExtractor(
            allow=(r'house.people.com.cn/index\d+',),
            restrict_xpaths=r'//div[@class="page_n clearfix"]/a[text()="下一页"]'),
            follow=True, process_request=isStartUrl_meta)
    )
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleCpcRootSpider(PeopleSpider):
    """中国共产党新闻网 首页头条+轮播"""
    name = "cpc_root_people"
    mystart_urls = {
        "http://cpc.people.com.cn/": 308,  # 首页头条+轮播
    }
    rules = (
        Rule(LinkExtractor(allow=r'cpc.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'),
                           deny='video',
                           restrict_xpaths=('//div[@class="mainBoxTop"]', '//div[@class="rcBox"]')
                           ), callback='parse_item', follow=False),
    )
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleDangSpider(PeopleSpider):
    """中国共产党新闻网"""
    name = "dangjian_people"
    mystart_urls = {
        "http://dangjian.people.com.cn/GB/394444/index.html": 311,
        "http://dangjian.people.com.cn/GB/394443/index.html": 313,
        "http://dangjian.people.com.cn/GB/359559/index.html": 314,
        "http://theory.people.com.cn/GB/136457/index.html": 315,
        "http://cpc.people.com.cn/GB/64093/64094/index.html": 316,
    }
    
    rules = (
        Rule(LinkExtractor(
            allow=r'(?:theory|dangjian|cpc).people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime(
                '%Y/%m'), deny='video',
            ), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'cpc.people.com.cn/GB/64093/64094/index\d+', restrict_xpaths=r'//div[@class="page"]/a[text()="下一页"]'
                           ), follow=True, process_request=isStartUrl_meta),
    )
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )


class PeopleFanSpider(PeopleSpider):
    name = "fanfu_people"
    mystart_urls = {
        "http://fanfu.people.com.cn/": 317,
    }
    rules = (
        Rule(LinkExtractor(allow=r'fanfu.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'), deny='video',
                           ), callback='parse_item', follow=False),
        # Rule(LinkExtractor(allow=r'fanfu.people.com.cn/index\d+.html',
        #                    ), follow=True, process_request=isStartUrl_meta),
    )
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    

class PeopleJhSpider(PeopleSpider):
    """习近平系列重要讲话数据库"""
    name = "jh_people"
    mystart_urls = {
        "http://jhsjk.people.cn/result": 321,
        "http://jhsjk.people.cn/result?form=706&else=501": 322,
        "http://jhsjk.people.cn/result?form=701&else=501": 323,
        "http://jhsjk.people.cn/result?form=702&else=501": 324,
        "http://jhsjk.people.cn/result?form=703&else=501": 325,
        "http://jhsjk.people.cn/result?form=704&else=501": 326,
        "http://jhsjk.people.cn/result?form=705&else=501": 327,
        "http://jhsjk.people.cn/result?form=707&else=501": 328,
        "http://jhsjk.people.cn/result?type=101": 329,
        "http://jhsjk.people.cn/result?type=102": 330,
        "http://jhsjk.people.cn/result?type=103": 331,
        "http://jhsjk.people.cn/result?type=104": 332,
        "http://jhsjk.people.cn/result?type=105": 333,
        "http://jhsjk.people.cn/result?type=106": 334,
        "http://jhsjk.people.cn/result?type=107": 335,
        "http://jhsjk.people.cn/result?type=108": 336,
        "http://jhsjk.people.cn/result/1?area=402": 337,
        "http://jhsjk.people.cn/result/1?area=401": 210,
    }
    # http://jhsjk.people.cn/article/28751570
    rules = (
        Rule(LinkExtractor(allow=r'jhsjk.people.cn/article/\d{8,}$', deny='video',
                           # restrict_xpaths=("//div[@class='fr p1_right' or @class='fl']/ul/li/a",)
                           ), callback='parse_item_jhsjk', follow=False),
        # Rule(LinkExtractor(allow=r'jhsjk.people.cn/result/\d+',
        #                    ), follow=True, process_request=isStartUrl_meta),
    )
    
    #  http://jhsjk.people.cn/result/7?type=108
    #  http://jhsjk.people.cn/result/2?form=701&else=501
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )
    
    def parse_item_jhsjk(self, response):
        
        
        try:
            # h2_div = response.xpath('//h2')[0]
            h1_div = response.xpath('//h1')[0]  # 主标题
            h3_div = response.xpath('//h3')[0]  # 副标题
            
            source_div = response.xpath('.//*[contains(text(), "来源：")]')[0]
            source_text = source_div.xpath('.//text()').extract_first('').split()
            pubtime = source_text[1].replace('发布时间：', '').replace('\n', '').strip()
            origin_name = source_text[0].replace('来源：', '').replace('\n', '').strip()
            content_div = response.xpath('.//div[@class="d2txt_con clearfix"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        


        title = ''.join(i.strip() for i in h1_div.xpath('./text()').extract())
        sub_title = ''.join(i.strip() for i in h3_div.xpath('./text()').extract())
        
        if sub_title:
            if sub_title.startswith("——"):
                title += sub_title
            else:
                title += "——" + sub_title
        
        content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[
            '//*[contains(text(),"相关新闻")]/ancestor::p',
            '//*[contains(text(),"相关新闻")]/ancestor::p/following-sibling::*'])
        
        return self.produce_item(response=response,
                                 title=title,
                                 pubtime=pubtime,
                                 origin_name=origin_name,
                                 content=content,

                                 media=media,
                                 )


class PeopleCpcSpider(PeopleSpider):
    """学习路上"""
    name = 'cpc_people'
    mystart_urls = {
        'http://cpc.people.com.cn/xuexi/GB/387488/index.html#p1': 212,  # '讲话原文',
        'http://cpc.people.com.cn/xuexi/GB/385476/index.html#p1': 213,  # '论述摘编',
        'http://cpc.people.com.cn/xuexi/GB/385477/index.html#p1': 214,  # '权威解读',
        'http://cpc.people.com.cn/xuexi/GB/385475/index.html#p1': 215,  # '独家策划',
        'http://cpc.people.com.cn/xuexi/GB/387489/index.html#p1': 216,  # '学习体会',
        'http://cpc.people.com.cn/xuexi/GB/387490/index.html#p1': 217,  # '图解',
        'http://cpc.people.com.cn/xuexi/GB/387492/index.html#p1': 218,  # '图集',  图集暂时不爬取
        # 'http://cpc.people.com.cn/xuexi/GB/387491/index.html#p1': 219,   #  '音视频' 音视频暂不爬取
        'http://cpc.people.com.cn/GB/64192/105996/352002/index.html': 220,  # '出席会议'
        'http://cpc.people.com.cn/GB/64192/105996/352003/index.html': 221,  # '出席活动'
        'http://cpc.people.com.cn/GB/64192/105996/352005/index.html': 93,   # 224,  # 会见接待  2019年7月8日核对source_id
        'http://cpc.people.com.cn/GB/64192/105996/352004/index.html': 223,  # '参观考察' 2019年7月8日核对source_id把224改为223
        'http://cpc.people.com.cn/GB/64192/105996/352006/index.html': 225,  # '出访'
        'http://cpc.people.com.cn/GB/64192/105996/352007/index.html': 226,  # '讲话'
        'http://cpc.people.com.cn/GB/64192/105996/352008/index.html': 227,  # '致电'
        'http://cpc.people.com.cn/GB/64192/105996/352009/index.html': 228,  # '其他'
        'http://cpc.people.com.cn/xijinping/index.html': 229,  # '首页'
        
        # 5月23日打标
        'http://cpc.people.com.cn/GB/164113/': 2688,
    }
    # http://cpc.people.com.cn/n1/2019/0115/c64094-30544006.html
    # http://cpc.people.com.cn/n1/2019/0325/c164113-30994324.html 图片
    # http://cpc.people.com.cn/n1/2019/0415/c164113-31030869.html 文本
    rules = (
        Rule(LinkExtractor(allow=r'cpc.people.com.cn/.*?/%s\d{2}/c\d+-\d+\.html' % datetime.today().strftime('%Y/%m'), deny='video'), callback='parse_item',
             follow=False),)
    custom_settings = deepcopy(PeopleSpider.custom_settings)
    custom_settings.update(
        {"SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleSpider.name,}
    )