# -*- coding:utf-8 -*-

import json
from news_all.spider_models import NewsRSpider


class RmrbsnVSpider(NewsRSpider):
    """人民日报少年网 视频"""
    name = "rmrbsn_video"

    mystart_urls = {"https://www.rmrbsn.cn/getTopicArticleByType?topicId=8": 3882}

    def parse(self, response):
        j_data = json.loads(response.text)
        for v_data in j_data["eightArticles"]:
            try:
                news_url = v_data.get("url")
                content_div = v_data["content"]
                content, media, videos, _ = self.content_clean(content_div, need_video=True, kill_xpaths=[
                    '//*[contains(text(),"欢迎全国中小学生向人民日报少年客户端投稿")]/following::*',
                    '//*[contains(text(),"欢迎全国中小学生向人民日报少年客户端投稿")]'])
                yield self.produce_item(response=response,
                                        title=v_data["title"],
                                        pubtime=v_data["ptime"],
                                        origin_name=v_data["resource"],
                                        content=content,
                                        media=media,
                                        videos=videos,
                                        srcLink=news_url)
            except:
                yield self.produce_debugitem(response, 'json error', srcLink=news_url)
