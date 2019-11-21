# -*- coding: utf-8 -*-

from news_all.tools.time_translater import timestamps
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class diyijuzispider(NewsRCSpider):
    name = 'diyijuzi'
    mystart_urls = {
        "https://www.diyijuzi.com/weimei/": 2862,  # 网站-商业网站-第一句子网-唯美的句子
        "https://www.diyijuzi.com/zheli/": 2864,  # 网站-商业网站-第一句子网-哲理的句子
        "https://www.diyijuzi.com/aiqing/": 2866,  # 网站-商业网站-第一句子网-爱情的句子
        "https://www.diyijuzi.com/xinsui/": 2867,  # 网站-商业网站-第一句子网-心碎的句子
        "https://www.diyijuzi.com/xinfan/": 2868,  # 网站-商业网站-第一句子网-心烦的句子
        "https://www.diyijuzi.com/anlian/": 2869,  # 网站-商业网站-第一句子网-暗恋的句子
        "https://www.diyijuzi.com/shiwang/": 2870,  # 网站-商业网站-第一句子网-失望的句子
        "https://www.diyijuzi.com/xiangni/": 2871,  # 网站-商业网站-第一句子网-想你的句子
        "https://www.diyijuzi.com/maren/": 2872,  # 网站-商业网站-第一句子网-骂人的句子
        "https://www.diyijuzi.com/shuqing/": 2873,  # 网站-商业网站-第一句子网-抒情的句子
        "https://www.diyijuzi.com/youmei/": 2874,  # 网站-商业网站-第一句子网-优美的句子
        "https://www.diyijuzi.com/lizhi/": 2875,  # 网站-商业网站-第一句子网-励志的句子
        "https://www.diyijuzi.com/youqing/": 2876,  # 网站-商业网站-第一句子网-友情的句子
        "https://www.diyijuzi.com/xinsuan/": 2877,  # 网站-商业网站-第一句子网-心酸的句子
        "https://www.diyijuzi.com/xinlei/": 2878,  # 网站-商业网站-第一句子网-心累的句子
        "https://www.diyijuzi.com/shilian/": 2880,  # 网站-商业网站-第一句子网-失恋的句子
        "https://www.diyijuzi.com/wunai/": 2881,  # 网站-商业网站-第一句子网-无奈的句子
        "https://www.diyijuzi.com/xiangjia/": 2882,  # 网站-商业网站-第一句子网-想家的句子
        "https://www.diyijuzi.com/gaoxiao/": 2883,  # 网站-商业网站-第一句子网-搞笑的句子
        "https://www.diyijuzi.com/shiyi/": 2884,  # 网站-商业网站-第一句子网-诗意的句子
        "https://www.diyijuzi.com/shanggan/": 2885,  # 网站-商业网站-第一句子网-伤感的句子
        "https://www.diyijuzi.com/jingdian/": 2886,  # 网站-商业网站-第一句子网-经典的句子
        "https://www.diyijuzi.com/qinqing/": 2887,  # 网站-商业网站-第一句子网-亲情的句子
        "https://www.diyijuzi.com/xintong/": 2888,  # 网站-商业网站-第一句子网-心痛的句子
        "https://www.diyijuzi.com/xinjing/": 2889,  # 网站-商业网站-第一句子网-心静的句子
        "https://www.diyijuzi.com/biaobai/": 2890,  # 网站-商业网站-第一句子网-表白的句子
        "https://www.diyijuzi.com/nanguo/": 2891,  # 网站-商业网站-第一句子网-难过的句子
        "https://www.diyijuzi.com/sinian/": 2892,  # 网站-商业网站-第一句子网-思念的句子
        "https://www.diyijuzi.com/xianshi/": 2893,  # 网站-商业网站-第一句子网-现实的句子
        "https://www.diyijuzi.com/huiyi/": 2894,  # 网站-商业网站-第一句子网-回忆的句子
        "https://www.diyijuzi.com/": 2895,  # 网站-商业网站-第一句子网-网站首页
        "https://www.diyijuzi.com/renshengganwu/": 2896,  # 网站-商业网站-第一句子网-人生感悟的句子
        "https://www.diyijuzi.com/zhengnengliang/": 2897,  # 网站-商业网站-第一句子网-正能量的句子
        "https://www.diyijuzi.com/chanyu/": 2898,  # 网站-商业网站-第一句子网-佛家经典禅语
        "https://www.diyijuzi.com/shangxin/": 2899,  # 网站-商业网站-第一句子网-伤心的句子
        "https://www.diyijuzi.com/houhui/": 2900,  # 网站-商业网站-第一句子网-后悔的句子
        "https://www.diyijuzi.com/ganren/": 2901,  # 网站-商业网站-第一句子网-感人的句子
        "https://www.diyijuzi.com/miaoxie/": 2902,  # 网站-商业网站-第一句子网-描写类句子
        "https://www.diyijuzi.com/taici/": 2903,  # 网站-商业网站-第一句子网-经典台词
        "https://www.diyijuzi.com/shuoshuo/": 2904,  # 网站-商业网站-第一句子网-说说大全
    }
    
    rules = (
        Rule(LinkExtractor(allow=(r'diyijuzi.com/.*?/\d+.html'), deny=r'666n.com/html'),
             callback='parse_item', follow=False),
    )
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//div[@class="content"]/h1/text()').extract()[0]
            # pubtime = xp('//div[@class="info"]/span/text()').extract()[1].strip()
            cv = xp("//div[@class='nr' or @class='con']")[0]
            content, media, _, _ = self.content_clean(cv)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=timestamps(),
            content=content,
            media=media,
        )
