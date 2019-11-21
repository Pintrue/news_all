#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/29 10:45
# @Author  : wjq
# @File    : chinadevelopment_all.py


from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from news_all.tools.others import to_list


class ChinadevelopmentAllSpider(NewsRCSpider):
    """中国发展网"""
    name = 'chinadevelopment_all'

    mystart_urls = {
        'http://dfmg.chinadevelopment.com.cn/mgkb/': 2743,  # //div[@class='fgwsf1']/ul[@class='fgwsf1-list']
        'http://aqzg.chinadevelopment.com.cn/jryw/': 2689,
        'http://cyfz.chinadevelopment.com.cn/cjyw/': 2690,
        'http://www.chinadevelopment.com.cn/news/zj/': 2693,
        'http://news.chinadevelopment.com.cn/zj/': 2697,
        'http://news.chinadevelopment.com.cn/ny/': 2698,
        'http://ndrc.chinadevelopment.com.cn/': 2699,
        'http://fz.chinadevelopment.com.cn/rd/': 2710,
        'http://fz.chinadevelopment.com.cn/cjsy/': 2716,
        'http://fz.chinadevelopment.com.cn/xyjs/': 2723,
        'http://fz.chinadevelopment.com.cn/yq/': 2725,
        'http://fz.chinadevelopment.com.cn/zcgd/': 2730,
        'http://fz.chinadevelopment.com.cn/fzzx/': 2731,
        'http://fz.chinadevelopment.com.cn/szfl/': 2735,
        'http://gjxq.chinadevelopment.com.cn/zxbd/': 2738,
        'http://dfmg.chinadevelopment.com.cn/mlwx/': 2742,
        'http://dfmg.chinadevelopment.com.cn/zczn/': 2745,
        'http://stpd.chinadevelopment.com.cn/lscy/': 2784, 'http://stpd.chinadevelopment.com.cn/zydt/': 2785,
        'http://slgj.chinadevelopment.com.cn/xwzx/hwxw/': 2786, 'http://www.chinadevelopment.com.cn/zgzs/gg/': 2787,
        'http://www.chinadevelopment.com.cn/zgzs/zx/': 2790, 'http://finance.chinadevelopment.com.cn/hy/ct/': 2793,
        'http://finance.chinadevelopment.com.cn/hy/jk/': 2794, 'http://finance.chinadevelopment.com.cn/hy/wy/': 2795,
        'http://finance.chinadevelopment.com.cn/hy/xf/': 2796, 'http://finance.chinadevelopment.com.cn/sc/yh/': 2798,
        'http://finance.chinadevelopment.com.cn/hy/': 2799, 'http://finance.chinadevelopment.com.cn/sc/gp/': 2800,
        'http://finance.chinadevelopment.com.cn/sp/': 2801, 'http://finance.chinadevelopment.com.cn/yw/': 2802,
        'http://finance.chinadevelopment.com.cn/sc/': 2804,
        'http://www.chinadevelopment.com.cn/fgw/': 3037,
    }

    rules = (
        # http://dfmg.chinadevelopment.com.cn/mgkb/2019/03/1482736.shtml
        # http://gjxq.chinadevelopment.com.cn/zxbd/2019/1484552.shtml
        # http://special.chinadevelopment.com.cn/2019zt/ztfy/2019/04/1479898.shtml
        # http://special.chinadevelopment.com.cn/2019zt/yjdjjxs/dfjj/dalian/2019/04/1493744.shtml
        # http://special.chinadevelopment.com.cn/2019zt/mtjj/2019/04/1484478.shtml
        # http://jjj.chinadevelopment.com.cn/jjjyw/2019/0404/1486809.shtml
       
        # http://special.chinadevelopment.com.cn/2019zt/2019lt/2019/01/1448145.shtml
        Rule(LinkExtractor(allow=(r'special.chinadevelopment.com.cn/\d{4}zt/\d{4}lt/%s/\d{2}/\d{6,}.shtml' % datetime.today().year,),
                           ),
             callback='parse_item_7', follow=False),
        # http://gjxq.chinadevelopment.com.cn/zxbd/2019/1505014.shtml
        Rule(LinkExtractor(
            allow=(r'gjxq.chinadevelopment.com.cn/zxbd/%s/\d{6,}.shtml' % datetime.today().year,),
            ),
             callback='parse_item_5', follow=False),
        Rule(LinkExtractor(allow=(r'chinadevelopment.com.cn/.*?/%s/(?:\d{2,4}/)?\d{6,}.shtml' % datetime.today().year,),
                           deny=('2019qglh', 'jbxx')),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=(r'chinadevelopment.com.cn.*?\w{6,}\.s?htm',), deny=('2019qglh', 'jbxx', '/201[0-8]/', r'chinadevelopment.com.cn/jbxx/\d+.shtml')),
             process_request=otherurl_meta, follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            # http://jjj.chinadevelopment.com.cn/jjjyw/2019/0404/1486809.shtml
            content_div = xp('.//div[contains(@class,"article-detail-inner")]') or xp(
                './/div[@class="left-box"]/div[contains(@class,"article-describe") or @class="content"]')
            source_div = xp('.//div[@class="article-infos ov"]')[0]
            pubtime = source_div.xpath('./span[@class="date fl-l"]/text()').extract_first('').strip()
            
            
        except:
            return self.parse_item_2(response)



        title = xp('.//h1[@id="article-content-title"]/text()').extract_first('') or \
                self.get_page_title(response).split('_')[0]

        origin_name = source_div.xpath('./span[@class="source fl-l"]/text()').extract_first()
        content, media, videos, video_cover = self.content_clean_cd(content_div)

        if "责任编辑：" not in content:
            tail_divs = xp('//div[contains(text(), "责任编辑：")]') or xp('//div/p[contains(text(), "责任编辑：")]/parent::div')
            if tail_divs:
                content += self.content_clean(tail_divs[0])[0]

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_2(self, response):
        # http://gjly.chinadevelopment.com.cn/lyhn/lygw/2019/03/1473006.shtml
        xp = response.xpath
        try:
            content_div = xp('.//div[contains(@class,"show_box_m")]')[0]
            source_div = xp('.//p[@class="show_box_info"]')[0]
            pubtime = source_div.xpath('./span[1]/text()').extract_first('').strip()
        except:
            return self.parse_item_3(response)



        title = xp('.//div[@class="show_box"]/h1/text()').extract_first('') or self.get_page_title(response).split('_')[
            0]

        origin_name = source_div.xpath('./span[2]/text()').extract_first().replace('-中国发展网', '').strip()
        content, media, videos, video_cover = self.content_clean_cd(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_3(self, response):
        # http://slgj.chinadevelopment.com.cn/xwzx/dslx/2019/0117/1443124.shtml
        xp = response.xpath
        try:
            content_div = xp('.//div[contains(@class,"am-container")]/div[@class="content"]')[0]
            source_div = xp('.//div[@class="rqly"]/text()')[0]
            st = source_div.extract().split('来源：')
            pubtime = st[0].strip()
            origin_name = st[1].strip()
        except:
            return self.parse_item_4(response)



        title = xp('.//div[@class="tips"]/h1/text()').extract_first('') or self.get_page_title(response).split('_')[0]
        content, media, videos, video_cover = self.content_clean_cd(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_4(self, response):
        # http://xyjj.chinadevelopment.com.cn/xxczh/snfz/2019/04/1489339.shtml
        xp = response.xpath
        try:
            source_div = xp('//div[@class="con_time"]/text()')[0]  # 2019-04-09 13:34     中国发展网
            pubtime = source_div.re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')[0]
            origin_name = source_div.extract().split()[-1].strip()
            content_div = xp('//div[@class="content article-content"]')[0]
        except:
            return self.parse_item_5(response)



        title = xp('.//div[@class="con_title"]/h1/text()').extract_first('') or \
                self.get_page_title(response).split('_')[0]
        content, media, videos, video_cover = self.content_clean_cd(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_5(self, response):
        # http://special.chinadevelopment.com.cn/2019zt/ztfy/2019/04/1479898.shtml
        xp = response.xpath
        try:
            source_text = xp('//p[@class="subtitle"]/text()')[
                0].extract()  # 2019-04-03  中国发展网
            ss = source_text.split()
            pubtime = ss[0]
            origin_name = ss[-1] if len(ss) >= 2 else ""
            content_div = xp('//div[@class="article"]')[0]
        except:
            return self.parse_item_6(response)



        title = self.get_page_title(response).split('_')[0]
        content, media, videos, video_cover = self.content_clean_cd(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

    def parse_item_6(self, response):
        # http://aqzg.chinadevelopment.com.cn/jryw/2019/0411/1491111.shtml
        xp = response.xpath
        try:
            # '2019-04-11 10:55\xa0\xa0\xa0\xa0来源：人民日报\xa0\xa0\xa0\xa0'
            source_div = xp('//div[@class="txtbox"]/div[@class="rqly"]/text()')[0]
            pubtime = source_div.re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')[0]
            origin_name = source_div.extract().split()[-1]
            content_div = xp('//div[@class="text_con"]//div[@class="box_con"]')[0]
        except:
            return self.parse_item_7(response)



        title = self.get_page_title(response).split('_')[0]
        content, media, videos, video_cover = self.content_clean_cd(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def parse_item_7(self, response):
        # http://special.chinadevelopment.com.cn/2019zt/2019lt/2019/01/1448145.shtml
        xp = response.xpath
        try:
            source_txt = xp('//p[@class="am-article-meta am-text-center"]/text()')[0].extract().split()
            pubtime = source_txt[0]
            origin_name = source_txt[-1] if len(source_txt) > 1 else ""
            content_div = xp('//div[@class="am-article-bd"]')[0]
            # //div[@class='am-container content']/article[@class="am-article"]/div[@class="am-article-bd"]
        except:
            return self.produce_debugitem(response, "xpath error")

        title = self.get_page_title(response).split('_')[0]
        content, media, videos, video_cover = self.content_clean_cd(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )
    
    def content_clean_cd(self, content_div, need_video=False, kill_xpaths=None):
        # 中国发展网都过滤 摘要
        # 校验sql  db.getCollection('news_all_local_debug').find({content:{$regex:"摘要："}})
        kill_xpaths = to_list(kill_xpaths) + [r'//p/*[starts-with(text(), "摘要：")]/parent::p/parent::div']
        return super(ChinadevelopmentAllSpider, self).content_clean(content_div, need_video=need_video, kill_xpaths=kill_xpaths)


        # 4月17  暂停抓取 2783 3013但已打标
# class ChinadevelopmentAllVSpider(ChinadevelopmentAllSpider):
#     """中国发展网"""
#     name = 'chinadevelopment_allv'
#
#     mystart_urls = {
#         'http://dfmg.chinadevelopment.com.cn/mlss/': 2783,
#         'http://app.chinadevelopment.com.cn/tags.php?tag=%E5%B0%8F%E5%BE%AE%E4%BC%81%E4%B8%9A': 3013,
