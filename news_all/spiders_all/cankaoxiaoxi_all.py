# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from copy import deepcopy
import re
from scrapy.conf import settings


class CanKaoXiaoXiSpider(NewsRCSpider):
    """参考消息"""
    name = 'cankaoxiaoxi_all'
    mystart_urls = {
        'http://photo.cankaoxiaoxi.com/mil/': 2189,  # 军事图片       图集
        'http://column.cankaoxiaoxi.com/': 2184,  # 观点
        'http://column.cankaoxiaoxi.com/g/china/': 2171,  # 海外看中国
        'http://www.cankaoxiaoxi.com/column/cartoon/': 2156,  #
        'http://ihl.cankaoxiaoxi.com/': 2186,  # 锐参考
        'http://www.cankaoxiaoxi.com/science/ITyj/': 2219,  # IT业界
        'http://www.cankaoxiaoxi.com/science/tsfx/': 2157,  # 探索发现
        'http://science.cankaoxiaoxi.com/': 2176,  # 科技健康
        'http://www.cankaoxiaoxi.com/finance/sygs/': 2163,  # 商业公司
        'http://finance.cankaoxiaoxi.com/': 2185,  # 财经
        'http://mil.cankaoxiaoxi.com/': 2179,  # 军事
        'http://world.cankaoxiaoxi.com/': 2201,  # 国际
        'http://www.cankaoxiaoxi.com/mil/wqzb/': 2164,  # 武器装备
        'http://www.cankaoxiaoxi.com/mil/zbdt/': 2221,  # 周边
        'http://www.cankaoxiaoxi.com/world/hqbl/': 2177,  # 环球博览
        'http://www.cankaoxiaoxi.com/world/ytxw/': 2167,  # 亚太
        'http://www.cankaoxiaoxi.com/china/shwx/': 2169,  # 社会观察
        'http://www.cankaoxiaoxi.com/china/szyw/': 2168,  # 时事外交
        'http://mil.cankaoxiaoxi.com/gjjq/': 2152,  #
        'http://mil.cankaoxiaoxi.com/zgjq/': 2151,  #
        'http://china.cankaoxiaoxi.com/': 2202,  # 中国
        'http://www.cankaoxiaoxi.com/science/hjbh/': 2155,  # 环境保护
        'http://www.cankaoxiaoxi.com/sports/zhty/': 2158,  # 综合体育
        'http://www.cankaoxiaoxi.com/sports/lq/': 2159,  # 篮球
        'http://www.cankaoxiaoxi.com/sports/zq/': 2160,  # 足球
        'http://www.cankaoxiaoxi.com/finance/jck/': 2161,  #
        'http://www.cankaoxiaoxi.com/finance/qyzx/': 2162,  # 企业资讯
        'http://www.cankaoxiaoxi.com/world/omxw/': 2166,  # 欧美
        'http://column.cankaoxiaoxi.com/kuaiping/': 2172,  # 参考快评
        'http://www.cankaoxiaoxi.com/sports/tyyc/': 2174,  # 有译思
        'http://www.cankaoxiaoxi.com/world/gjgd/': 2175,  # 国际滚动
        'http://www.cankaoxiaoxi.com/world/qtdq/': 2178,  # 其他地区
        'http://www.cankaoxiaoxi.com/china/gacz/': 2180,  # 港澳传真
        'http://www.cankaoxiaoxi.com/china/zgwj/': 2181,  # 中国外交
        'http://sports.cankaoxiaoxi.com/': 2182,  # 体育
        'http://finance.cankaoxiaoxi.com/chuhaiji/': 2183,  # 出海记
        'http://column.cankaoxiaoxi.com/g/column/g/china/ldzg/': 2188,  # 论道中国
        'http://photo.cankaoxiaoxi.com/world/': 2190,  # 国际图片             图集
        'http://column.cankaoxiaoxi.com/g/world/olgc/': 2191,  #
        'http://photo.cankaoxiaoxi.com/china/': 2192,  # 中国图片              图集
        'http://column.cankaoxiaoxi.com/g/world/dqs/': 2193,  #
        'http://column.cankaoxiaoxi.com/g/world/zuluyatai/': 2195,  #
        'http://photo.cankaoxiaoxi.com/finance/': 2199,  # 财经图片            图集
        'http://photo.cankaoxiaoxi.com/science/': 2200,  # 科技图片            图集
        'http://column.cankaoxiaoxi.com/g/china/zwgx/': 2203,  # 中外关系
        'http://www.cankaoxiaoxi.com/roll/': 2207,  # 滚动新闻
        'http://www.cankaoxiaoxi.com/photo/mil/': 2210,  # 军事图片             图集
        'http://www.cankaoxiaoxi.com/finance/gjcj/': 2212,  # 国际财经
        'http://www.cankaoxiaoxi.com/photo/world/': 2213,  # 国际图片         图集
        'http://www.cankaoxiaoxi.com/finance/zgcj/': 2214,  # 中国财经
        'http://mil.cankaoxiaoxi.com/jsgd/': 2216,  # 军事滚动
        'http://mil.cankaoxiaoxi.com/zbdt/': 2217,  # 周边动态
        'http://www.cankaoxiaoxi.com/science/jksh/': 2220,  # 健康生活
        'http://tw.cankaoxiaoxi.com': 2222,  # 台海
        'http://www.cankaoxiaoxi.com/tw/thgd/': 2223,  # 台海滚动
        'http://www.cankaoxiaoxi.com/tw/twyw/': 2224,  # 台湾要闻
        'http://www.cankaoxiaoxi.com/tw/hxla/': 2225,  # 海峡两岸
    }
    
    # http://column.cankaoxiaoxi.com/2019/0325/2375428.shtml
    # http://www.cankaoxiaoxi.com/photo/mil/20190327/2375556.shtml
    # http://ihl.cankaoxiaoxi.com/2019/0402/2376202.shtml
    rules = (
        Rule(LinkExtractor(allow=(r'cankaoxiaoxi.com.*?/%s\d{2}/\d{5,}.shtml' % datetime.today().strftime('%Y/%m'),
                                  r'cankaoxiaoxi.com.*?/%s\d{2}/\d{5,}.shtml' % datetime.today().strftime('%Y%m'),), ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'cankaoxiaoxi.com.*?\w{5,}.s?htm',),
                           deny=(r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/')),
             process_request=otherurl_meta, follow=False),
    )
    
    custom_settings = {
        'DEPTH_LIMIT': 0,  # 翻页需要设置深度为0 或者 >1
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    def parse_item(self, response):
        try:
            new_div = response.xpath('.//div[@id="allList"]')[0]
            source_div = new_div.xpath('.//div[@class="articleBody"]/div[@class="info"]')[0]
            content_div = \
            new_div.xpath('.//div[@class="articleBody"]/div[@class="articleContent"]/div[@class="articleText"]')[0]
            pubtime = source_div.xpath('.//span[@id="pubtime_baidu"]/text()')[0].extract()
        except:
            return self.parse_images(response)
        
        title1 = response.request.meta.get('link_text', '').strip()
        title = new_div.xpath('.//h1/text()').extract_first('').strip() or title1
        
        origin_name = source_div.xpath('.//span[@id="source_baidu"]/text()').extract_first('')
        
        next_a = response.xpath('//div[@class="page"]//a[@id="next_page"]')  # 下一页
        if next_a and next_a.xpath('./@href').extract_first() != 'http://www.cankaoxiaoxi.com/':
            content_div = \
            response.xpath('.//div[@class="articleBody"]/div[@class="articleContent"]/div[@class="articleText"]')[0]
            # print(content_div)
            return response.follow(next_a[0], callback=self.parse_page,
                                   meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                         'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                                         'content': content_div.extract(),
                                         'start_url_time': response.meta.get('start_url_time'),
                                         'schedule_time': response.meta.get('schedule_time')})
        
        content, media, videos, video_cover = self.content_clean(content_div)
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=content,
            media=media
        )
    
    def parse_page(self, response):
        xp = response.xpath
        meta_new = deepcopy(response.meta)
        
        try:
            new_div = xp('.//div[@id="allList"]')[0]
            content_div = \
            new_div.xpath('.//div[@class="articleBody"]/div[@class="articleContent"]/div[@class="articleText"]')[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()
        
        next_a = response.xpath('.//div[@class="page"]//a[@id="next_page"]')  # 下一页
        if next_a and next_a.xpath('./@href').extract_first() != 'http://www.cankaoxiaoxi.com/':
            return response.follow(next_a[0], callback=self.parse_page, meta=meta_new)
        """
        # 或者 
        next_url = xp('//*[@class="pageLink"]//a[contains(text(), "下一页")]/@href').extract_first()
        if next_url:
            yield response.follow(next_url, callback=self.parse_page)
        """
        content, media, videos, video_cover = self.content_clean(meta_new['content'])
        
        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),

            content=content,
            media=media
        )
    
    # http://www.cankaoxiaoxi.com/photo/mil/20190327/2375556.shtml   图集
    def parse_images(self, response):
        try:
            source_div = response.xpath('.//div[@class="main"]/div[@class="content column"]')[0]
            pubtime = source_div.xpath('.//div[@class="dateinfo"]/p/span[@class="date"]/text()')[0].extract()
        except:
            return self.parse_images2(response)
        
        title1 = response.request.meta.get('link_text', '').strip()
        title = source_div.xpath('.//h1/text()').extract_first('').strip() or title1
        
        origin_name = source_div.xpath('.//div[@class="dateinfo"]/p/span[@class="source"]/text()').extract_first('')
        
        rt = response.text
        # regex = re.compile("({ orig:.*?})")
        
        pat = re.compile(r"""orig: ['"](.*?)['"].*?note: ['"](.*?)['"]""")
        fr = re.finditer(pat, rt)
        media = {}
        new_content = ''
        total = rt.count('photos.push') - 1
        # content_list = regex.findall(rt)
        for i, j in enumerate(fr):
            media.setdefault("images", {})
            src = j.group(1)
            if i == total:
                break
            media["images"][str(i + 1)] = {"src": src}
            new_content += '${{%s}}$<p>%s</p>' % ((i + 1), j.group(2).encode('utf-8').decode('unicode_escape'))
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=new_content,
            media=media
        )
    
    # http://www.cankaoxiaoxi.com/photo/mil/20181224/2366322.shtml
    def parse_images2(self, response):
        try:
            source_div = response.xpath('.//div[@class="column"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        pubtime = source_div.xpath('.//*/span[@class="post-time"]/text()').extract_first('').strip()
        
        title1 = response.request.meta.get('link_text', '').strip()
        title = source_div.xpath('.//h1/text()').extract_first('').strip() or title1
        
        origin_name = source_div.xpath('.//*/span[@class="source"]/text()').extract_first('')
        
        rt = response.text
        # regex = re.compile("({ orig:.*?})")
        
        pat = re.compile(r"""orig: ['"](.*?)['"].*?note: ['"](.*?)['"]""")
        fr = re.finditer(pat, rt)
        media = {}
        new_content = ''
        total = rt.count('photos.push') - 2
        # content_list = regex.findall(rt)
        for i, j in enumerate(fr):
            media.setdefault("images", {})
            src = j.group(1)
            if i == total:
                break
            media["images"][str(i + 1)] = {"src": src}
            new_content += '${{%s}}$<p>%s</p>' % ((i + 1), j.group(2).encode('utf-8').decode('unicode_escape'))
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,

            content=new_content,
            media=media
        )
