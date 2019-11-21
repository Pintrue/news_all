#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 17:08
# @Author  : wjq
# @File    : jfdaily.py
import json
import random
from scrapy import Request
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.tools.agents import USER_AGENTS
from news_all.spider_models import NewsRCSpider, isStartUrl_meta, NewsRSpider


class JfdailySpider(NewsRCSpider):
    """上观新闻"""
    name = 'jfdaily'
    mystart_urls = {
        'https://www.jfdaily.com/news/sublist?section=32': 1301202,  # 上观新闻-城事（体育）-左侧列表采集
        'https://www.jfdaily.com/news/sublist?section=82': 1301203,  # 上观新闻（原解放网）-天下（原舆情）
        'https://www.jfdaily.com/news/sublist?section=13': 1301199,  # 上观新闻（原解放网）-财经（原市场解码）
        'https://www.jfdaily.com/news/sublist?section=26': 1301200,  # 上观新闻（解放网）-区情-左侧列表采集
        'https://www.jfdaily.com/news/sublist?section=25': 1301201,  # 上观新闻（解放网）-区情（上海屋檐下）
        'https://www.jfdaily.com/news/sublist?section=14': 1301198,  # 上观新闻（解放网）-财经
    }
    
    rules = (
        # https://www.jfdaily.com/news/detail?id=158798
        Rule(LinkExtractor(
            allow=(r'/news/detail\?id=\d+',), ),  # jfdaily.com
            callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'/news/sublist\?section=\d+&page=\d+',
                           restrict_xpaths=r'//div[@class="fenye1outer"]//a[text()="下一页"]'
                           ),
             follow=True, process_request=isStartUrl_meta)
    )
    custom_settings = {'DEPTH_LIMIT': 2}
    
    def parse_item(self, response):
        xp = response.xpath
        try:
            sidv = xp('//div[@class="fenxiang_zz"]')[0]
            pubtime = sidv.re(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')[0]
            cvs = xp('//div[@class="wz_contents1"]')
            content_div = cvs[0]
            title = self.get_page_title(response).split('--')[0]
            content, media, _, _ = self.content_clean(content_div, kill_xpaths=r'//div[@class="news-edit-info"]')
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name="上观新闻",
            content=content,
            media=media
        )


class JfdailyWapSpider(NewsRSpider):
    """上观新闻客户端"""
    name = 'jfdaily_wap'

    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        'http://services.shobserver.com/news/get/sectionidWithNidPtime?pagesize=10&sign=bf8012b3b65150f5f5c77e03ac4484ea&subsectionids=13%2C14%2C15%2C16%2C17%2C18%2C19&page=1&versionCode=520&platform=2&sectionid=2&times=1533026131411': 1301665,
        # 上观-财经
    }

    def parse(self, response):
        rs = json.loads(response.text)
        if not rs.get('breturn') or not isinstance(rs.get('object'),dict):  # "breturn":true,
            return self.produce_debugitem(response, 'json error')
        obj = rs['object']
        news_list = obj.get('newsList')
        if not isinstance(news_list,list):
            return self.produce_debugitem(response, 'json error')
        
        for i in news_list:
            news_id = str(i.get('id'))
            news_url = 'https://www.jfdaily.com/news/detail?id=' + news_id
            title = i.get('title')
            if i.get('newstype') != "0":
                print()
            if i.get("isCoverVideo") != 0:
                continue

            pubtime = i.get('publishtime')
        
            yield Request(
                url=news_url,
                headers={"User-Agent": USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)]},
                callback=self.parse_item,
                meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                      
                      'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
            )

    def parse_item(self, response):
        xp = response.xpath
        try:
            content_div = xp('//div[@class="wz_contents1"]')[0]
            content, media, _, _ = self.content_clean(content_div, kill_xpaths=r'//div[@class="news-edit-info"]')
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=response.meta.get('title'),
            pubtime=response.meta.get('pubtime'),
            origin_name="上观新闻",
            content=content,
            media=media
        )



"""
{
    "breturn":true,
    "success":false,
    "errorinfo":null,
    "ireturn":1000,
    "object":{
        "recommendList":[

        ],
        "newsList":[
            {
                "id":158818,
                "title":"发生了什么？上交所要对科创板两家保荐机构进行现场督导",
                "newstype":"0",
                "status":"4",
                "sectionname":"财经",
                "subsectionname":"金融区块链",
                "videoName":"",
                "isCoverVideo":0,
                "videoPoster":null,
                "videoDuration":null,
                "replay":0,
                "publishtime":1561106354000,
                "publishHours":"10分钟前",
                "picurl":"2019/6/21/22bb7f78-901d-4047-83bb-87e061e552c9.jpg",
                "picurl2":"",
                "picurl3":"",
                "picpath":"690_390",
                "picwidth":690,
                "picheight":390,
                "isvote":0,
                "isrecommend":0,
                "showtype":0,
                "actid":0,
                "actstarttime":null,
                "h5url":"",
                "iorder":0
            },
            {
                "id":158797,
                "title":"好不容易准入的带壳“猫山王”为何必须冷冻进口？海关权威解读来啦！",
                "newstype":"0",
                "status":"4",
                "sectionname":"财经",
                "subsectionname":"市场解码",
                "videoName":"",
                "isCoverVideo":0,
                "videoPoster":null,
                "videoDuration":null,
                "replay":0,
                "publishtime":1561104613000,
                "publishHours":"39分钟前",
                "picurl":"2019/6/21/291644e4-b6a2-4e51-9b3d-315ca443ccd7.jpg",
                "picurl2":"",
                "picurl3":"",
                "picpath":"690_390",
                "picwidth":690,
                "picheight":390,
                "isvote":0,
                "isrecommend":0,
                "showtype":0,
                "actid":0,
                "actstarttime":null,
                "h5url":"",
                "iorder":0
            },
            {
                "id":158798,
                "title":"200名干部已到上海薄弱村集中报到，要拜农村这片火热土地为师",
                "newstype":"0",
                "status":"4",
                "sectionname":"财经",
                "subsectionname":"市场解码",
                "videoName":"",
                "isCoverVideo":0,
                "videoPoster":null,
                "videoDuration":null,
                "replay":0,
                "publishtime":1561104438000,
                "publishHours":"42分钟前",
                "picurl":"2019/6/21/7b27360b-cd01-4cce-96b5-5e96df2b5854.jpg",
                "picurl2":"",
                "picurl3":"",
                "picpath":"690_390",
                "picwidth":690,
                "picheight":390,
                "isvote":0,
                "isrecommend":0,
                "showtype":0,
                "actid":0,
                "actstarttime":null,
                "h5url":"",
                "iorder":0
            },
            {
                "id":158777,
                "title":"菜精包装，鲜鱼去腮去鳞去内脏再销售，智慧微菜场为“新时尚”作“源头减量”文章",
                "newstype":"0",
                "status":"4",
                "sectionname":"财经",
                "subsectionname":"市场解码",
                "videoName":"",
                "isCoverVideo":0,
                "videoPoster":null,
                "videoDuration":null,
                "replay":0,
                "publishtime":1561100572000,
                "publishHours":"1小时前",
                "picurl":"2019/6/21/46558d5c-ab17-4d7b-9d57-9dd23fc7e856.jpg",
                "picurl2":"",
                "picurl3":"",
                "picpath":"690_390",
                "picwidth":690,
                "picheight":390,
                "isvote":0,
                "isrecommend":0,
                "showtype":1,
                "actid":0,
                "actstarttime":null,
                "h5url":"",
                "iorder":0
            },
            {
                "id":158611,
                "title":"采购商冒雨“相亲”上海地产水果，金山果农坦言：我们不愁卖但求你懂我",
                "newstype":"0",
                "status":"4",
                "sectionname":"财经",
                "subsectionname":"市场解码",
                "videoName":"",
                "isCoverVideo":0,
                "videoPoster":null,
                "videoDuration":null,
                "replay":0,
                "publishtime":1561069825000,
                "publishHours":"10小时前",
                "picurl":"2019/6/20/57b411b3-5e56-4597-9f85-1ee53a97462e.jpg",
                "picurl2":"",
                "picurl3":"",
                "picpath":"690_390",
                "picwidth":690,
                "picheight":390,
                "isvote":0,
                "isrecommend":0,
                "showtype":0,
                "actid":0,
                "actstarttime":null,
                "h5url":"",
                "iorder":0
            },
            {
                "id":158658,
                "title":"上海多区公共区域垃圾桶少了一半？记者调查结果出乎意料",
                "newstype":"0",
                "status":"4",
                "sectionname":"财经",
                "subsectionname":"公共空间",
                "videoName":"",
                "isCoverVideo":0,
                "videoPoster":null,
                "videoDuration":null,
                "replay":0,
                "publishtime":1561068018000,
                "publishHours":"10小时前",
                "picurl":"2019/6/20/90db50dd-ffe4-41df-af17-fbc4a06267f7.jpg",
                "picurl2":"",
                "picurl3":"",
                "picpath":"690_390",
                "picwidth":690,
                "picheight":390,
                "isvote":0,
                "isrecommend":0,
                "showtype":1,
                "actid":0,
                "actstarttime":null,
                "h5url":"",
                "iorder":0
            },
            {
                "id":158653,
                "title":"海外公共政策专家：上海减少垃圾桶，说明市民意识已经进入新的层次",
                "newstype":"0",
                "status":"4",
                "sectionname":"财经",
                "subsectionname":"财经连线",
                "videoName":"",
                "isCoverVideo":0,
                "videoPoster":null,
                "videoDuration":null,
                "replay":0,
                "publishtime":1561035557000,
                "publishHours":"19小时前",
                "picurl":"2019/6/20/b8f6e141-d6c3-43a9-89d7-de5fc8cf72a7.jpg",
                "picurl2":"",
                "picurl3":"",
                "picpath":"690_390",
                "picwidth":690,
                "picheight":390,
                "isvote":0,
                "isrecommend":0,
                "showtype":0,
                "actid":0,
                "actstarttime":null,
                "h5url":"",
                "iorder":0
            },
            {
                "id":158622,
                "title":"还有3个月，“不换卡、不换号”的5G服务就将正式面世，但手机您得换",
                "newstype":"0",
                "status":"4",
                "sectionname":"财经",
                "subsectionname":"市场解码",
                "videoName":"",
                "isCoverVideo":0,
                "videoPoster":null,
                "videoDuration":null,
                "replay":0,
                "publishtime":1561030182000,
                "publishHours":"21小时前",
                "picurl":"2019/6/20/c2e898bc-8d48-4bee-8fc1-69850fe0320b.jpg",
                "picurl2":"",
                "picurl3":"",
                "picpath":"690_390",
                "picwidth":690,
                "picheight":390,
                "isvote":0,
                "isrecommend":0,
                "showtype":0,
                "actid":0,
                "actstarttime":null,
                "h5url":"",
                "iorder":0
            },
            {
                "id":158617,
                "title":"“榴莲控”看过来，正宗的带壳“猫山王”来了！",
                "newstype":"0",
                "status":"4",
                "sectionname":"财经",
                "subsectionname":"创客驿站",
                "videoName":"",
                "isCoverVideo":0,
                "videoPoster":null,
                "videoDuration":null,
                "replay":0,
                "publishtime":1561025415000,
                "publishHours":"22小时前",
                "picurl":"2019/6/20/b5022d2d-ae56-4d5a-a328-11177fea661a.jpg",
                "picurl2":"",
                "picurl3":"",
                "picpath":"690_390",
                "picwidth":690,
                "picheight":390,
                "isvote":0,
                "isrecommend":0,
                "showtype":0,
                "actid":0,
                "actstarttime":null,
                "h5url":"",
                "iorder":0
            },
            {
                "id":158585,
                "title":"【新时代新作为新篇章】高可靠性保障上海电网今年迎峰度夏",
                "newstype":"0",
                "status":"4",
                "sectionname":"财经",
                "subsectionname":"产业观察",
                "videoName":"",
                "isCoverVideo":0,
                "videoPoster":null,
                "videoDuration":null,
                "replay":0,
                "publishtime":1561020021000,
                "publishHours":"1天前",
                "picurl":"2019/6/20/31f4ff0c-fe02-4ddf-ae57-ccf2f072943d.jpeg",
                "picurl2":"",
                "picurl3":"",
                "picpath":"690_390",
                "picwidth":690,
                "picheight":390,
                "isvote":0,
                "isrecommend":0,
                "showtype":0,
                "actid":0,
                "actstarttime":null,
                "h5url":"",
                "iorder":0
            }
        ],
        "total":12328,
        "totalpage":1233,
        "nowpage":1,
        "pagepize":10,
        "advertList":[

        ]
    }
}
"""