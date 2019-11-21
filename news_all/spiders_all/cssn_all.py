# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin, urlsplit
import os
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from news_all.spider_models import NewsRCSpider, otherurl_meta
from copy import deepcopy


class CssnAllSpider(NewsRCSpider):
    """中国社会科学网"""
    name = 'cssn_all'
    mystart_urls = {
        'http://acad.cssn.cn/dzyx/dzyx_jxyx/': 1948, 'http://acad.cssn.cn/dzyx/dzyx_llsj/': 1949,
        'http://acad.cssn.cn/dzyx/dzyx_mtgz/': 1950, 'http://acad.cssn.cn/dzyx/dzyx_yxyw/': 1951,
        'http://arch.cssn.cn/kgx/ggkg/': 1952, 'http://arch.cssn.cn/kgx/kgdt/': 1953,
        'http://arch.cssn.cn/kgx/kgsb/': 1954, 'http://arch.cssn.cn/kgx/ycbh/': 1955,
        'http://art.cssn.cn/ysx/ysx_ycjx/': 1956, 'http://chis.cssn.cn/zgs/zgs_bk/': 1957,
        'http://chis.cssn.cn/zgs/zgs_gd/': 1958, 'http://chis.cssn.cn/zgs/zgs_jl/': 1959,
        'http://chis.cssn.cn/zgs/zgs_pl/': 1960, 'http://chis.cssn.cn/zgs/zgs_sb/': 1961,
        'http://cul.cssn.cn/wh/wh_whrd/': 1962, 'http://econ.cssn.cn/jjx/jjx_xjpxsdzgtsshzyjjsx/': 1963,
        'http://edu.cssn.cn/jyx/jyx_gdjyx/': 1964, 'http://edu.cssn.cn/jyx/jyx_ptjyx/': 1965,
        'http://gn.cssn.cn/hqxx/xkdt/xkdtnews/': 1966, 'http://gn.cssn.cn/hqxx/yw/': 1967,
        'http://his.cssn.cn/lsx/zwbl/': 1968, 'http://indi.cssn.cn/kxk/rdgz/': 1969,
        'http://joul.cssn.cn/bk/bkpd_qklm/bkpd_bkwz/': 1970, 'http://lcl.cssn.cn/gd/gd_rwhn/gd_mzgz/': 1971,
        'http://marx.cssn.cn/mkszy/gwmkzy/': 1972, 'http://marx.cssn.cn/mkszy/mkszy_zgjxdsjbwt/': 1973,
        'http://marx.cssn.cn/mkszy/mkszyfzs/': 1974, 'http://marx.cssn.cn/mkszy/mkszyzgh/': 1975,
        'http://marx.cssn.cn/mkszy/yc/': 1976, 'http://mil.cssn.cn/jsx/jsjj_jsx/': 1977,
        'http://news.cssn.cn/zx/bwyc/': 1978, 'http://news.cssn.cn/zx/shwx/': 1979,
        'http://news.cssn.cn/zx/yw/': 1980,'http://orig.cssn.cn/sf/': 1987,
        'http://phil.cssn.cn/zhx/zx_kxjszx/': 1988, 'http://pol.cssn.cn/zzx/zggcd_zzx/': 1989,
        'http://pol.cssn.cn/zzx/zgzz_zzx/': 1990, 'http://sky.cssn.cn/skyskl/skyskl_jczx/': 1991,
        'http://tt.cssn.cn/zk/zk_rdgz/': 1992, 'http://unt.cssn.cn/gx/gx_gjsd/': 1993,
        'http://unt.cssn.cn/gx/gx_gxxx/': 1994, 'http://unt.cssn.cn/gx/gx_xywh/': 1995,
        'http://unt.cssn.cn/gx/gxjxky/': 1996, 'http://unt.cssn.cn/gx/xskx/': 1997,
        'http://whis.cssn.cn/sjs/sjs_hqzs/': 1998, 'http://whis.cssn.cn/sjs/sjs_lsjd/': 1999,
        'http://www.cssn.cn/gjgxx/gj_bwsf/': 2026,
        'http://www.cssn.cn/gjgxx/gj_rdzx/': 2027
    }

    # http://www.cssn.cn/zx/201904/t20190402_4858823.shtml
    # http://cul.cssn.cn/wh/wh_cysc/201903/t20190326_4853705.shtml
    # http://econ.cssn.cn/jjx/jjx_xjpxsdzgtsshzyjjsx/201905/t20190514_4888612.html
    # http://www.cssn.cn/mkszyzghpd/mkszyzghpd_yc/201905/t20190513_4884446.html
    rules = (
        Rule(LinkExtractor(allow=(r'cssn.cn.*?/%s/t\d+_\d+.s?html'%datetime.today().strftime('%Y%m')), ),
                           callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'cssn.cn.*?\w+.s?htm'),
                           deny=(r'/201[0-8]', r'/20190[1-9]/', r'/20190[1-9]/',)
                           ),
             process_request=otherurl_meta, follow=False),
    )
    custom_settings = {
        'DEPTH_LIMIT': 0,
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }
    
    # http://www.cssn.cn/zx/201904/t20190418_4866089.shtml
    def parse_item(self, response):
        xp = response.xpath
        try:
            source_div = xp('.//div[@class="f-main-left-Title"]/div[@class="TitleFont2"]')[0]
            content_div = xp('.//div[@id="Zoom"]/div[@class="TRS_Editor"]')[0]
            time_re = source_div.re(r'\d{2,4}年\d{1,2}月\d{1,2}日\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
        except:
            return self.parse_item2(response)
        
        title = self.get_page_title(response).split('-')[0]

        all_page = xp(".//div[@class='ImageListView ImageListViewpage fenye']").re(r'var countPage = (\d+)')
        if all_page:
            count = int(all_page[0])
            if count > 1:
                urls = self.getAtUrl(count, response)
                return response.follow(urls[0], callback=self.parse_page,
                                       meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                             'pubtime': pubtime, 'title': title,
                                             'content': content_div.extract(), 'urls': urls,
                                             'start_url_time': response.meta.get('start_url_time'),
                                             'schedule_time': response.meta.get('schedule_time')
                                             })
        
        content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[])
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media
        )
    
    def getAtUrl(self, count, response):
        url_parse = urlsplit(response.url)
        tail, sufx = os.path.basename(url_parse.path).split('.')
        return [urljoin(response.url, tail + '_%s.' % idx + sufx) for idx in range(1, count)]
    
    def parse_page(self, response):
        meta_new = deepcopy(response.meta)
        try:
            content_div = response.xpath('.//div[@class="TRS_Editor"]')[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()
        
        index = response.meta['urls'].index(response.url)
        if index + 1 != len(response.meta['urls']):
            return response.follow(response.meta['urls'][index + 1], callback=self.parse_page,
                                   meta=meta_new)
        
        content, media, videos, video_cover = self.content_clean(meta_new['content'])
        
        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),
            content=content,
            media=media
        )
    
    # http://gn.cssn.cn/hqxx/tpnew/201904/t20190419_4866717.shtml      http://gn.cssn.cn/hqxx/tpnew/
    def parse_item2(self, response):
        xp = response.xpath
        try:
            source_div = xp('.//div[@class="HDphoto_main"]/div[@class="HDphoto_main_time"]')[0]
            content_div = xp('.//div[@class="HDphoto_main_img"]')[0]
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        
        title = self.get_page_title(response).split('-')[0]
        all_page = xp(".//div[@class='ImageListView ImageListViewpage fenye']").re(r'var countPage = (\d+)')
        if all_page:
            count = int(all_page[0])
            if count > 1:
                urls = self.getAtUrl(count, response)
                return response.follow(urls[0], callback=self.parse_page,
                                       meta={'source_id': response.meta.get('source_id'), 'first_url': response.url,
                                             'pubtime': pubtime, 'title': title,
                                             'content': content_div.extract(), 'urls': urls,
                                             'start_url_time': response.meta.get('start_url_time'),
                                             'schedule_time': response.meta.get('schedule_time')
                                             })
        
        content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[])
        
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media
        )
    
    def parse_page2(self, response):
        meta_new = deepcopy(response.meta)
        try:
            new_div = response.xpath('.//div[@id="f-main"]')[0]
            # source_div = new_div.xpath('./div[@class="HDphoto_main"]/div[@class="HDphoto_main_time"]')[0]
            content_div = new_div.xpath('./div[@class="HDphoto_main_img"]')[0]
        except:
            return self.produce_debugitem(response, 'xpath error')
        meta_new['content'] += content_div.extract()
        
        index = response.meta['urls'].index(response.url)   # '_14.shtml' 是索引14 第15页, urls = [第2页, ...最后一页的url]
        if index + 1 != len(response.meta['urls']):
            return response.follow(response.meta['urls'][index + 1], callback=self.parse_page2,
                                   meta=meta_new)
        
        content, media, videos, video_cover = self.content_clean(meta_new['content'], kill_xpaths=[])
        
        return self.produce_item(
            response=response,
            title=meta_new.get('title'),
            pubtime=meta_new.get('pubtime'),
            origin_name=meta_new.get('origin_name'),
            content=content,
            media=media
        )
