# -*- coding: utf-8 -*-

from copy import deepcopy
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
import re

allurl_pat = re.compile(r'"allUrl"\:"(.*?html)')


class CriSpipder(NewsRCSpider):
    '''国际在线'''
    name = 'cri_all'
    
    mystart_urls = {
        'http://bj.cri.cn/list/3268c6a5-109a-4391-b3f6-9e8b8df13f3a.html': 913,  # 乐活北京
        'http://bj.cri.cn/list/a96994f1-a1d6-4f66-adc1-96464ebbe272.html': 914,  # 创新北京
        'http://city.cri.cn/tourism': 883,  # 旅游
        'http://cx.cri.cn/technology': 859,  # 科技创新
        'http://ent.cri.cn/drama/zx/': 1306,  # 更多>>
        'http://ln.cri.cn/fangchan/guandian': 1294,  # 观点
        'http://ln.cri.cn/fangchan/redian': 1296,  # 热点
        'http://ich.cri.cn/news': 875,  # 要闻滚动
        'http://ich.cri.cn/ichexhibition': 870,  # 非遗风采
        'http://news.cri.cn/list/zhuanjiatan': 231,  # 1222,  # 专家谈
        ##'http://gx.cri.cn/news': 1018,   #  广西要闻
        'http://news.cri.cn/list/Macron': 1218,  # 马克龙
        'http://news.cri.cn/list/Trump': 1219,  # 特朗普
        'http://news.cri.cn/list/TheresaMaryMay': 1220,  # 特雷莎·梅
        'http://news.cri.cn/china': 1226,  # 国内
        'http://hn.cri.cn/yule': 902,  # 娱乐
        'http://hlj.cri.cn/ent': 242,  # 1165,  # 更多>>
        'http://ge.cri.cn/roll': 887,  # 滚动
        'http://ge.cri.cn/globalnews': 886,  # 环球快讯
        'http://ge.cri.cn/policy': 888,  # 政策解读 
        'http://news.cri.cn/list/B&R': 853,  # 一带一路
        'http://money.cri.cn/fund': 247,  # 856,  # 基金
        'http://money.cri.cn/stock': 278,  # 857,  # 证券
        'http://money.cri.cn/bank': 285,  # 855,  # 银行
        'http://ce.cri.cn/view': 866,  # 观点
        'http://ce.cri.cn/depth': 863,  # 深度
        # 'http://sports.cri.cn/list/zhuting': 1333,  # 朱婷   # 删除 不更新
        'http://sports.cri.cn/list/zhouqi': 288,  # 1334,  # 周琦
        # 'http://sports.cri.cn/list/shalabowa': 1335,  # 莎拉波娃  # 删除 不更新
        'http://sports.cri.cn/list/sunyang': 1336,  # 孙杨
        # 'http://sports.cri.cn/list/lipi': 1337,  # 里皮  # 删除 不更新
        # 'http://sports.cri.cn/list/lindan': 1338,  # 林丹   # 删除 不更新
        # 'http://sports.cri.cn/list/liuguoliang': 1339,  # 刘国梁   # 删除 不更新
        'http://sports.cri.cn/list/kebi': 1340,  # 科比
        'http://sports.cri.cn/list/huangma': 1341,  # 皇家马德里
        'http://sports.cri.cn/list/feidele': 1342,  # 费德勒
        'http://sports.cri.cn/list/dingjunhui': 1343,  # 丁俊晖
        'http://sn.cri.cn/food': 1154,  # 美食
        'http://eco.cri.cn/povertyalleviation': 865,  # 精准扶贫
        'http://news.cri.cn/opinion/': 1212,  # 评论
        'http://news.cri.cn/list/Merkel': 967,  # 默克尔
        'http://news.cri.cn/list/wmkzg': 970,  # 外媒看中国
        'http://arts.cri.cn/news': 854,  # 新闻聚焦
        'http://cx.cri.cn/news': 1163,  # 创新要闻
        'http://ce.cri.cn/focus': 1145,  # 全息热点
        'http://money.cri.cn/news': 965,  # 理财要闻
        'http://cx.cri.cn/famous': 1160,  # 企业创新
        'http://eco.cri.cn/news': 962,  # 今日新闻
        'http://arts.cri.cn/exhibitions': 1147,  # 展讯导航
        'http://sn.cri.cn/B&R': 1153,  # 国际范
        'http://it.cri.cn/industry': 1164,  # 业界
        'http://news.cri.cn/special/2019lh/voice': 1266,  # 更多 >
        'http://news.cri.cn/special/2019lh/roll': 1264,  # 更多 >
        'http://news.cri.cn/world/': 839,  # 国际
        'http://news.cri.cn/': 845,  #
        'http://news.cri.cn/china/': 841,  # 国内
        'http://ge.cri.cn/inc/f80ca528-5aa5-4961-93e4-3a86c7b69e57.inc': 1349,  #  
        'http://sports.cri.cn/': 848,  # 体育
        'http://news.cri.cn/exclusive': 842,  # 原创
        'http://news.cri.cn/special/2019lh/live': 1267,  # 更多 >
        'http://news.cri.cn/special/2019lh/pinglun': 1265,  # 更多 >
        'http://news.cri.cn/cfxx': 836,  #
        'http://jiaoxue.cri.cn/hotnews': 823,  #
        'http://if.cri.cn/payment/index.html': 819,  #
        'http://if.cri.cn/p2p/index.html': 91106,  # 821,  #
        'http://ent.cri.cn/roll': 827,  #
        'http://news.cri.cn/list/guankuitianxia': 837,  # 管窥
    }
    rules = (
        # http://news.cri.cn/20190321/62a25611-be8e-46d2-6dae-7aeb3a518130.html
        # http://sn.cri.cn/n/20190512/ead934ff-6d0c-ba5c-46fc-e6a1cf756cb5.html
        Rule(
            LinkExtractor(allow=r'cri.cn.*?/%s\d{2}/.*?.html' % datetime.today().strftime('%Y%m'), deny=('video', 'audio'),
                          ),
            callback='parse_item', follow=False),
        # http://money.cri.cn/303/2019/05/06/e3051329-e6d9-63e7-3c6c-32456d65979b.html
        Rule(
            LinkExtractor(allow=r'cri.cn.*?/%s/\d{2}/.*?.html' % datetime.today().strftime('%Y/%m'),
                          deny=('video', 'audio'),
                          ),
            callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'cri.cn.*?.htm'),
                           deny=(r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/', r'cri.cn/special/', r'cri.cn/list/',
                                 r'/index.htm', r'/sitemap.html', r'cri.cn/live/')),
             process_request=otherurl_meta, follow=False)
    )
    custom_settings = {
        'DEPTH_LIMIT': 0,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
 
    # http://news.cri.cn/20190321/62a25611-be8e-46d2-6dae-7aeb3a518130.html
    # http://ln.cri.cn/20190226/4ba47d15-7b87-2c3c-9b67-161fdc5c513c.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            content_div = xp('.//div[@id="abody"]')[0]
            allurl = self.get_allpageurl(content_div)
            if allurl:
                return response.follow(allurl, callback=self.parse_allpage,
                                       meta={'source_id': response.meta.get('source_id'),
                                             'start_url_time': response.meta.get('start_url_time'),
                                             'schedule_time': response.meta.get('schedule_time')})
            pb = xp('.//span[@id="acreatedtime" or @id="apublishtime"]/text()') or xp('//div[@class="caption"]/*/span[1]/text()')
            pubtime = pb[0].extract().strip()
        except:
            return self.parse_item2(response)

        title = ''.join(i.strip() for i in xp('.//h1/text()').extract_first('')) or self.get_page_title(response).split('-')[0]
        origin_name = xp('.//span[@id="asource"]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    # http://news.cri.cn/20190315/87baadb1-261c-787f-add4-82d84da2aced.html
    def parse_item2(self, response):
        try:
            content_div = response.xpath('.//div[@id="abody"]')[0]
            allurl = self.get_allpageurl(content_div)
            if allurl:
                return response.follow(allurl, callback=self.parse_allpage,
                                       meta={'source_id': response.meta.get('source_id'),
                                             'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')})
            head_div = response.xpath('.//div[@class="slider-top"]')[0]
            pubtime = head_div.xpath('.//*/span[1]/text()')[0].extract().strip()
        except:
            return self.parse_item3(response)
        
        title = ''.join(i.strip() for i in head_div.xpath('./h3/text()').extract_first('')) or self.get_page_title(response).split('-')[0]
        origin_name = head_div.xpath('.//*/span[2]/text()').extract_first('')
        # origin_name = head_div.re('来源：(\w{2,})')[0]
        
        content, media, videos, video_cover = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    # http://arts.cri.cn/20190311/a690c356-7cdb-23fc-8e8d-1f83e7a2c782.html
    def parse_item3(self, response):
        try:
            content_div = response.xpath('.//div[@id="abody"]')[0]
            allurl = self.get_allpageurl(content_div)
            if allurl:
                return response.follow(allurl, callback=self.parse_allpage,
                                       meta={'source_id': response.meta.get('source_id'),
                                             'start_url_time': response.meta.get('start_url_time'),
                                             'schedule_time': response.meta.get('schedule_time')
                                             })
            news_div = response.xpath('.//div[@class="con-title clearfix"]')[0]
            head_div = news_div.xpath('.//div[@class="info"]')[0]

            time_re = head_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        
        title = ''.join(i.strip() for i in news_div.xpath('./h3/text()').extract_first('')) or self.get_page_title(response).split('-')[0]
        origin_name = head_div.xpath('.//span[2]/a/text()').extract_first('')
        # origin_name = head_div.re('来源：(\w{2,})')[0]
        
        content, media, videos, video_cover = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def get_allpageurl(self, content_div):
        pagedata = content_div.xpath('./@pagedata').extract()
        if not pagedata:
            return
        url_sh = allurl_pat.search(pagedata[0])
        if url_sh:
            return url_sh.group(1)
    
    def parse_allpage(self, response):
        xp = response.xpath
        try:
            news_div = response.xpath('.//div[@class="article-box"]')[0]
            content_div = xp('.//div[@id="abody"]')[0]
            pubtime = xp('.//span[@id="acreatedtime" or @id="apublishtime"]/text()')[0].extract().strip()
        except:
            return self.produce_debugitem(response, "xpath error")
        
        title = ''.join(i.strip() for i in news_div.xpath('.//h1/text()').extract_first('')) or self.get_page_title(response).split('-')[0]
        origin_name = xp('./span[@id="asource"]/text()').extract_first('')
        content, media, videos, video_cover = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
