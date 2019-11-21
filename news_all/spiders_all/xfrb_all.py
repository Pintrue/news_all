# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class XfrbAllSpider(NewsRCSpider):
    """消费日报网"""
    name = 'xfrb_all'
    mystart_urls = {

               'http://www.xfrb.com.cn/html/rdjj/zuixinzixun/': 1895,
               'http://www.xfrb.com.cn/html/baixingshichuang/tuijiantoutiao/': 1896,
               'http://www.xfrb.com.cn/html/baixingshichuang/xinwenzixun/': 1897,
               'http://www.xfrb.com.cn/html/baixingshichuang/gaoduanfangtan/': 1898,
               'http://www.xfrb.com.cn/html/baixingshichuang/minshengguanzhu/': 1899,
               'http://www.xfrb.com.cn/html/baixingshichuang/jiaotidianshang/': 1900,
               'http://www.xfrb.com.cn/html/baixingshichuang/fangchanloushi/': 1901,
               'http://www.xfrb.com.cn/html/baixingshichuang/nenyuankeji/': 1902,
               'http://www.xfrb.com.cn/html/baixingshichuang/shipinanquan/': 1903,
               'http://www.xfrb.com.cn/html/baixingshichuang/qichemingpin/': 1904,
               'http://www.xfrb.com.cn/html/baixingshichuang/shishangyule/': 1905,
               'http://www.xfrb.com.cn/html/baixingshichuang/shumalicai/': 1906,
               'http://www.xfrb.com.cn/html/baixingshichuang/yiliaojiankang/': 1907,
               'http://www.xfrb.com.cn/html/baixingshichuang/jiadianjiaji/': 1908,
               'http://www.xfrb.com.cn/html/baixingshichuang/lvyoumeishi/': 1909,
               'http://www.xfrb.com.cn/html/baixingshichuang/gongyicishan/': 1910,
               'http://www.xfrb.com.cn/html/baixingshichuang/yishushoucang/': 1911,
               'http://www.xfrb.com.cn/html/guanzhu/shengtaijujiao/shengtaishipin/': 1912,
               'http://www.xfrb.com.cn/html/guanzhu/shehuiguanzhu/xiaofeiredian/': 1913,
               'http://www.xfrb.com.cn/html/guanzhu/shehuiguanzhu/jiajishenghuo/': 1914,
               'http://www.xfrb.com.cn/html/guanzhu/shehuiguanzhu/chanyezaixian/': 1915,
               'http://www.xfrb.com.cn/html/shichang/shangchao/': 1916,
               'http://www.xfrb.com.cn/html/shichang/dianshang/': 1917,
               'http://www.xfrb.com.cn/html/shichang/zhixiao/': 1918,
               'http://www.xfrb.com.cn/html/lvyouwenchuang/lvyou/': 1919,
               'http://www.xfrb.com.cn/html/lvyouwenchuang/wenchuang/': 1920,
               'http://www.xfrb.com.cn/html/lvyouwenchuang/jiaoyu/': 1921,
               'http://www.xfrb.com.cn/html/lvyouwenchuang/licai/': 1922,

    }

    # http://www.xfrb.com.cn/html/rdjj/zuixinzixun/505117.html     hhttp://www.xfrb.com.cn/html/zixun/redianjujiao/list_769_1.html

    rules = (
        Rule(LinkExtractor(allow=(r'xfrb.com.cn/.*?/.*?/\d+.html'), ),
                           callback='parse_item', follow=False),
        # Rule(LinkExtractor(allow=(r'cnr\.cn/.*?t\d+_\d+\.s?html',),
        #                    deny=(r'\.cnr\.cn/native/city/', r'\.cnr\.cn/(?:js2014/)?jssp',)),
        #      callback='parse_urls', follow=False),

    )
    # http://www.xfrb.com.cn/html/rdjj/zuixinzixun/505117.html
    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="content_left"]')[0]
            source_div = news_div.xpath('./h3')[0]
            content_div = news_div.xpath('./div[@class="content_div"]')[0]

            time_re = source_div.re(r'\d{2,4}-\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0] if time_re else ''
        except:
            return self.produce_debugitem(response, "xpath error")

        title = ''.join(i.strip() for i in news_div.xpath('./div[@class="title"]/text()').extract())

        content, media, videos, video_cover = self.content_clean(content_div)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            content=content,
            media=media
        )

