# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.spider_models import NewsRCSpider


class MmymwwSpider(NewsRCSpider):
    '''莫名苑美文网'''
    name = 'mmymww'
    mystart_urls = {
        "http://www.szwj72.cn/t/shuqingsanwen/": 1339, # 网站-商业网站-莫名苑美文网-美文摘抄-最新抒情散文
        "http://www.szwj72.cn/t/aiqingsanwen/": 1513, # 网站-商业网站-莫名苑美文网-美文摘抄-爱情散文
        "http://www.szwj72.cn/t/youmeisanwen/": 1664, # 网站-商业网站-莫名苑美文网-美文摘抄-优秀散文
        "http://www.szwj72.cn/t/renshengganwu/": 1682, # 网站-商业网站-莫名苑美文网-美文摘抄-人生感悟
        "http://www.szwj72.cn/t/qingganmeiwen/": 1684, # 网站-商业网站-莫名苑美文网-美文摘抄-情感散文
        "http://www.szwj72.cn/t/shanggansanwen/": 1686, # 网站-商业网站-莫名苑美文网-美文摘抄-伤感散文
        "http://www.szwj72.cn/t/weixiaoshuo/": 1687, # 网站-商业网站-莫名苑美文网-美文摘抄-伤感爱情小说
        "http://www.szwj72.cn/t/zheli/": 1845, # 网站-商业网站-莫名苑美文网-美文摘抄-哲理语句
        "http://www.szwj72.cn/Article/gwsh/Index.html": 1861, # 网站-商业网站-莫名苑美文网-散文随笔-感悟生活
        "http://www.szwj72.cn/Article/aqzw/Index.html": 1871, # 网站-商业网站-莫名苑美文网-散文随笔-爱情滋味
        "http://www.szwj72.cn/Article/zaqq/Index.html": 1873, # 网站-商业网站-莫名苑美文网-散文随笔-挚爱亲情
        "http://www.szwj72.cn/Article/yqtd/Index.html": 2127, # 网站-商业网站-莫名苑美文网-散文随笔-友情天地
        "http://www.szwj72.cn/Article/qcxy/Index.html": 2128, # 网站-商业网站-莫名苑美文网-散文随笔-青春校园
        "http://www.szwj72.cn/article/hywy/Index.html": 2129, # 网站-商业网站-莫名苑美文网-散文随笔-婚姻物语
        "http://www.szwj72.cn/essay/cszd/Index.html": 2130, # 网站-商业网站-莫名苑美文网-杂文侃谈-处世之道
        "http://www.szwj72.cn/essay/yssp/Index.html": 2131, # 网站-商业网站-莫名苑美文网-杂文侃谈-影视书评
        "http://www.szwj72.cn/essay/shts/Index.html": 2132, # 网站-商业网站-莫名苑美文网-杂文侃谈-生活贴士
        "http://www.szwj72.cn/essay/xljt/Index.html": 2133, # 网站-商业网站-莫名苑美文网-杂文侃谈-心灵鸡汤
        "http://www.szwj72.cn/essay/xyxx/Index.html#": 2134, # 网站-商业网站-莫名苑美文网-杂文侃谈-心语星象
        "http://www.szwj72.cn/essay/jdyl/Index.html": 2136, # 网站-商业网站-莫名苑美文网-杂文侃谈-经典语录
        "http://www.szwj72.cn/essay/shige/Index.html": 2137, # 网站-商业网站-莫名苑美文网-杂文侃谈-诗歌大全
        "http://www.szwj72.cn/t/qingganmeiwen/Index.html": 2138, # 网站-商业网站-莫名苑美文网-情感美文
        "http://www.szwj72.cn/essay/weixiaoshuo/Index.html": 2140, # 网站-商业网站-莫名苑美文网-伤感爱情
        "http://www.szwj72.cn/aiqing/qinggan/Index.html": 2142, # 网站-商业网站-莫名苑美文网-情感
        "http://www.szwj72.cn/aiqing/qinggangushi/Index.html": 2143, # 网站-商业网站-莫名苑美文网-爱情故事
    }
    rules = (
        # http://www.szwj72.cn/Article/hsyy/201907/3414.html
        Rule(LinkExtractor(allow=(r'szwj72.cn/Article/[a-z]+/\d{6}/\d{4}\.html',),
                           ), callback='parse_item',
             follow=False),
    )
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp("//h1[@class='article-title']/a/text()").extract_first() or self.get_page_title(response)
            # pubtime = xp("//span[@class='item'][1]/text()").extract_first()
            #
            #
            origin_name = xp("//span[@class='item'][2]/a/text()").extract_first()
            content_div = xp("//article[@class='article-content']")[0]

        except:
            return self.produce_debugitem(response, 'xpath error')

        content, media, videos, video_cover = self.content_clean(content_div,kill_xpaths=["//article[@class='article-content']/p[last() - position() <= 4]",# 作者信息和声明
                                                                                          "//div[@class='alert alert-warning alert-dismissible']",# 版权
                                                                                          "//div[@class='list-group']",# 上一页和下一页标签
                                                                                          "//div[@class='am-list-news am-list-news-default xg']",#相关推荐
                                                                                          ])
        return self.produce_item(
            response=response,
            title=title,
            # self.get_page_title(response).split('_')[0]
            pubtime=datetime.now(),
            origin_name=origin_name,
            content=content,
            media=media
        )
