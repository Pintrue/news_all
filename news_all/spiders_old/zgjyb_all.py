# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class Zgjyb_allSpider(NewsRCSpider):
    """中国教育报"""
    name = 'zgjyb'
    mystart_urls = {
        'http://www.jyb.cn/list_gjjy/': 1301606,  # 中国教育报-国际教育-左下列表
        'http://www.jyb.cn/list_jcjy/': 1301607,  # 中国教育报-基础教育-左下列表和右上最新发布
        'http://www.jyb.cn/list_xqjy/': 1301611,  # 中国教育报-学前教育-左下列表
        'http://www.jyb.cn/list_jtjy/': 1301608,  # 中国教育报-家庭教育-左下列表
        'http://www.jyb.cn/list_llzk/': 1301610,  # 中国教育报-思想理论-左下列表
        'http://www.jyb.cn/list_mzjy/': 1301609,  # 中国教育报-民族教育
        'http://www.jyb.cn/sy/zhxw/': 1301613,  # 中国教育报-综合新闻
        'http://www.jyb.cn/list_zyjy/': 1301612,  # 中国教育报-职业教育-左下列表
        'http://www.jyb.cn/list_gdjy/': 1301605,  # 中国教育报-高等教育-左下列表

    }
    rules = (
        # http://www.jyb.cn/zcg/xwy/wzxw/201811/t20181125_1267665.html
        # http://www.jyb.cn/zcg/xwy/wzxw/201811/t20181105_1258222.html
        # http://www.jyb.cn/zcg/xwy/wzxw/201811/t20181123_1267036.html
        #http://www.jyb.cn/zgjyb/201811/t20181126_1267919.html
        #http://www.jyb.cn/zgjyb/201811/t20181125_1267620.html
        #http://www.jyb.cn/zgjyb/201811/t20181122_1266320.html
        #http://www.jyb.cn/zgjyb/201811/t20181126_1267896.html
        #http://www.jyb.cn/zgjyb/201811/t20181120_1265138.html
        #http://www.jyb.cn/zgjyb/201811/t20181126_1267907.html

        # http://www.jyb.cn/zcg/xwy/wzxw/201811/t20181125_1267665.html
        Rule(LinkExtractor(allow=(r'jyb.cn/zcg/xwy/wzxw/\d{6}/t\d+_\d+.html' ),
                           ), callback='parse_item',
             follow=False),

        Rule(LinkExtractor(allow=(r'jyb.cn/zgjyb/\d{6}/t\d+_\d+.html'),
                           ), callback='parse_item',
             follow=False),

    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//div[@class='xl_title']/text()").extract_first()
            content_div = xp("//div[@class='xl_text']")[0]

            pubtime = xp("//div[@class='xl_title']/h2/span[1]").re(r'\d{2,4}-\d{1,2}-\d{1,2}')[0]
            # pubtime = xp("//div[@class='Remark']/span/text()").extract_first().split('|')[0]
            
                
            origin_name =xp('//div[@class="xl_title"]/h2/span[@id="js_source"]/text()').extract_first('')
        except:
            return self.produce_debugitem(response, "xpath error")
            # return self.parse_item_2(response)

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
