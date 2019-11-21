# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta


class ChinaGovAllSpider(NewsRCSpider):
    """中国政府网"""
    name = 'china_gov_all'
    mystart_urls = {
     'http://www.gov.cn/premier/zuixin.htm': 2253,
     'http://www.gov.cn/premier/lkq_hy.htm': 2254, 'http://www.gov.cn/premier/lkq_hd.htm': 2255,
     'http://www.gov.cn/premier/lkq_cxcj.htm': 2256, 'http://www.gov.cn/premier/meitibaodao.htm': 2257,
     'http://www.gov.cn/premier/lkq_jh.htm': 2258, 'http://www.gov.cn/premier/lkq_wz.htm': 2259,
     'http://www.gov.cn/premier/lkq_tpk.htm': 2260, 'http://www.gov.cn/guowuyuan/gwy_cwh.htm': 2261,
     'http://www.gov.cn/guowuyuan/gwycw_sc.htm': 2262, 'http://www.gov.cn/premier/lkq_cf.htm': 2263,
     'http://www.gov.cn/guowuyuan/hanzheng/hz_zx.htm': 2264, 'http://www.gov.cn/guowuyuan/hanzheng/hz_hy.htm': 2265,
     'http://www.gov.cn/guowuyuan/hanzheng/hz_hd.htm': 2266, 'http://www.gov.cn/guowuyuan/hanzheng/hz_cxcj.htm': 2267,
     'http://www.gov.cn/guowuyuan/sunchunlan/scl_zx.htm': 2268,
     'http://www.gov.cn/guowuyuan/sunchunlan/scl_hd.htm': 2269,
     'http://www.gov.cn/guowuyuan/sunchunlan/scl_cxcj.htm': 2270,
     'http://www.gov.cn/guowuyuan/huchunhua/hch_zx.htm': 2271, 'http://www.gov.cn/guowuyuan/huchunhua/hch_hy.htm': 2272,
     'http://www.gov.cn/guowuyuan/huchunhua/hch_cxcj.htm': 2273, 'http://www.gov.cn/guowuyuan/liuhe/lh_zx.htm': 2274,
     'http://www.gov.cn/guowuyuan/liuhe/lh_hd.htm': 2275, 'http://www.gov.cn/guowuyuan/liuhe/lh_cf.htm': 2276,
     'http://www.gov.cn/guowuyuan/liuhe/lh_cxcj.htm': 2277, 'http://www.gov.cn/guowuyuan/weifenghe/zuixin.htm': 2278,
     'http://www.gov.cn/guowuyuan/weifenghe/huodong.htm': 2279, 'http://www.gov.cn/guowuyuan/wangyong/zuixin.htm': 2280,
     'http://www.gov.cn/guowuyuan/wangyong/wangy_hd.htm': 2281,
     'http://www.gov.cn/guowuyuan/wangyong/wangy_cxcj.htm': 2282, 'http://www.gov.cn/guowuyuan/wangyi/zuixin.htm': 2283,
     'http://www.gov.cn/guowuyuan/wangyi/chufang.htm': 2284, 'http://www.gov.cn/guowuyuan/wangyi/cxcj.htm': 2285,
     'http://www.gov.cn/guowuyuan/xiaojie/zuixin.htm': 2286, 'http://www.gov.cn/guowuyuan/xiaojie/huodong.htm': 2287,
     'http://www.gov.cn/guowuyuan/xiaojie/cxcj.htm': 2288, 'http://www.gov.cn/guowuyuan/zhaokezhi/huodong.htm': 2289,
     'http://www.gov.cn/guowuyuan/zhaokezhi/cxcj.htm': 2290, 'http://www.gov.cn/xinwen/fabu/zccfh/index.htm': 2291,
     'http://www.gov.cn/xinwen/fabu/bumen.htm': 2292, 'http://www.gov.cn/zhengce/zuixin.htm': 2293,
     'http://www.gov.cn/zhengce/index.htm': 2294, 'http://www.gov.cn/zhengce/jiedu/bumen.htm': 2295,
     'http://www.gov.cn/zhengce/jiedu/zhuanjia.htm': 2296, 'http://www.gov.cn/zhengce/jiedu/meiti.htm': 2297,
     'http://www.gov.cn/fuwu/fuwuxinxi/index.html': 2298, 'http://www.gov.cn/shuju/kuaidi.htm': 2299,
     'http://www.gov.cn/shuju/jiedu.htm': 2300, 'http://www.gov.cn/shuju/yaowen.htm': 2301
    }

    # http://www.gov.cn/premier/2019-04/30/content_5387938.htm
    rules = (
        Rule(LinkExtractor(allow=(r'gov.cn.*?/%s/\d{2}/content_\d+.htm'%datetime.today().strftime('%Y-%m')), ),
                           callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'gov.cn.*?w+.htm'),  deny=(r'/201[0-8]', r'/20190[1-9]/', r'/2019-0[1-9]', r'download.html'),),
                           process_request=otherurl_meta, follow=False),
    )

    #http://www.oceanol.com/content/201904/16/c86335.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="article oneColumn pub_border"]')[0]
            source_div = news_div.xpath('./div[@class="pages-date"]')[0]
            content_div = news_div.xpath('./div[@id="UCAP-CONTENT"]')[0]
            # pubtime = source_div.xpath('./div[@class="ly"]/span[@id="time_tex"]/text()').extract_first('').strip()
            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
            title = ''.join(i.strip() for i in news_div.xpath('./h1/text()').extract())
            origin_name = news_div.xpath('./div[@class="pages-date"]/span[@class="font"]/text()').extract_first('')
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
