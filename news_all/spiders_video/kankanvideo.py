# -*- coding: utf-8 -*-

import json
from news_all.spider_models import NewsRSpider
from news_all.tools.others import to_list


class KanknaVideoSpider(NewsRSpider):
    """看看新闻客户端 视频"""
    name = 'kankanvideo_wap'

    mystart_urls = {

        'http://baoliao.api.kankanews.com/kkuser/listinfo/list/appclassid/617/timestamp/0?androidver=5.4.5': 7652,

    }

    def parse(self, response):
        rj = json.loads(response.text)
        list = rj.get("list")
        for j in list:
            title = j.get("title")
            video_url = j.get("videourl")

            pubtime = j.get("newsdate")

            sharepic = j.get("sharepic")
            videos = {'1': {'src': video_url}}
            video_cover = to_list(sharepic)

            yield self.produce_item(
                response=response,
                title=title,
                pubtime=pubtime,
                # origin_name=origin_name,
                
                content='<div>#{{1}}#</div>',
                media={},
                videos=videos,
                srcLink=video_url
            )
