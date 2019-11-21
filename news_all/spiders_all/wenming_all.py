# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class WenmingAllSpider(NewsRCSpider):
    """中国文明网"""
    name = 'wenming_all'
    mystart_urls = {
        'http://www.wenming.cn/ldhd/': 2208,
        'http://www.wenming.cn/a2/gzhy/': 2209, 'http://www.wenming.cn/bwzx/jj/': 2211,
        'http://www.wenming.cn/bwzx/dt/': 2215, 'http://www.wenming.cn/bwzx/ggtz/': 2218,
        'http://www.wenming.cn/ziliao/rsrm/': 2226, 'http://www.wenming.cn/specials/mtnxw/': 2227,
        'http://www.wenming.cn/wmcz2017/yfys/': 2228, 'http://www.wenming.cn/wmxy/yw_01/': 2229,
        'http://www.wenming.cn/wcnrsxdd/': 2230, 'http://www.wenming.cn/zyfw/rd/': 2231,
        'http://www.wenming.cn/zyfw/dffc/': 2232, 'http://www.wenming.cn/zyfw/bmfc/': 2233,
        'http://www.wenming.cn/wmly/yw_01/': 2234, 'http://www.wenming.cn/wmjts/yw_01/': 2235,
        'http://www.wenming.cn/wmczs/yw_01/': 2236, 'http://www.wenming.cn/sdkm/sj/': 2237,
        'http://www.wenming.cn/sbhr_pd/tt/': 2238, 'http://www.wenming.cn/wmpl_pd/yczl/': 2239,
        'http://www.wenming.cn/wmpl_pd/zmgd/': 2240, 'http://www.wenming.cn/wmzh_pd/jj_wmzh/': 2241,
        
        # 老爬虫的
        'http://www.wenming.cn/a2/fbt/': 1301303,  # 中国文明网-发布厅
        'http://www.wenming.cn/dfcz/index_30050.shtml': 1301633,  # 中国文明网-地方联播
        'http://www.xingshizhengce.com/xjxx/': 1301305,  # 中国文明网-形势政策-宣教信息-左侧列表
        'http://www.wenming.cn/a/yw/': 1301306,  # 中国文明网-要闻
    }
    # http://www.wenming.cn/ldhd/xjp/zyjh/201905/t20190504_5100282.shtml
    rules = (
        Rule(LinkExtractor(allow=(r'wenming.cn.*?/%s/t\d+_\d+.shtml' % datetime.today().strftime('%Y%m')), ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'wenming.cn.*?\d+.s?html',),
                           deny=(r'/201[0-8]', r'20190[1-6]')),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            source_div = xp('.//div[@class="box_tex"]/div[@id="time_tex"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}')
            pubtime = time_re[0]
            content_div = xp('.//div[@id="tex"]/div[@class="TRS_Editor"]')[0]
            title = xp('//div[@id="title_tex"]/text()').extract_first('') or self.get_page_title(response).split('---')[
                0]
            og = source_div.re(r'来源：[\S]+')
            origin_name = og[0] if og else xp('/html/head/meta[@name="source"]/@content').extract_first('')
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    # http://www.wenming.cn/wmpl_pd/zmgd/201905/t20190505_5100910.shtml
    def parse_item2(self, response):
        xp = response.xpath
        try:
            source_div = xp('.//div[@class="tt"]/div[@class="tt-box"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}')
            pubtime = time_re[0]
            content_div = xp('.//div[@class="main-l-box"]/div[@class="TRS_Editor"]')[0]
            title = xp('//div[@class="tt-tit"]/text()').extract_first('') or self.get_page_title(response).split('---')[
                0]
            origin_name = xp('//div[@class="tt-ly"]/text()').extract_first('') or xp(
                '/html/head/meta[@name="source"]/@content').extract_first('')
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.parse_item3(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
        
    def parse_item3(self, response):
        # http://www.wenming.cn/dfcz/hn/201905/t20190505_5100564.shtml
        xp = response.xpath
        try:
            source_div = xp('.//div[@class="dc-title02"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}')
            pubtime = time_re[0]
            content_div = xp('.//div[@class="TRS_Editor"]')[0]
            origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first('')
            title = xp('//div[@class="dc-title"]/text()').extract_first('') or \
                    self.get_page_title(response).split('---')[0]
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.parse_item4(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item4(self, response):
        # http://www.wenming.cn/sbhr_pd/sbhr_zghyshhs/gxbj/201901/t20190104_4961299.shtml
        
        xp = response.xpath
        try:
            source_div = xp('.//div[@class="R-date"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}')
            pubtime = time_re[0]
            content_div = xp('.//div[@class="TRS_Editor"]')[0]
            origin_name = xp('/html/head/meta[@name="source"]/@content').extract_first('')
            title = xp('//div[@class="pannel-title"]/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div)
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
