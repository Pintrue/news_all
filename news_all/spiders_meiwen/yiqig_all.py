#!/usr/bin/env python 
# -*- coding:utf-8 _*-  
# Time: 2019/07/26
# Author: zcy

from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider


class ChickenSoupSpider(NewsRCSpider):
    """一起感悟人生"""
    name = 'yiqig_all'
    mystart_urls = {
        'http://www.yiqig.com/': 2739,  # 主页
        'http://www.yiqig.com/zhihuirensheng/renshengganwu/': 2741,  # 智慧人生-人生感悟
        'http://www.yiqig.com/zhihuirensheng/renshengzheli/': 2747,  # 智慧人生-人生哲理
        'http://www.yiqig.com/zhihuirensheng/sixiangsiwei/': 2749,  # 智慧人生-思想思维
        'http://www.yiqig.com/zhihuirensheng/weirenchushi/': 2750,  # 智慧人生-为人处世
        'http://www.yiqig.com/zhihuirensheng/renshengsuibi/': 2752,  # 智慧人生-人生随笔
        'http://www.yiqig.com/zhichanglizhi/chenggongrensheng/': 2755,  # 职场励志-成功人生
        'http://www.yiqig.com/zhichanglizhi/lizhiwenzhang/': 2757,  # 职场励志-励志文章
        'http://www.yiqig.com/zhichanglizhi/lizhimingyan/': 2759,  # 职场励志-励志名言
        'http://www.yiqig.com/zhichanglizhi/lizhigushi/': 2761,  # 职场励志-励志故事
        'http://www.yiqig.com/zhichanglizhi/zhichangzhinan/': 2763,  # 职场励志-职场指南
        'http://www.yiqig.com/zhichanglizhi/touzilicai/': 2765,  # 职场励志-投资理财
        'http://www.yiqig.com/zhichanglizhi/qiuzhizhinan/': 2766,  # 职场励志-求职指南
        'http://www.yiqig.com/zhichanglizhi/guanliyishu/': 2768,  # 职场励志-管理艺术
        'http://www.yiqig.com/zhichanglizhi/qita/': 2770,  # 职场励志-其他
        'http://www.yiqig.com/lianaibaodian/nanhaibidu/': 2772,  # 恋爱宝典-男孩必读
        'http://www.yiqig.com/lianaibaodian/nvhaibidu/': 2773,  # 恋爱宝典-女孩必读
        'http://www.yiqig.com/lianaibaodian/aiqingwenzhang/': 2776,  # 恋爱宝典-爱情文章
        'http://www.yiqig.com/lianaibaodian/aiqingganwu/': 2777,  # 恋爱宝典-爱情感悟
        'http://www.yiqig.com/lianaibaodian/aiqingmingyan/': 2779,  # 恋爱宝典-爱情名言
        'http://www.yiqig.com/shejiaoshenghuo/qinqingganwu/': 2781,  # 社交生活-亲情感悟
        'http://www.yiqig.com/shejiaoshenghuo/shehuiganwu/': 2803,  # 社交生活-社会感悟
        'http://www.yiqig.com/shejiaoshenghuo/jiatingjiaoyu/': 2805,  # 社交生活-家庭教育
        'http://www.yiqig.com/shejiaoshenghuo/shenghuoganwu/': 2808,  # 社交生活-生活感悟
        'http://www.yiqig.com/shejiaoshenghuo/youqingganwu/': 2810,  # 社交生活-友情感悟
        'http://www.yiqig.com/jiankangrensheng/xiushenyangxing/': 2813,  # 健康人生-修身养性
        'http://www.yiqig.com/jiankangrensheng/xinlijiankang/': 2815,  # 健康人生-心理健康
        'http://www.yiqig.com/jiankangrensheng/jianfeijianmei/': 2818,  # 健康人生-减肥健美
        'http://www.yiqig.com/jiankangrensheng/yinshijiankang/': 2819,  # 健康人生-饮食健康
        'http://www.yiqig.com/mingrenmingyan/jingdianmingyan/': 2821,  # 名人名言-经典名言
        'http://www.yiqig.com/mingrenmingyan/renshenggeyan/': 2823,  # 名人名言-人生格言
        'http://www.yiqig.com/mingrenmingyan/mingrenmingyan/': 2826,  # 名人名言-名人名言
        'http://www.yiqig.com/mingrenmingyan/yingwenmingyan/': 2828,  # 名人名言-英文名言
        'http://www.yiqig.com/mingrenmingyan/zhelimingyan/': 2830,  # 名人名言-哲理名言
        'http://www.yiqig.com/mingrenmingyan/zuoyouming/': 2832,  # 名人名言-座右铭
        'http://www.yiqig.com/gurenmingyue/': 2834,  # 古人名曰
        'http://www.yiqig.com/news/': 2836,  # 最近更新
        'http://www.yiqig.com/tj/': 2838,  # 推荐文章
    }

    rules = (
        Rule(LinkExtractor(allow=r'yiqig.com/.*/.*/.*.html', deny=r'yiqig.com/.*/.*/list.*.html'),
             callback='parse_item',
             follow=False
             ),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//h1/text()').extract_first() or self.get_page_title(response).split('_')[0]
            # pubtime = xp('//div[@class="info"]/text()[2]').extract_first().strip()
            content = xp('//div[@class="content"]')[0]
            content, media, _, _ = self.content_clean(content)
        except:
            self.produce_debugitem(response, 'xpath error')
            
        yield self.produce_item(
            response=response,
            title=title,
            pubtime=datetime.now(),
            content=content,
            media=media
        )

