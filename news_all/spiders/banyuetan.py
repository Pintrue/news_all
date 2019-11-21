# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider
from datetime import datetime
from news_all.tools.time_translater import Pubtime
import re
import json

class Banyuetan(NewsRCSpider):
    """半月谈"""
    name = 'banyuetan'

    mystart_urls = {
        'http://www.banyuetan.org/': 5350,
        'http://www.banyuetan.org/byt/jinritan/index.html': 5352,
        'http://www.banyuetan.org/byt/shizhengjiangjie/index.html': 5356,
        'http://www.banyuetan.org/byt/banyuetanpinglun/index.html': 5357,
        'http://www.banyuetan.org/byt/jicengzhili/index.html': 5358,
        'http://www.banyuetan.org/byt/kaoshifuwu/index.html': 5359,
        'http://www.banyuetan.org/byt/wenhua/index.html': 5363,
        'http://www.banyuetan.org/byt/jiaoyu/index.html': 5369,
        'http://www.banyuetan.org/byt/jingji/index.html': 5370,
        'http://www.banyuetan.org/byt/zllb/index.html': 5371,
        'http://www.banyuetan.org/byt/renwu/index.html': 5372,
        'http://www.banyuetan.org/byt/junshi/index.html': 5374,
        'http://www.banyuetan.org/byt/lvyou/index.html': 5375,
        'http://www.banyuetan.org/byt/sixiang/index.html': 5376,
        'http://www.banyuetan.org/byt/difangguancha/index.html': 5377,
        'http://www.banyuetan.org/byt/jiemachengshi/index.html': 5379,
        'http://www.banyuetan.org/byt/ldqishinian/index.html': 5380,
        'http://www.banyuetan.org/byt/guoji/index.html': 5381,
        'http://www.banyuetan.org/byt/keji/index.html': 5382,
        'http://www.banyuetan.org/byt/shengtai/index.html': 5383,
        'http://www.banyuetan.org/byt/jiankang/index.html': 5384,
        'http://www.banyuetan.org/byt/minshenghuati/index.html': 5385,
        'http://www.banyuetan.org/byt/tupiangushi/index.html': 5386,
        'http://www.banyuetan.org/byt/dangjian/index.html': 5387,
        'http://www.banyuetan.org/byt/xiangcunzhenxing/index.html': 5388,
        'http://www.banyuetan.org/byt/jingzhunfupin/index.html': 5389,

    }

    rules = (
        # http://www.banyuetan.org/jy/detail/20191022/1000200033136041571709364819495308_1.html
        # http://www.banyuetan.org/xszg/detail/20191022/1000200033137251571705903434482250_1.html
        Rule(LinkExtractor(allow=r'.banyuetan.org/\w+/\w+/%s\d{2}/\w+\.html' % datetime.today().strftime('%Y%m'),),
             callback='parse_item',
             follow=False),

        # http://www.banyuetan.org/tpgs/byt/detail/image/20191015/1000200033136181571103305744311819_1.html
        Rule(LinkExtractor(allow=r'.banyuetan.org/\w+/\w+/\w+/\w+/%s\d{2}/\w+\.html' % datetime.today().strftime('%Y%m'), ),
             callback='parse_item_2',
             follow=False),
    )


    def parse_item(self, response):
        # http://www.banyuetan.org/yw/detail/20191022/1000200033137441571705027341468427_1.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='detail_tit']/h1/text()").extract_first()
            pubtime = Pubtime(xp("//div[@class='detail_tit_time']/text()").extract_first())
            content_div = xp("//div[@class='detail_content']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)
            origin_name = xp("//div[@class='detail_tit_source']/text()").extract_first()
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,
        )

    def parse_item_2(self, response):
        # http://www.banyuetan.org/tpgs/byt/detail/image/20191015/1000200033136181571103305744311819_1.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='img_title']/h3[@id='imgTitle']/text()").extract_first()
            pubtime = xp("//meta[@name='publishdate']/@content").get()
            origin_name = xp("//li[@class='source']/em/text()").extract_first()
            news_div = xp("//head/script[2]").extract_first().strip()
            content_div = news_div.replace("\r\n","")
            param = re.findall("(?<=imgInfo=).*?(?=;)", content_div)[0]
            news = json.loads(param)
            imgs = news.get("list")
            content, media = make_img_content(imgs)

        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
        )


def make_img_content(img_cons):
    """拼接json中图、文列表为html
    :param img_cons list
    """
    media = {'images': {}}
    content = ''
    for i, j in enumerate(img_cons):
        content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
        img_url = j.get('img')
        media['images'][str(i + 1)] = {"src": img_url}
        if j.get('note'):
            content += '<p>' + j['note'] + '</p>'
    return content, media