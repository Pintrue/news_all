# -*- coding: utf-8 -*-

import json
from scrapy import FormRequest
from news_all.spider_models import *
from news_all.tools.others import to_list
from scrapy.conf import settings


class CctvchildSpider(NewsRSpider):
    """CCTV-少儿频道"""
    name = 'cctvchild_app'
    
    mystart_urls = {
        'https://api.cctv.cn/childmobileinf/rest/cctv/cardgroups': [
            3017, 3018, 3019, 3020, 3021, 3022, 3023, 3024, 3025, 3026, 3027, 3028, 3029, 3030, 3031, 3032, 3033, 3034]}
    
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    
    start_formdata_map = {
        3017: ("推荐", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                      'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1547174590780555"}'}),
        3018: ("大视界", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                       'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1547174630783556"}'}),
        3019: ("大视界-动画片", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                           'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1547549227742425"}'}),
        3020: ("大视界-六一晚会", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                            'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1561705200669742"}'}),
        3021: ("大视界-最野假期", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                            'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1547176242993572"}'}),
        3022: ("大视界-动物好伙伴", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                             'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1551859538300202"}'}),
        3023: ("大视界-创意大赛", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                            'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1548319282379544"}'}),
        3024: ("大视界-孝心少年", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                            'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1547176214271596"}'}),
        3025: ("大视界-情景剧", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                           'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1548127868549846"}'}),
        3026: ("大视界-过年啦", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                           'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1547176110078570"}'}),
        3027: ("大视界-赢在博物馆", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                             'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1547540690917184"}'}),
        3028: ("大视界-微星时代", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                            'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1547540182406121"}'}),
        3029: ("大视界-智慧树", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                           'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1547176282412574"}'}),
        3030: ("大视界-银河之声", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                            'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1547176267875573"}'}),
        3031: ("大视界-小鬼当家", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                            'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1547176130737595"}'}),
        3032: ("大视界-极速少年", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                            'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1547550267930783"}'}),
        3033: ("大视界-七巧板", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                           'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1548323772684547"}'}),
        3034: ("大视界-音乐快递", {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                            'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"Page1551159187522726"}'}),
        
    }
    
    start_method = 'POST'
    
    def parse(self, response):
        rj = json.loads(response.text)
        cardgroups = rj.get("cardgroups")
        for i in cardgroups:
            cards = i.get("cards")
            for j in cards:
                id = j.get("id")
                formdata_body = {'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}',
                                 'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":""}'}
                formdata_json = json.loads(formdata_body.get("json"))
                formdata_json['cardgroups'] = id
                formdata_body['json'] = json.dumps(formdata_json)
                # p ={'appcommon': '{"ap":"androidphone","an":"央视少儿","adid":"864416035963936","av":"2.1.1"}', 'json': '{"paging":{"page_size":20,"page_no":1,"last_id":""},"cardgroups":"VIDE1561964208019810"}'}
                print(id)
                yield FormRequest(
                    url="https://api.cctv.cn/childmobileinf/rest/cctv/cardgroups",
                    formdata=formdata_body,
                    method="POST",
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'],
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )
    
    def parse_item(self, response, only_video=False):
        rj = json.loads(response.text)
        cardgroups = rj.get("cardgroups")
        if cardgroups is None:
            return
        for j in cardgroups:
            cards = j.get("cards")
            for i in cards:
                try:
                    video = i.get("video")
                    url = video.get("url_cd")
                    date = i.get("date")

                    title = i.get("title")
                    source = i.get("source")
                    
                    photo = i.get("photo")
                    image = photo.get("thumb")
                    videos = None
                    
                    if url.endswith(('.mp4', '.mkv', '.avi', '.wmv', '.iso')):
                        videos = {'1': {'src': url}}
                        video_cover = to_list(image)
                        content = '<div>#{{1}}#</div>'
                        if only_video:
                            return videos, video_cover
                    elif url.endswith(('.mp3')):
                        return self.produce_debugitem(response, "audio filter")
                    else:
                        content = i.get("content")
                except:
                    return self.produce_debugitem(response, "json error")
                
                return self.produce_item(
                    response=response,
                    title=title,
                    pubtime=date,
                    origin_name=source,
                    content=content,
                    media={},
                    videos=videos
                )
