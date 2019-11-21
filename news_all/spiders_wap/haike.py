# -*- coding: utf-8 -*-

import json
import re
from scrapy import Request
from news_all.spider_models import NewsRSpider
from news_all.tools.others import to_list
from scrapy.conf import settings


class HaikeGSpider(NewsRSpider):
    chinese_name = """海客新闻app"""
    name = 'haike_get_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    api = 'http://haikenews.android.haiwainet.cn/hk-service-file/search/comprehensive?size=10&current=1&channelId={}&searchType=1'
    
    channel_source_ids = {
        "评论": 318,
        "视觉": 319,
        "美国": 320,
        "台湾": 338,
        "学习小组": 339,
        "侠客岛": 340,
        "日本": 341,
        "华人": 342,
        "南海": 343,
        "加拿大": 344,
        "朝鲜": 346,
        "澳大利亚": 347,
        "澳门": 349,
        "德国": 351,
        "香港": 352,
        "新西兰": 354,
        "新加坡": 355,
        "法国": 357,
        "韩国": 359,
        "理论": 360,
        "非洲": 363,
        "西班牙": 365,
        "意大利": 367,
        "葡萄牙": 368,
        "荷兰": 370,
    }
    channel_map = {
        "评论": "24",
        "视觉": "28626342773919744",
        "美国": "87364687141933056",
        "台湾": "87360228580003840",
        "学习小组": "28628764766375936",
        "侠客岛": "28330840010428416",
        "日本": "87364126875193344",
        "华人": "87359445713162240",
        "南海": "28628839613730816",
        "加拿大": "87364771057373184",
        "朝鲜": "87364000949604352",
        "澳大利亚": "87364495835533312",
        "澳门": "87359173611884544",
        "德国": "87363087107231744",
        "香港": "87359658297266176",
        "新西兰": "87364579029553152",
        "新加坡": "87361937398173696",
        "法国": "87362964025380864",
        "韩国": "87364302822051840",
        "理论": "28628667403997184",
        "非洲": "87361625614585856",
        "西班牙": "87363192061300736",
        "意大利": "87363342129303552",
        "葡萄牙": "87363474916773888",
        "荷兰": "87363795948802048",
    }
    start_headers = {  # 可以不加headers
        "ProductCode": "haikenews",
        "Os": "Android",
        "Os_Version": "6.0",
        "HaikeVersion": "65",
        "Content-Type": "application/json;charset=utf-8",
        "Host": "haikenews.android.haiwainet.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.10.0",
    }
    mystart_urls = {}
    for i, j in channel_map.items():
        mystart_urls[api.format(j)] = channel_source_ids[i]
    
    def parse(self, response):
        rs = json.loads(response.text)
        if str(rs.get('code')) != "200":
            return self.produce_debugitem(response, 'json error')
        
        for i in rs.get('data'):
            iid = i.get("id")
            # mediaId = i.get('mediaId', '')
            news_url = 'http://haiwaivideo.android.haiwainet.cn//hk-service-news/news/publish/{}'.format(iid)
            pubtime = i.get("releaseTime") or i.get("createTime")
            
            origin_name = i.get("origin").get("sourceName")
            title = i.get("title")
            summary = i.get('summary')
            video_url = i.get("videoUrl")  # type="5"时有video_url todo 怎样简写
            if video_url:
                print()
            
            yield Request(
                url=news_url,
                callback=self.parse_item,
                meta={'pubtime': pubtime, 'title': title, 'origin_name': origin_name,
                      'summary': summary,
                      'source_id': response.meta['source_id'],
                      'start_url_time': response.meta.get('start_url_time'),
                      'schedule_time': response.meta.get('schedule_time')}
            )
    
    def parse_item(self, response):
        rs = json.loads(response.text)
        if str(rs.get('code')) != "200":
            # {"code":"404","data":null,"message":"没有找到指定稿件数据","meta":{"current":1,"pages":0,"size":10,"total":0},"msg":"没有找到指定稿件数据","status":"404"}
            return self.produce_debugitem(response, 'json error')
        
        data = rs.get('data')
        if not data:
            return
        video_url = data.get("videoUrl")
        content = data.get('content')  # or data.get('strContent')
        
        if not content and not video_url:
            self.log('source_id: %s, url: %s, 无正文无视频' % (response.meta.get('source_id'), response.url))
            return self.produce_debugitem(response, 'json error')
        
        if content:
            if video_url:
                content, media, _, _ = self.content_clean(content)
                content = '<p>#{{1}}#<p>' + content
                videos = {'1': {'src': video_url}}
                video_cover = to_list(data.get("thumbnail"))
                self.log(
                    'source_id: %s, 有正文有视频, url:%s, 正文:%s' % (response.meta.get('source_id'), response.url, content))
            
            else:
                content, media, videos, video_cover = self.content_clean(content)
                self.log(
                    'source_id: %s, 有正文无视频, url:%s, 正文:%s' % (response.meta.get('source_id'), response.url, content))
        
        elif video_url:
            content = '<p>#{{1}}#<p>'
            videos = {'1': {'src': video_url}}
            video_cover = to_list(data.get("thumbnail"))
            media = {}
            self.log('source_id: %s, 无正文有视频, url:%s, 视频:%s' % (response.meta.get('source_id'), response.url, video_url))
        
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            summary=response.request.meta['summary'],
            content=content,
            media=clear_haike_media(media),
            videos=videos,
            video_cover=video_cover,  # etl暂时未用到
        )

# class HaiKePSpider(NewsRSpider):
#     # 海客新闻post
#     name = 'haike_post_app'
#
#     custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
#     mystart_urls = {
#         'http://haikenews.android.haiwainet.cn/recommend/Resys?latitude=39.927&productCode=1&imei=861603035854842&longitude=116.4804&version=5.1.3': 320,
#         # 推荐
#     }
#
#     # {"msg":"指纹验证失败！","code":1,"cost":0}
#     # {"msg":"http status 500: 服务器遇到错误，无法完成请求（服务器内部错误）","code":1,"cost":10010}
#     """
#     //access_token:
#     //productCode: haikenews
#     //imeiCode: 861603035854842
#     //os: Android
#     //os_version: 6.0
#     haikeVersion: 65
#     timestamp: 1562821619678  # 必须要
#     //nonceStr: 8613410
#     signature: 55a0e3dee281b15930718587dc90c553  # 必须要
#     Content-Type: application/json;charset=utf-8
#     //Content-Length: 0
#     Host: haikenews.android.haiwainet.cn
#     Connection: Keep-Alive
#     Accept-Encoding: gzip
#     User-Agent: okhttp/3.10.0
#     """
#     start_method = "POST"
#     start_headers = {
#         "USER_AGENT": "okhttp/3.10.0",
#         "Content-Type": "application/json;charset=utf-8"
#     }
#
#     def parse(self, response):
#
#         rs = json.loads(response.text)
#
#         if str(rs.get('code')) != "200":
#             return self.produce_debugitem(response, 'json error')
#
#         for i in rs.get('data'):
#             iid = i.get("id")
#             news_url = 'http://haikenews.haiwainet.cn/hk-service-news/news/publish/{}'.format(iid)
#
#             contentType = str(i.get("contentType"))
#             if contentType == "1":
#                 newsInfo = i.get("newsInfo")
#             elif contentType == "3":
#                 newsInfo = i.get("newsInfo")
#                 self.log('contentType==3, source_id:%s, response.text: %s ' % (
#                     response.meta.get('source_id'), response.text))
#                 # news_url = 'http://haikenews.haiwainet.cn/hk-service-news/news/publish/{}'.format(iid)  # todo check
#             else:
#                 self.log('contentType!=1 or 3, source_id:%s, response.text: %s ' % (
#                     response.meta.get('source_id'), response.text))  # todo check
#                 # news_url = 'http://haikenews.haiwainet.cn/hk-service-news/news/publish/{}'.format(iid)  # todo check
#
#             if not newsInfo:
#                 newsInfo = i.get('freshnewsInfo') or deepcopy(i)
#
#             pubtime = newsInfo.get("publishTime") or newsInfo.get("releaseTime") or newsInfo.get("createTime")
#
#             if newsInfo.get("origin"):
#                 origin_name = newsInfo.get("origin").get("sourceName")
#             else:
#                 origin_name = '海客新闻'
#                 print('no newsInfo.get("origin"), contentType:%s, newsInfo： %s' % (contentType, newsInfo))
#
#             title = newsInfo.get("title")
#             summary = i.get('summary')
#             video_url = newsInfo.get("videoUrl")
#
#             yield Request(
#                 url=news_url,
#                 callback=self.parse_item,
#                 meta={'pubtime': pubtime, 'title': title, 'origin_name': origin_name, 'video_url': video_url,
#                       'summary': summary, 'contentType': i.get("contentType"),
#                       'source_id': response.meta['source_id']}
#             )
#
#     def parse_item(self, response):
#
#         rs = json.loads(response.text)
#
#         if str(rs.get('code')) != "200":
#             return self.produce_debugitem(response, 'json error')
#
#         video_url = response.meta.get('video_url')
#         videos = {'1': {'src': video_url}} if video_url else {}
#
#         data = rs.get('data')
#         if data:
#             content = data.get('content', '')
#             content, media, _, _ = self.content_clean(content)
#
#         else:  # 故意抛出缺正文的记录
#             content = ''
#             media = {}
#
#         return self.produce_item(
#             response=response,
#             title=response.request.meta['title'],
#             pubtime=response.request.meta['pubtime'],
#             origin_name=response.request.meta['origin_name'],
#             summary=response.request.meta['summary'],
#             content=content,
#             media=clear_haike_media(media),
#             videos=videos,
#         )
#
#
# class HaiKePUSpider(NewsRSpider):
#     # 海客新闻post_update
#     name = 'haike_post_update'
#
#     custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
#     api = 'http://haikenews.android.haiwainet.cn/hk-service-file/advertPositions/detail/2'  # 推荐-热点精选轮播
#     start_headers = {
#         "USER_AGENT": "okhttp/3.10.0",
#         "Content-Type": "application/json;charset=utf-8",
#         "productCode": "haikenews",  # 不加也行
#         "Host": "haikenews.android.haiwainet.cn",  # 不加也行
#     }
#     start_body = {"size": 5, "totalData": 1}
#     mystart_reqs = [
#         FormRequest(api, method="POST", body=json.dumps(start_body), dont_filter=True, meta={'source_id': 320}), ]
#
#     def parse(self, response):
#         # 2019年3月18日再次抓包的
#         """
#         {
#     "status":"200",
#     "code":"200",
#     "msg":"",
#     "message":"",
#     "data":{
#         "id":2,
#         "advertCode":"2",
#         "advertName":"热点精选-首页轮播图",
#         "productCode":"",
#         "advertOpen":"2",
#         "advertLimitCount":"5",
#         "startTime":"",
#         "overTime":"",
#         "contentType":"",
#         "materialList":[{
#                 "id":2771,
#                 "fileCode":1105496849089015809,
#                 "accessUrl":"http://mk.haiwainet.cn/newsHtml/2019/3/12/1105496849089015809.shtml",
#                 "title":"传播两会声音 聚焦海客视点",
#                 "advertText":"传播两会声音 聚焦海客视点",
#                 "sortNum":2,
#                 "adverter":"",
#                 "publishTime":1552879194000,
#                 "advertPosition":"2",
#                 "newsCode":1105496849089015809,
#                 "startTime":"",
#                 "overTime":"",
#                 "contentType":"1",
#                 "materialType":"2",
#                 "type":"5",
#                 "horizontal":"http://haikenews.static.haiwainet.cn/images/2019/3/12/d5966d8e-1fe1-4492-b892-45626e367d76.png",
#                 "vertical":"",
#                 "video":"http://haiwaivideo.src.haiwainet.cn/video/HKBBXWSSK/20190318/155287766709724800.mp4",
#                 "status":"",
#                 "sourceName":"海外网",
#                 "channelList":"",
#                 "channelNameList":[
#
#                 ]
#             },]
#         "advertMaterialList":[
#
#         ],
#         "status":""
#     },
#     "meta":{
#         "total":0,
#         "size":10,
#         "pages":0,
#         "current":1
#     }
# }
#         """
#
#         rs = json.loads(response.text)
#
#         if str(rs.get('code')) != "200":
#             return self.produce_debugitem(response, 'json error')
#
#         for i in rs.get('data').get('materialList'):
#             news_url = i.get("accessUrl")
#
#             contentType = str(i.get("contentType"))
#             if contentType != "1":
#                 self.log('contentType!=1, source_id:%s, response.text: %s, contentType: %s ' % (
#                     response.meta.get('source_id'), response.text, contentType))
#
#             materialType = str(i.get("materialType"))
#             if materialType != "2":
#                 self.log('materialType!=2, source_id:%s, response.text: %s, materialType: %s ' % (
#                     response.meta.get('source_id'), response.text, materialType))
#             title = i.get("title")
#
#             pubtime = i.get("publishTime")
#             
#                 yield self.produce_debugitem(response, 'pubtime 24 hours after', srcLink=news_url)
#                 continue
#
#             origin_name = i.get("sourceName") or '海外网'
#             video_url = i.get("video")
#             video_cover = i.get("horizontal")
#
#             yield Request(
#                 url=news_url,
#                 callback=self.parse_item,
#                 meta={'pubtime': pubtime, 'title': title, 'origin_name': origin_name, 'video_url': video_url,
#                       'video_cover': video_cover, 'contentType': i.get("contentType"),
#                       'source_id': response.meta['source_id']}
#             )
#
#     def parse_item(self, response):
#         # 2019年3月18日再次抓包的
#
#         try:
#             content_div = response.xpath('.//div[@id="artical"]/div[@class="content"]')[0]
#         except:
#             return self.produce_debugitem(response, 'xpath error')
#
#         content, media, _, _ = self.content_clean(content_div)
#         video_url = response.request.meta.get('video_url')
#         videos = {'1': {'src': video_url}} if video_url else {}
#
#         return self.produce_item(
#             response=response,
#             title=response.request.meta['title'],
#             pubtime=response.request.meta['pubtime'],
#             origin_name=response.request.meta['origin_name'],
#             
#             content=content,
#             media=clear_haike_media(media),
#             videos=videos,
#         )
#
#
Extensions = ['BMP', 'jpg', 'JPG', 'JPEG', 'png', 'PNG', 'gif', 'GIF']
img_pattern = re.compile(r"src=(.*?\.(?:%s))" % ('|'.join(Extensions)))


def clear_haike_media(media):
    # https://timgsa.baidu.com/timg?image&amp;quality=80&amp;size=b9999_10000&amp;sec=1553609064431&amp;di=e57d2fa7c3c84de86499c2300df331c7&amp;imgtype=0&amp;src=http://upload.cankaoxiaoxi.com/2017/0413/1492082050435.jpg
    """
    :param media:    dict
    :return:
    """
    images = media.get("images")
    if not images:
        return media

    images_new = {}
    for i, j in images.items():
        pic_url = j['src']
        if pic_url.find('src') < 0:
            return media

        pic_url = img_pattern.search(pic_url).group(1)
        images_new[i] = {"src": pic_url}

    media['images'] = images_new
    return media
