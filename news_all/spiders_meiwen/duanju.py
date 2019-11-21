# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class duanjuspider(NewsRCSpider):
    name = 'duanju'
    mystart_urls = {
        'https://www.duanju.cc/':2454,
        'https://www.duanju.cc/jingdian/':2602,                    # 网站-商业网站-短句网-首页
        'https://www.duanju.cc/shanggan/':2603,                    # 网站-商业网站-短句网-经典短句
        'https://www.duanju.cc/weimei/':2605,                    # 网站-商业网站-短句网-伤感短句
        'https://www.duanju.cc/gaoxiao/':2607,                    # 网站-商业网站-短句网-唯美短句
        'https://www.duanju.cc/aiqing/':2609,                    # 网站-商业网站-短句网-搞笑短句
        'https://www.duanju.cc/lizhi/':2610,                    # 网站-商业网站-短句网-爱情短句
        'https://www.duanju.cc/zheli/':2613,                    # 网站-商业网站-短句网-励志短句
        'https://www.duanju.cc/xinqing/':2615,                    # 网站-商业网站-短句网-哲理短句
        'https://www.duanju.cc/weimeijuzi/':2617,                    # 网站-商业网站-短句网-心情短句
        'https://www.duanju.cc/sanwen/':2620,                    # 网站-商业网站-短句网-唯美的句子
        'https://www.duanju.cc/renshengganwu/':2622,                    # 网站-商业网站-短句网-随笔散文
        'https://www.duanju.cc/jingdianyulu/':2695,                    # 网站-商业网站-短句网-人生感悟
        'https://www.duanju.cc/huiyijuzi/':2700,                    # 网站-商业网站-短句网-经典语录
        'https://www.duanju.cc/lizhimingyan/':2702,                    # 网站-商业网站-短句网-回忆的句子
        'https://www.duanju.cc/sinianjuzi/':2712,                    # 网站-商业网站-短句网-励志名言
        'https://www.duanju.cc/shangganrizhi/':2718,                    # 网站-商业网站-短句网-思念的句子
        'https://www.duanju.cc/youmeijuzi/':2720,                    # 网站-商业网站-短句网-伤感日志
        'https://www.duanju.cc/shangganjuzi/':2722,                    # 网站-商业网站-短句网-优美的句子
        'https://www.duanju.cc/shicimingju/':2726,                    # 网站-商业网站-短句网-伤感的句子
    }
    rules = (
        Rule(LinkExtractor(allow=(r'duanju.cc/.*?/\d+.html'),deny=r'666n.com/html'),
        callback='parse_item', follow=False),
    )

    def parse_item(self,response):
        try:
            xp = response.xpath
            title = xp('//h2[@class="wz-title"]/text()').extract_first()
            # pubtime = xp('//div[@class="wz-info"]/text()').extract()[1].replace("发布时间：",'').replace("|",'').replace(" ",'').replace("人气值：",'')
            #
            #
            cv = xp("//div[@class='wz-txtrr']")
            content,media,_,_=self.content_clean(cv)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,  # must
            title=title,
            pubtime=datetime.now(),
            origin_name='', # 没有注明作者
            content=content,
            media=media,
        )