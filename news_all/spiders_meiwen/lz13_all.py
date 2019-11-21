#!/usr/bin/env python 
# -*- coding:utf-8 _*-  
# Time: 2019/07/26
# Author: zcy

import re
from datetime import datetime
from copy import deepcopy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.conf import settings
from news_all.spider_models import NewsRCSpider


class ChickenSoupSpider(NewsRCSpider):
    """励志一生"""
    name = 'lz13_all'
    mystart_urls = {
        'https://www.lz13.cn/lizhi/lizhiwenzhang.html': 2414,  # 网站-商业网站-励志一生-励志文章
        'https://www.lz13.cn/lizhi/lizhigushi.html': 2427,  # 网站-商业网站-励志一生-励志故事
        'https://www.lz13.cn/lizhi/lizhimingyan.html': 2429,  # 网站-商业网站-励志一生-励志名言
        'https://www.lz13.cn/lizhi/lizhidianying.html': 2431,  # 网站-商业网站-励志一生-励志电影
        'https://www.lz13.cn/lizhi/renshengganwu.html': 2434,  # 网站-商业网站-励志一生-人生感悟
        'https://www.lz13.cn/lizhi/jingdianyulu.html': 2436,  # 网站-商业网站-励志一生-经典语录
        'https://www.lz13.cn/lizhi/zhichanglizhi.html': 2438,  # 网站-商业网站-励志一生-职场励志
        'https://www.lz13.cn/lizhi/qingchunlizhi.html': 2440,  # 网站-商业网站-励志一生-青春励志
        'https://www.lz13.cn/lizhi/weirenchushi.html': 2442,  # 网站-商业网站-励志一生-为人处世
        'https://www.lz13.cn/lizhi/lizhiyanjiang.html': 2444,  # 网站-商业网站-励志一生-励志演讲
        'https://www.lz13.cn/lizhi/meiwen.html': 2446,  # 网站-商业网站-励志一生-经典美文
        'https://www.lz13.cn/lizhi/lizhikouhao.html': 2447,  # 网站-商业网站-励志一生-励志口号
        'https://www.lz13.cn/lizhi/lizhijiaoyu.html': 2448,  # 网站-商业网站-励志一生-励志教育
        'https://www.lz13.cn/lizhi/daxueshenglizhi.html': 2449,  # 网站-商业网站-励志一生-大学生励志
        'https://www.lz13.cn/lizhi/chenggonglizhi.html': 2450,  # 网站-商业网站-励志一生-成功励志
        'https://www.lz13.cn/lizhi/lizhirenwu.html': 2451,  # 网站-商业网站-励志一生-励志人物
        'https://www.lz13.cn/lizhi/mingrenmingyan.html': 2452,  # 网站-商业网站-励志一生-名人名言
        'https://www.lz13.cn/lizhi/lizhigequ.html': 2453,  # 网站-商业网站-励志一生-励志歌曲
        'https://www.lz13.cn/lizhi/zheli.html': 2601,  # 网站-商业网站-励志一生-人生哲理
        'https://www.lz13.cn/lizhi/jingdianyuduan.html': 2604,  # 网站-商业网站-励志一生-经典句子
        'https://www.lz13.cn/lizhi/lizhichuangye.html': 2606,  # 网站-商业网站-励志一生-励志创业
        'https://www.lz13.cn/lizhi/gaosanlizhi.html': 2608,  # 网站-商业网站-励志一生-高三励志
        'https://www.lz13.cn/lizhi/jiatingjiaoyu.html': 2611,  # 网站-商业网站-励志一生-家庭教育
        'https://www.lz13.cn/lizhi/ganenlizhi.html': 2612,  # 网站-商业网站-励志一生-感悟亲情
        'https://www.lz13.cn/lizhi/shanggan.html': 2614,  # 网站-商业网站-励志一生-伤感日志
        'https://www.lz13.cn/lizhi/lizhishuji.html': 2616,  # 网站-商业网站-励志一生-励志书籍
        'https://www.lz13.cn/lizhi/lizhishige.html': 2619,  # 网站-商业网站-励志一生-励志诗歌
        'https://www.lz13.cn/lizhi/lizhijiangxuejin.html': 2621,  # 网站-商业网站-励志一生-励志奖学金
    }

    rules = (
        Rule(LinkExtractor(allow=r'lz13.cn/.*/\d+.html'),
             callback='parse_item',
             follow=False
             ),
    )

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': deepcopy(settings.getdict('DOWNLOADER_MIDDLEWARES_NOREDICT'))
    }

    def parse_item(self, response):
        xp = response.xpath
        try:
            title = xp('//div[@class="PostHead"]/h2/text()').extract_first()
            # head_info = xp('//span[@class="submitted"]').extract_first()
            # pubdate = re.findall('\d{4}/\d+/\d+', head_info)
            # pubtime = ''
            # if len(pubdate) == 0:
            #     pubmonth = xp('//div[@class="post_month"]/text()').extract_first().strip()
            #     pubmonth = list(calendar.month_abbr).index(pubmonth)
            #     pubday = xp('//div[@class="post_day"]/text()').extract_first().strip()
            #     pubtime = '%s/%s' % (pubmonth, pubday)
            # else:
            #     pubtime = pubdate[0] + ' ' + re.findall('\d{2}:\d{2}', head_info)[0]
    
            content_div = xp('//div[@class="PostContent"]/p')
            content, media, _, _ = self.content_clean(content_div, kill_xpaths=[])  # todo why '//div[@class="PostContent"]/p[position()<3]' 没kill掉
        except:
            return self.produce_debugitem(response, 'xpath error')

        yield self.produce_item(
            response=response,
            title=title,
            pubtime=datetime.now(),
            origin_name='励志一生',
            content=content,
            media=media
        )