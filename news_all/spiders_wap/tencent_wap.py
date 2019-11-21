# -*- coding: utf-8 -*-

import json
import re
from scrapy import Request
from news_all.spider_models import NewsRSpider
from copy import deepcopy
from scrapy.conf import settings

img_pattern = re.compile(r'\<\!--IMG_(\d+)--\>')  # <!--IMG_2-->


class TencentWapSpider(NewsRSpider):
    chinese_name = """腾讯app"""
    name = 'tencent_app'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN'),
        'DEPTH_LIMIT': 2
    }
    # 以下custom_settings 备用 用浏览器防止反爬
    # custom_settings = {'DOWNLOADER_MIDDLEWARES':
    #                        {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    #                         'news_all.middlewares.UserAgentMiddleware': 20,
    #                         'news_all.middlewares.PhantomJSMiddleware': 540,
    #                         }}
    mystart_urls = {
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_top&devid=52cbe7cd7f5efa46': 1079,  # 要闻
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_recommend&devid=52cbe7cd7f5efa46': 1080,  # 推荐
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_sports&devid=52cbe7cd7f5efa46': 1081,  # 体育
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_finance&devid=52cbe7cd7f5efa46': 1082,  # 财经
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_tech&devid=52cbe7cd7f5efa46': 1083,  # 科技
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_mil&devid=52cbe7cd7f5efa46': 1084,  # 军事

        # 扩展的栏目
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_child_newRecommend&devid=52cbe7cd7f5efa46': 3289,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_child_xiaoshipin&devid=52cbe7cd7f5efa46': 3290,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_child_jingxuan&devid=52cbe7cd7f5efa46': 3291,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_child_overseas&devid=52cbe7cd7f5efa46': 3292,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_child_youxi&devid=52cbe7cd7f5efa46': 3293,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_child_sannong&devid=52cbe7cd7f5efa46': 3294,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_child_aishenghuo&devid=52cbe7cd7f5efa46': 3295,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_child_yule2&devid=52cbe7cd7f5efa46': 3296,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_child_junshi&devid=52cbe7cd7f5efa46': 3297,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_child_guoji&devid=52cbe7cd7f5efa46': 3298,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_child_tiyu&devid=52cbe7cd7f5efa46': 3299,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_child_nba&devid=52cbe7cd7f5efa46': 3300,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_top&devid=52cbe7cd7f5efa46': 3301,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_19&devid=52cbe7cd7f5efa46': 3302,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_game&devid=52cbe7cd7f5efa46': 3303,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_ent&devid=52cbe7cd7f5efa46': 3304,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_lad&devid=52cbe7cd7f5efa46': 3305,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_world&devid=52cbe7cd7f5efa46': 3306,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_cul&devid=52cbe7cd7f5efa46': 3307,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_house&devid=52cbe7cd7f5efa46': 3308,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_video_main&devid=52cbe7cd7f5efa46': 3309,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_auto&devid=52cbe7cd7f5efa46': 3310,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_istock&devid=52cbe7cd7f5efa46': 3311,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_ac&devid=52cbe7cd7f5efa46': 3312,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_lic&devid=52cbe7cd7f5efa46': 3313,

        # 5月28日打标的
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_emotion&devid=52cbe7cd7f5efa46': 3343,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_workplace&devid=52cbe7cd7f5efa46': 3344,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_legal&devid=52cbe7cd7f5efa46': 3345,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_pplvideo&devid=52cbe7cd7f5efa46': 3346,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_olympic&devid=52cbe7cd7f5efa46': 3347,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_msh&devid=52cbe7cd7f5efa46': 3348,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_jiaju&devid=52cbe7cd7f5efa46': 3349,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_nba&devid=52cbe7cd7f5efa46': 3472,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_esport&devid=52cbe7cd7f5efa46': 3473,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_digi&devid=52cbe7cd7f5efa46': 3474,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_astro&devid=52cbe7cd7f5efa46': 3475,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_movie&devid=52cbe7cd7f5efa46': 3476,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_edu&devid=52cbe7cd7f5efa46': 3477,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_meirong&devid=52cbe7cd7f5efa46': 3478,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_tv&devid=52cbe7cd7f5efa46': 3479,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_strike&devid=52cbe7cd7f5efa46': 3480,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_health&devid=52cbe7cd7f5efa46': 3481,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_lifes&devid=52cbe7cd7f5efa46': 3482,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_visit&devid=52cbe7cd7f5efa46': 3483,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_zongyi&devid=52cbe7cd7f5efa46': 3484,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_food&devid=52cbe7cd7f5efa46': 3485,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_baby&devid=52cbe7cd7f5efa46': 3486,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_pet&devid=52cbe7cd7f5efa46': 3487,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_history&devid=52cbe7cd7f5efa46': 3492,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_music&devid=52cbe7cd7f5efa46': 3493,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_media&devid=52cbe7cd7f5efa46': 3502,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_kepu&devid=52cbe7cd7f5efa46': 3503,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_football&devid=52cbe7cd7f5efa46': 3504,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_icesnow&devid=52cbe7cd7f5efa46': 3505,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_orignal&devid=52cbe7cd7f5efa46': 3506,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_cba&devid=52cbe7cd7f5efa46': 3507,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_nflfootball&devid=52cbe7cd7f5efa46': 3508,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_twentyf&devid=52cbe7cd7f5efa46': 3509,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_netcourt&devid=52cbe7cd7f5efa46': 3510,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_acg&devid=52cbe7cd7f5efa46': 3511,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_tencentgy&devid=52cbe7cd7f5efa46': 3512,
        'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_agri&devid=52cbe7cd7f5efa46': 3513,
        # 'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_reading&devid=52cbe7cd7f5efa46': 3514,
    }

    def parse(self, response):
        rs = json.loads(response.text)
        if rs.get('ret') != 0:
            return self.produce_debugitem(response, 'json error')
        feedlist_items = rs.get('newslist')

        for i in feedlist_items:
            news_url = i.get('url') or i.get('short_url')

            if len(set([i.get('url'), i.get("short_url"), i.get('surl')])) != 1:
                print('url: %s\n short_url: %s\n surl: %s' % (i.get('url'), i.get("short_url"), i.get('surl')))

            if 'view.inews.qq.com/a/HOT' in news_url:
                continue
            if i.get('video_channel'):
                yield self.produce_debugitem(response, 'video filter')
                continue  # 排除视频

            pubtime = i.get('time')
            title = i.get('title')
            origin_name = i.get('source')
            yield Request(
                url=news_url,
                callback=self.parse_item_2,
                meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                      'origin_name': origin_name,
                      # 'jstype': True,
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )

    def parse_item(self, response):
        xp = response.xpath
        if 'window.__initData' not in response.text:
            print('-' * 20)
            return

        s_divs = xp('//script[contains(text(), "window.__initData")]/text()')
        if s_divs:
            ss = s_divs[0].extract()
            if 'VIDEO_0' in ss:  # 'VIDEO_0'
                # vid = re.search(r"videoId=(\w{5,})&from").group(1)
                # self.log('spider: %s, url: %s, 包含视频: %s'%(self.name, response.url, self.get_videourl(vid)))
                return  # todo

        try:
            cvs = xp("//div[@class='_1SZZ_Lq4pPJn2Qotiz5wwc']") or xp(
                '//div[contains(@class,"_11vzQYzE2TprUTvw0YpW9O")]')  # _11vzQYzE2TprUTvw0YpW9O _1bbMmdR1MYxkjAcL9EEUy8
            content_div = cvs[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content_div,
                                                                 kill_xpaths=[r'//*[contains(text(),"更多精彩资讯，欢迎关注")]',
                                                                              r'//img[contains(@src, "inews.gtimg.com/newsapp_bt/0/8536899439")]',
                                                                              r'//span[text()="点击查看全文"]/parent::div'])
        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            
            content=content,
            media=media
        )

    def parse_item_2(self, response):  # 不用浏览器的解析
        
        xp = response.xpath
        if 'window.__initData' not in response.text:
            print('window.__initData not in response url: %s'%response.url)
            return

        s_divs = xp('//script[contains(text(), "window.__initData")]/text()')
        if not s_divs:
            return

        ss = s_divs[0].extract()
        if 'VIDEO_0' in ss:  # 'VIDEO_0'
            # vid = re.search(r"videoId=(\w{5,})&from", ss).group(1)
            # self.log('spider: %s, url: %s, 包含视频: %s' % (self.name, response.url, self.get_videourl(vid)))
            return # todo

        start = ss.index('{"content":{')

        try:
            rj = json.loads(ss[start:-1]).get('content')  # 去最后1个分号
            content_div = rj.get('cnt_html')
            if not content_div:
                sectionList = rj.get('sectionList')
                if sectionList:
                    news_data = sectionList[0].get('newsList')[0]
                    news_id = news_data.get('id')
                    if news_data.get('title') == response.request.meta['title']:
                        return response.follow(news_id,
                                               callback=self.parse_item_2,
                                               meta=deepcopy(response.meta))
                    print('标题不符')
                    return
            content, img_count = self.image_clean(content_div)
            media = {}
            img_data = rj.get('cnt_attr')  # https://view.inews.qq.com/a/20190506A04N6300?uid= 得到[]
            if img_data:
                img_dict = {i: j for i, j in img_data.items() if i[:4]=="IMG_"}
            else:
                img_dict = {}

            if isinstance(img_dict, dict):
                for i, j in img_dict.items():
                    media.setdefault("images", {})  # key IMG_0
                    imgs = j.get('img').get('imgurl641') or j.get('img').get('imgurl640') or j.get('img').get(
                        'imgurl1000')  # 优先取680*668的图片
                    media['images'][str(int(i.replace('IMG_', '')) + 1)] = {"src": imgs.get('imgurl')}
            if img_count != len(img_dict):
                self.log('图片数量不符!')
        except Exception as e:
            print(e)
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            
            content=content,
            media=media
        )

    def get_videourl(self, vid):
        """备用 解析视频 """
        """
        url: https://view.inews.qq.com/a/20190507A017MS00?uid=,
        https://view.inews.qq.com/a/20190507A01A2H00?uid=解析的视频地址不对
        """
        import requests
        import json
        # vid = 'e07435holft'
        for definition in ['shd', 'hd', 'sd']:
            params = {'isHLS': False, 'charge': 0, 'vid': vid, 'defn': definition, 'defnpayver': 1, 'otype': 'json',
                      'platform': 10901, 'sdtfrom': 'v1010', 'host': 'v.qq.com', 'fhdswitch': 0, 'show1080p': 1}
            r = requests.get('http://h5vv.video.qq.com/getinfo', params=params)
            data = json.loads(r.content[len('QZOutputJson='):-1])
            url_prefix = data['vl']['vi'][0]['ul']['ui'][0]['url']
            for stream in data['fl']['fi']:
                if stream['name'] != definition:
                    continue
                stream_id = stream['id']
                urls = []
                for d in data['vl']['vi'][0]['cl'].get('ci', []):
                    keyid = d['keyid']
                    filename = keyid.replace('.10', '.p', 1) + '.mp4'
                    params = {'otype': 'json', 'vid': vid, 'format': stream_id, 'filename': filename,
                              'platform': 10901, 'vt': 217, 'charge': 0, }
                    r = requests.get('http://h5vv.video.qq.com/getkey', params=params)
                    data = json.loads(r.content[len('QZOutputJson='):-1])
                    url = '%s/%s?sdtfrom=v1010&vkey=%s' % (url_prefix, filename, data['key'])
                    urls.append(url)
                    print('stream:', stream['name'])
                    for url in urls:
                        print(url)
        if urls:
            return urls[0]

    def image_clean(self, content):
        fr = re.finditer(img_pattern, content)
        new_content = ''
        img_count = 0
        for i, j in enumerate(fr):
            st = content.find(j.group())
            end = st + len(j.group())
            new_content += content[:st] + '${{%s}}$' % (i + 1)
            content = content[end:]
            img_count += 1

        new_content += content
        new_content.replace('$$', '$<br>$')  # 连续2图片加换行
        return new_content, img_count
