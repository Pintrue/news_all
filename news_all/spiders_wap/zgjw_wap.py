#!/usr/bin/env python
# -*- coding:utf-8 _*-
# Time: 2019/07/18
# Author: zcy

from news_all.spider_models import NewsRSpider
from scrapy.conf import settings
import json
from scrapy import Request, FormRequest


class ZgjwSpider(NewsRSpider):
    """中国军网 app"""
    name = 'zgjw_app'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN'),
        'DEPTH_LIMIT': 20
    }
    
    list_url = 'http://appapi.81.cn/v4/i/statuses/getlist.json?devicetype=2&device_size=720.0x1280.0&version=187&tagid={}'
    detail_url = 'http://appapi.81.cn/v4/i/statuses/detail.json?devicetype=2&itemid={}'
    
    # today = datetime.date.today()
    # formatted_today = today.strftime('%Y%m%d')
    # jfjb_url = 'http://appapi.81.cn/v4/i/statuses/getlist.json?tagtype=10&device_size=720.0x1280.0&version=187&data={}&devicetype=2&h=945&w=645&coords=1'.format(
    #     formatted_today)  # 解放军报
    # gfb_url = 'http://appapi.81.cn/v4/i/statuses/getlist.json?tagtype=20&device_size=720.0x1280.0&version=187&data={}&devicetype=2&h=945&w=645&coords=1'.format(
    #     formatted_today)  # 国防报
    
    # 不写data 就返回当天的新闻
    jfjb_url = 'http://appapi.81.cn/v4/i/statuses/getlist.json?tagtype=10&device_size=720.0x1280.0&version=187&devicetype=2&h=945&w=645&coords=1' # 解放军报
    gfb_url = 'http://appapi.81.cn/v4/i/statuses/getlist.json?tagtype=20&device_size=720.0x1280.0&version=187&devicetype=2&h=945&w=645&coords=1'  # 国防报
    
    mystart_urls = {}
    tagid_list = [
        '274_275',  # 首页-推荐
        '745_749',  # 首页-新闻
        '280_281',  # 首页-评论
        '312_313',  # 首页-视频
        '315_316',  # 首页-图片
        '283_284',  # 首页-军史
        '767_769',  # 首页-人物
        '815_817',  # 首页-兵器
        '304_305',  # 首页-军校
        '863_865',  # 首页-女兵
        '903_905',  # 首页-H5
        '301_302',  # 首页-军嫂
        '783_785',  # 首页-外军
        '1297_1299',  # 首页-军艺
        '1321_1323',  # 首页-VR
        '1195_1197',  # 首页-军委机关
        '1235_1237',  # 首页-陆军
        '1227_1229',  # 首页-海军
        '1219_1221',  # 首页-空军
        '1211_1213',  # 首页-火箭军
        '1025_1027',  # 首页-武警部队
        '1203_1205',  # 首页-战略支援
        '1335_1337',  # 首页-联勤保障
        '1033_1035',  # 首页-东部战区
        '1041_1043',  # 首页-南部战区
        '1179_1181',  # 首页-西部战区
        '1187_1189',  # 首页-北部战区
        '1243_1245',  # 首页-中部战区
        '1145_1147',  # 首页-我们的天空
        '1139_1141',  # 首页-当代海军
        '1131_1133',  # 首页-第一军情
        '1123_1125',  # 首页-三剑客
        '1107_1109',  # 首页-解放军生活
        '1099_1101',  # 首页-军报记者
        '1089_1093',  # 首页-环球军事
        '1115_1117',  # 首页-钧正平
        '298_299',  # 首页-老兵
        '937_939',  # 首页-军医
        '292_293',  # 首页-英烈
        '775_777',  # 首页-军工
        '879_881',  # 首页-边防
        '839_841',  # 首页-维和
        '871_873',  # 首页-军厨
        '287_288',  # 首页-发言人
        '1405_1407',  # 首页-军服
        '1395_1399',  # 首页-理论
        '333_334',  # 军报每天读-视频播报
        '1383_1385',  # 军报每天读-音频播报
        '1361_1363',  # 八一电视-微视
        '1377_1379',  # 八一电视-访谈
        '1351_1355',  # 八一电视-综艺
        '1369_1371',  # 八一电视-动漫
        '1389_1391',  # 八一电视-剧场
    ]
    
    for i, tagid in enumerate(tagid_list):
        mystart_urls[list_url.format(tagid)] = i + 3401
    mystart_urls[jfjb_url] = 3454
    mystart_urls[gfb_url] = 3455
  
    def parse(self, response):
        source_id = response.meta['source_id']
        if source_id != 3454 and source_id != 3455:  # 不是解放军报或国防报
            list_dict = json.loads(response.body)
            if len(list_dict) == 0:
                return
            maxid = list_dict[-1]['item_id']  # 当前列表最后一个 item_id 作为请求下一页列表 post 请求的 maxid
            for item in list_dict:
                item_url = self.detail_url.format(item['item_id'])
                yield Request(
                    url=item_url,
                    callback=self.parse_item,
                    meta={
                        'source_id': source_id,
                        'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')
                    }
                )
            
            # 获取下一页列表
            yield FormRequest(
                url=response.request.url,
                formdata={'maxid': maxid},
                callback=self.parse,
                meta={
                    'max_id': maxid,
                    'source_id': response.meta['source_id'],
                    'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')
                }
            )
        else:  # 解放军报或国防报
            section_list = json.loads(response.body)
            for section in section_list:
                areas = section.get('areas')
                for area in areas:
                    yield Request(
                        url=self.detail_url.format(area['newsid']),
                        callback=self.parse_item,
                        meta={
                            'source_id': source_id,
                            'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')
                        }
                    )
    
    def parse_item(self, response):
        item_dict = json.loads(response.body)
        title = item_dict[0].get('title')
        origin_name = item_dict[0].get('doings_source')
        summary = item_dict[0].get('description')
        videos = item_dict[0].get('video')
        content = item_dict[0].get('content')
        pubtime = item_dict[0].get('time')
      
        content_clean, media, _, _ = self.content_clean(content)
        
        videos_dict = {}
    
        if isinstance(videos, str):
            videos_dict = {'1': {'src': videos}}
        if isinstance(videos, list):
            for i, video in enumerate(videos):
                videos_dict[str(i + 1)] = {'src': video}
        if not videos_dict and isinstance(item_dict[0].get('target_url'), str) and item_dict[0]['target_url'][-4:]=='.mp4':
            videos_dict = {'1': {'src': item_dict[0]['target_url']}}
            
        yield self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            summary=summary,
            content='<div>#{{1}}#</div></br>' + content_clean if len(videos_dict) != 0 else content_clean,
            media=media,
            videos=videos_dict if len(videos_dict) != 0 else ''
        )
