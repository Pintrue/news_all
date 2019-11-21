# -*- coding: utf-8 -*-
# @Time   : 2019/8/26 下午4:15
# @Author : NewmanZhou
# @Project : news_all
# @FileName: jksb_video.py


import random
from jsonpath import jsonpath

from news_all.spider_models import NewsRCSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from datetime import datetime
import os
import requests
import time
import re
from news_all.tools.agents import USER_AGENTS
from news_all.tools.html_clean import get_query_map

CCODE = '0521'
YKAPI = "https://ups.youku.com/ups/get.json?vid={vid}&ccode={ccode}&client_ip=192.168.1.1&client_ts={client_ts}&utid={utid}"
UTID = "giyYEr+fQ0gCAXbPYiKva2h5"


class JksbVideoSpider(NewsRCSpider):
    """健康时报 视频"""
    name = 'jksb_video'

    mystart_urls = {
        'http://www.jksb.com.cn/html/video/daifusay/': 3861,  # 健康时报_视频
    }

    # http://www.jksb.com.cn/html/2019/daifusay_0823/140279.html
    rules = (
        Rule(LinkExtractor(allow=(r'jksb.com.cn/html/%s/daifusay_\d{4}/\d+.html') % datetime.today().strftime('%Y'),
                           ), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        xp = response.xpath
        try:
            origin_name = xp('//div[@class="info"]/span[2]/a/text()').extract_first()
            title = xp('//h1[@class="title"]/text()').extract_first()
            pubtime = xp('//div[@class="info"]/span[1]/text()').extract_first()

            src = xp('//div[@id="content"]//iframe/@src').extract()[0]
            if get_query_map(src)["netloc"] == "player.youku.com":
                video_url = get_youku_video(os.path.basename(src), UTID)
            else:
                video_url = src

            content_div = xp('//div[@id="content"]').extract()
            content, media, _, _ = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")
        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content='<p>#{{1}}#</p>' + content,
            media=media,
            videos={'1': {'src': video_url}},
        )


def get_utid():
    try:
        res = requests.get('https://log.mmstat.com/eg.js')
        return re.search(r'Etag="(.+?)"', res.text).group(1)
    except:
        return "kcrvFQMSeU0CAXx/aII4Iyhy"


def get_youku_video(vid, utid):
    url = YKAPI.format(vid=vid, ccode=CCODE, client_ts='%0.f' % time.time(), utid=utid)
    res = requests.get(url,
                       headers={"Referer": "http://player.youku.com/embed/" + vid,
                                "User-Agent": random.choice(USER_AGENTS)}
                       )
    rj = res.json()

    if jsonpath(rj, '$.data.error.note') == ["utid参数错误"]:
        return get_youku_video(vid, get_utid())
    # 取 最大的视频 $.data.stream[1].width=640  $.data.stream[1].height=360
    # print('%s X %s' % (jsonpath(rj, '$.data.stream[0].width')[0], jsonpath(rj, '$.data.stream[0].height')[0],))
    return jsonpath(rj, '$.data.stream[0].segs[0].cdn_url')[0]
