# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class ZdsgSpider(NewsRCSpider):
    """驻各国大使馆"""
    name = 'zdsg'
    mystart_urls = {
        'http://tl.chineseembassy.org/chn/sgdt/': 1301669,  # 驻东帝汶民主共和国大使馆-使馆动态
        'http://uz.china-embassy.org/chn/zwgxzxdt/': 1301699,  # 驻乌兹别克斯坦共和国大使馆-中乌关系最新动态
        'http://uz.china-embassy.org/chn/zwgx/rwhz/': 1301698,  # 驻乌兹别克斯坦共和国大使馆-人文合作
        'http://uz.china-embassy.org/chn/sgxx/sgsd/': 1301697,  # 驻乌兹别克斯坦共和国大使馆-使馆动态
        'http://ye.china-embassy.org/chn/sgdt/': 1301704,  # 驻也门共和国大使馆-使馆动态
        'http://il.chineseembassy.org/chn/sgxw/': 1301705,  # 驻以色列国大使馆-使馆新闻动态
        'http://il.chineseembassy.org/chn/zygx/sbwl/': 1301706,  # 驻以色列国大使馆-双边往来
        'http://il.chineseembassy.org/chn/zygx/whys/jyjl/': 1301710,  # 驻以色列国大使馆-教育交流
        'http://il.chineseembassy.org/chn/zygx/whys/': 1301709,  # 驻以色列国大使馆-文化交流
        'http://il.chineseembassy.org/chn/zygx/kxjs/': 1301707,  # 驻以色列国大使馆-科技合作
        'http://il.mofcom.gov.cn/article/jmxw/': 1301708,  # 驻以色列国大使馆-经贸新闻
        'http://qa.chineseembassy.org/chn/zkgxyw/': 1301671,  # 驻卡塔尔国大使馆-中卡关系要闻
        'http://qa.chineseembassy.org/chn/dsxx/zyhd/': 1301672,  # 驻卡塔尔国大使馆-重要活动
        'http://kg.chineseembassy.org/chn/dssghd/': 1301903,  # 驻吉尔吉斯共和国大使馆-使馆活动
        'http://kz.chineseembassy.org/chn/sgxx/sgdt/': 1301670,  # 驻哈萨克斯坦共和国大使馆-使馆动态
        'http://tr.chineseembassy.org/chn/ztgx/': 1301695,  # 驻土耳其共和国大使馆-中土关系
        'http://tr.chineseembassy.org/chn/A/': 1301696,  # 驻土耳其共和国大使馆-文化交流
        'http://tr.chineseembassy.org/chn/xwdt/': 1301693,  # 驻土耳其共和国大使馆-新闻动态
        'http://tj.chineseembassy.org/chn/xwdt/': 1301936,  # 驻塔吉克斯坦共和国大使馆-新闻动态
        'http://bd.china-embassy.org/chn/zmjw/': 1301907,  # 驻孟加拉人民共和国大使馆-中孟交往
        'http://np.mofcom.gov.cn/article/c/': 1301680,  # 驻尼泊尔联邦民主共和国大使馆-双边往来
        'http://np.mofcom.gov.cn/article/redianzhuizong/': 1301678,  # 驻尼泊尔联邦民主共和国大使馆-商情发布
        'http://np.mofcom.gov.cn/article/zxhz/zhengt/': 1301679,  # 驻尼泊尔联邦民主共和国大使馆-对尼援助
        'http://np.mofcom.gov.cn/article/jmxw/': 1301677,  # 驻尼泊尔联邦民主共和国大使馆-经贸新闻
        'http://pk.chineseembassy.org/chn/zbgx/wenhuafuwu/': 1301894,  # 驻巴基斯坦伊斯兰共和国大使馆-文化交流
        'http://bh.china-embassy.org/chn/zbgx/': 1301662,  # 驻巴林王国大使馆-中巴关系
        'http://bh.china-embassy.org/chn/dsxx/dshd/': 1301663,  # 驻巴林王国大使馆-大使活动
        'http://lk.china-embassy.org/chn/xwdt/': 1301692,  # 驻斯里兰卡大使馆-使馆新闻
        'http://jp.china-embassy.org/chn/zrgx/': 1301909,  # 驻日本国大使馆-中日关系
        'http://jp.china-embassy.org/chn/sgxxs/': 1301908,  # 驻日本国大使馆-使馆信息
        'http://jp.china-embassy.org/chn/jyylxsjl/': 1301934,  # 驻日本国大使馆-教育与留学生交流
        'http://jp.china-embassy.org/chn/whjl/': 1301912,  # 驻日本国大使馆-文化交流
        'http://jp.china-embassy.org/chn/jykj/': 1301911,  # 驻日本国大使馆-科技合作
        'http://jp.china-embassy.org/chn/jmhz/': 1301910,  # 驻日本国大使馆-经贸合作
        'http://jp.china-embassy.org/chn/zrgx/rbsg/': 1301935,  # 驻日本国大使馆-重要演讲
        'http://kp.chineseembassy.org/chn/zcwj/': 1301896,  # 驻朝鲜民主主义人民共和国大使馆-中朝交往
        'http://kp.chineseembassy.org/chn/dssghd/': 1301897,  # 驻朝鲜民主主义人民共和国大使馆-大使/使馆活动
        'http://kp.chineseembassy.org/chn/zcgx/jyjl1/': 1301895,  # 驻朝鲜民主主义人民共和国大使馆-教育交流
        'http://kw.chineseembassy.org/chn/sbwl/': 1301904,  # 驻科威特国大使馆-双边往来
        'http://jo.chineseembassy.org/chn/zygxyw/': 1301711,  # 驻约旦哈希姆王国大使馆-使馆报道
        'http://jo.chineseembassy.org/chn/zygxs/jsjl/': 1301889,  # 驻约旦哈希姆王国大使馆-军事交流
        'http://jo.chineseembassy.org/chn/zygxs/zzwls/': 1301886,  # 驻约旦哈希姆王国大使馆-政治往来
        'http://jo.chineseembassy.org/chn/zygxs/kjwh/': 1301888,  # 驻约旦哈希姆王国大使馆-科技文化
        'http://jo.chineseembassy.org/chn/zygxs/jmhz/': 1301887,  # 驻约旦哈希姆王国大使馆-经贸合作
        'http://jo.chineseembassy.org/chn/dsxxs/zyhd/': 1301890,  # 驻约旦哈希姆王国大使馆-重要活动
        'http://ph.china-embassy.org/chn/zfgxzgdmgx/': 1301898,  # 驻菲律宾共和国大使馆-中菲关系/中国/东盟关系
        'http://ph.china-embassy.org/chn/zfgx/jswl/': 1301901,  # 驻菲律宾共和国大使馆-军事交往
        'http://ph.china-embassy.org/chn/zfgx/zzgx/': 1301899,  # 驻菲律宾共和国大使馆-政治关系
        'http://ph.china-embassy.org/chn/zfgx/whjy/': 1301902,  # 驻菲律宾共和国大使馆-文化交流
        'http://ph.china-embassy.org/chn/zfgx/jmgx/': 1301900,  # 驻菲律宾共和国大使馆-经贸关系
        'http://mn.china-embassy.org/chn/sghd/': 1301675,  # 驻蒙古国大使馆-使馆活动
        'http://mn.china-embassy.org/chn/yhjl/': 1301674,  # 驻蒙古国大使馆-友好交流
        'http://mn.china-embassy.org/chn/mgdt/': 1301676,  # 驻蒙古国大使馆-蒙古动态
        'http://az.china-embassy.org/chn/xwdt/': 1301661,  # 驻阿塞拜疆共和国大使馆-新闻动态
        'http://sy.chineseembassy.org/chn/tzhf/': 1301892,  # 驻阿拉伯叙利亚共和国大使馆-团组互访
        'http://sy.chineseembassy.org/chn/xwfb/': 1301891,  # 驻阿拉伯叙利亚共和国大使馆-新闻发布
        'http://mv.china-embassy.org/chn/zmgx/': 1301906,  # 驻马尔代夫共和国大使馆-中马关系
        'http://mv.china-embassy.org/chn/sgsd/': 1301905,  # 驻马尔代夫共和国大使馆-使馆快递
        'http://lb.china-embassy.org/chn/zyts/': 1301673,  # 驻黎巴嫩共和国大使馆-要闻及重要提示
    }
    rules = (
        #http://tl.chineseembassy.org/chn/sgdt/t1672921.htm
        #http://uz.china-embassy.org/chn/zwgxzxdt/t1657889.htm
        #http://uz.china-embassy.org/chn/zwgx/rwhz/t1640632.htm
        #http://uz.china-embassy.org/chn/sgxx/sgsd/t1672794.htm
        #http://ye.china-embassy.org/chn/sgdt/t1673011.htm
        #http://il.chineseembassy.org/chn/sgxw/t1671197.htm
        #http://il.chineseembassy.org/chn/zygx/sbwl/t1616080.htm
        #http://il.chineseembassy.org/chn/zygx/whys/jyjl/t1663346.htm
        #http://il.chineseembassy.org/chn/zygx/whys/t1473521.htm
        #http://qa.chineseembassy.org/chn/zkgxyw/t1672710.htm
        #http://kg.chineseembassy.org/chn/dssghd/t1671300.htm
        #http://kz.chineseembassy.org/chn/sgxx/sgdt/t1672778.htm
        #http://tr.chineseembassy.org/chn/xwdt/t1669845.htm
        #http://bd.china-embassy.org/chn/zmjw/t1668138.htm
        #http://pk.chineseembassy.org/chn/zbgx/wenhuafuwu/t1639569.htm

        #http://il.mofcom.gov.cn/article/jmxw/201906/20190602872569.shtml
        #http://np.mofcom.gov.cn/article/c/201804/20180402733921.shtml
        #http://np.mofcom.gov.cn/article/zxhz/zhengt/201905/20190502867606.shtml

        #http://tl.chineseembassy.org/chn/sgdt/t1672921.htm
        #http://qa.chineseembassy.org/chn/zkgxyw/t1672710.htm
        Rule(LinkExtractor(allow=(r'chineseembassy.org/chn.*?/t\d+.htm'),
                           ), callback='parse_item',
             follow=False),
        #http://uz.china-embassy.org/chn/zwgx/rwhz/t1640632.htm
        Rule(LinkExtractor(allow=(r'china-embassy.org/chn.*?/t\d+.htm'),
                           ), callback='parse_item',
             follow=False),
        ##http://np.mofcom.gov.cn/article/zxhz/zhengt/201905/20190502867606.shtml
        Rule(LinkExtractor(allow=(r'np.mofcom.gov.cn/article.*?/%s/\d+.shtml' % datetime.today().strftime('%Y%m'),),
                           ), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@id='News_Body_Title']/text()").extract_first()
            # source = xp("//div[@class='article-infos']")[0]
            content_div = xp("//div[@id='News_Body_Txt_A']")[0]
            pubtime = xp("//div[@id='News_Body_Time']").re(r'\d{2,4}/\d{1,2}/\d{1,2}')[0]
            # pubtime = xp("//div[@id='News_Body_Time']/text()").extract_first()
            
            
            # origin_name = xp('//span[@class="source"]/text()').extract_first('')
            origin_name = " "
        except:
            return self.parse_item_2(response)

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )

    def parse_item_2(self, response):
        
        xp = response.xpath
        try:
            title = xp("//div[@id='article']/table/tbody/tr[1]/td/text()").extract_first()
            # source = xp("//div[@class='article-infos']")[0]
            content_div = xp("//div[@id='article']")[0]
            pubtime = xp("//tr[2]/td[@class='t2']").re(r'\d{2,4}/\d{1,2}/\d{1,2}')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            
            
        except:
            return self.parse_item_3(response)

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            
            content=content,
            media=media
        )

    #http://np.mofcom.gov.cn/article/redianzhuizong/201906/20190602871705.shtml
    def parse_item_3(self, response):
        
        xp = response.xpath
        try:
            title = xp("//h2[@id='artitle']/text()").extract_first()
            # source = xp("//div[@class='article-infos']")[0]
            content_div = xp("//div[@id='zoom']")[0]
            pubtime = xp("//tbody/tr/td[2]/text()").extract_first().strip()
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            
            
            origin_name = xp('//td[@class="from"]/text()').extract_first('')
        except:
            return self.parse_item_4(response)

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )

    def parse_item_4(self, response):
        
        xp = response.xpath
        try:
            title = xp("//td[@class='bigtitle']/text()").extract_first()
            # source = xp("//div[@class='article-infos']")[0]
            content_div = xp("//td[@class='content1']")[0] or xp("//td[@class='content']")[0]
            pubtime = xp("//td[@class='time']").re(r'\d{2,4}/\d{1,2}/\d{1,2}')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            
            
            origin_name = " "
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, _, _ = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=pubtime,
            origin_name=origin_name,
            
            content=content,
            media=media
        )

