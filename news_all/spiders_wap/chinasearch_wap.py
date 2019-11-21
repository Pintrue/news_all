#-*- coding:utf-8 -*-
# @Time    : 2019/7/15 14:29
# @Author  : zxy
# @File    : chinasearch_wap.py

import re
import json
from datetime import datetime
from scrapy import Request
from scrapy.conf import settings
from news_all.spider_models import NewsRSpider
from news_all.tools.html_clean import get_query_map


base_api = "http://mobapp.chinaso.com/1/category/newsDetailHtml?type=wap&extra=norecmd&jsonpcallback=getContent&nid={}&contentId=null"
CHINASO_NETLOC = "m.news.chinaso.com"


class QiushiSpider(NewsRSpider):
    chinese_name = """中国搜索app"""
    name = 'chinasearch_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
                    "http://mob.chinaso.com/1/news/list?id=3294&page=0":3461,
                    "http://mob.chinaso.com/1/news/list?id=all&page=0":3462,
                    "http://mob.chinaso.com/1/news/list?id=3618532919&page=0":3463,
                    "http://mob.chinaso.com/1/news/list?id=326866&page=0":3464,
                    "http://mob.chinaso.com/1/news/list?id=326862&page=0":3465,
                    "http://mob.chinaso.com/1/news/list?id=3283946&page=0":3466,
                    "http://mob.chinaso.com/1/news/list?id=3618495672&page=0":3467,
                    "http://mob.chinaso.com/1/news/list?id=325790&page=0":3468,
                    "http://mob.chinaso.com/1/news/list?id=3271500&page=0":3469,
                    "http://mob.chinaso.com/1/news/list?id=326864&page=0":3470,
                    # "http://mob.chinaso.com/1/news/list?id=3618526360&page=0":3471,
                    "http://mob.chinaso.com/1/news/list?id=3618526362&page=0":3488,
                    "http://mob.chinaso.com/1/news/list?id=3618526364&page=0":3489,
                    "http://mob.chinaso.com/1/news/list?id=3618526360&page=0":3490,
                    "http://mob.chinaso.com/1/news/list?id=3618526358&page=0":3491,
                    "http://mob.chinaso.com/1/news/list?id=3618526357&page=0":3494,
                    "http://mob.chinaso.com/1/news/list?id=3618526356&page=0":3495,
                    "http://mob.chinaso.com/1/news/list?id=3294094&page=0":3496,
                    "http://mob.chinaso.com/1/news/list?id=3618445392&page=0":3497,
                    "http://mob.chinaso.com/1/news/list?id=3293750&page=0":3498,
                    "http://mob.chinaso.com/1/news/list?id=3288740&page=0":3499,
                    }

    base_api = "http://mobapp.chinaso.com/1/category/newsDetailHtml?type=wap&extra=norecmd&jsonpcallback=getContent&nid={}&contentId=null"
    def parse(self, response):
        rs = json.loads(response.text)
        for art_data in rs.get('list', []):
            url_query_map = get_query_map(art_data.get("url"))
            if "nid" in url_query_map["query"]:
                #parse article
                news_url = base_api.format(url_query_map["query"].get("nid"))

                title = art_data.get('title')
                origin_name = art_data.get("mname")
                meta_data = {'source_id': response.meta['source_id'], 
                      'title': title, 
                      
                      'origin_name': origin_name,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                yield Request(
                    url=news_url, 
                    callback=self.parse_item,
                    meta=meta_data)
            elif CHINASO_NETLOC == url_query_map["netloc"]:
                #article list article all from other site skip
                pass
                #url = "%s://%s%s"%(url_query_map["scheme"], url_query_map["netloc"], url_query_map["query"].get("tid"))
                #yield Request(url, callback=self.parse_article_list)
            else:
                continue            

    def parse_item(self, response):
        json_pattern = re.compile(r"getContent\((.*)\)")

        json_str = json_pattern.findall(response.text)[0]
        j_data = json.loads(json_str)
        pubtime = j_data.get('timeString')

        media = {}
        content = []
        media_index = 1
        for value in j_data["content"]:
            if "text" == value["type"]:
                content.append("<p>%s</p>"%value["value"])  # 没有图片？
            elif "image" == value["type"]:
                media.setdefault("images", {})
                content.append('<p>${{%s}}$</p>' % media_index)
                media['images'][str(media_index)] = {"src": value.get('value')}
                media_index += 1
            else:
                pass
        content = self.parser.cleaner.clean_html("".join(content))  # 再去不要的dom 和 属性
        content = content.replace('$$', '$<br>$')  # 让2图换行
        return self.produce_item(
            response=response,
            title=response.meta['title'],
            pubtime=pubtime,
            origin_name=response.meta["origin_name"],
            summary=j_data.get('summary'),
            content=content,
            media=media)
