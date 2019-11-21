# -*- coding: utf-8 -*-

from news_all.spider_models import NewsRSpider
from scrapy.conf import settings
import json
from scrapy import Request
import jsonpath
import requests


class CntvcboxAppSipder(NewsRSpider):
    """央视影音"""
    name = 'cntvcbox_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}

    mystart_urls = {
        'http://cbox.cntv.cn/json2015/topshouye/newyear/index.json': 3316,  # APP端-中央媒体移动端-央视影音-精选
        'http://cbox.cntv.cn/json2015/fenleierjiye/tiyuyexinban/sports2017/no1/womenfootballcup/2019WTTC/index.json': 3317,
                                                                                                                             # APP端-中央媒体移动端-央视影音-世界杯
        'http://cbox.cntv.cn/json2015/fenleierjiye/kejiaoerjiye2017/special/dengzhewo/dzw/dzwz/index.json': 3318,
                                                                                                                             # APP端-中央媒体移动端-央视影音-等着我
        'http://cbox.cntv.cn/json2015/topic/cboxzz/kandian/shouye/index.json': 3319,  # APP端-中央媒体移动端-央视影音-看点
        'http://cbox.cntv.cn/json2015/fenleierjiye/tiyuyexinban/sports2017/main/index.json': 3320,
                                                                                                                             # APP端-中央媒体移动端-央视影音-体育
        'http://media.app.cntvwb.cn/vapi/video/vlist.do?gid=182mmeA30926&n=20&p=1&uid=': 3321,  # APP端-中央媒体移动端-央视影音-小央视频
        'http://api.cntv.cn/list/getCboxFeedRecommend?serviceId=cbox&n=20&p=2&serviceId=cbox&type=0&utdid=WQhBxuWoQM8DAC1vA7UdQhHx': 3322,
                                                                                                                            # APP端-中央媒体移动端-央视影音-爱看
        'http://cbox.cntv.cn/json2015/medium/news/main928/index.json': 3323,  # APP端-中央媒体移动端-央视影音-新闻
        'http://cbox.cntv.cn/json2015/fenleierjiye/caijing/caijing/index.json': 3324,  # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/fenleierjiye/mkyuyue/main/index.json': 3325,  # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/fenleierjiye/aixiyou/onTV/main/index.json': 3326,  # APP端-中央媒体移动端-央视影音-上电视
        'http://cbox.cntv.cn/json2015/jingxuan/zgxqdh/main/index.json': 3327,  # APP端-中央媒体移动端-央视影音-汽车
        'http://cbox.cntv.cn/json2015/music/jingxuanPAGEqiuA3XbgxDXGhPewPlpy181024/main/index.json': 3328,
                                                                                                                            # APP端-中央媒体移动端-央视影音-音乐
        'http://cbox.cntv.cn/json2015/medium/main/main/index.json': 3329,  # APP端-中央媒体移动端-央视影音-书画
        'http://api.cntv.cn/list/CboxSpecialList?id=TDAT1504838902038321&serviceId=cbox&serviceId=cbox&n=20&p=1': 3330,
                                                                                                                             # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/fenleierjiye/caijing/mkyuyue/meirijingxuan/index.json': 3331,
                                                                                                                             # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/fenleierjiye/caijing/mkyuyue/touzixiaofei/index.json': 3332,
                                                                                                                             # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/fenleierjiye/caijing/mkyuyue/gushidongtai/index.json': 3333,
                                                                                                                                # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/fenleierjiye/caijing/mkyuyue/caijingVjiangtang/index.json': 3334,
                                                                                                                              # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/fenleierjiye/caijing/mkyuyue/duihuadaka/index.json': 3335,  # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/fenleierjiye/caijing/mkyuyue/caijingquan/index.json': 3336,
                                                                                                                             # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/fenleierjiye/mkyuyue/yyjs/index.json': 3337,  # APP端-中央媒体移动端-央视影音-军事
        'http://api.cntv.cn/video/videolistById?serviceId=cbox&vsid=VSET100424684697&em=02&n=20&p=1': 3338,
                                                                                                                              # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/fenleierjiye/mkyuyue/module/zgjlnew/index.json': 3339,  # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/fenleierjiye/mkyuyue/module/ljzb/index.json': 3340,  # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/fenleierjiye/mkyuyue/module/hjzb/index.json': 3341,  # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/fenleierjiye/mkyuyue/module/kjzb/index.json': 3350,  # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/fenleierjiye/mkyuyue/module/jbzt/index.json': 3351,  # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/jingxuan/zgxqdh/module/mkyuyuePAGE8F5pfSes6Bugd3OfnJLn180927/index.json': 3352,
                                                                                             # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/jingxuan/zgxqdh/module/sphf/index.json': 3353,  # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/jingxuan/zgxqdh/module/zba/index.json': 3354,  # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/jingxuan/zgxqdh/module/mkyuyuePAGEGNRW8QtXrVj72MRvz2uF180927/index.json': 3355,
                                                                                     # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/music/jingxuanPAGEqiuA3XbgxDXGhPewPlpy181024/module/yytj/index.json': 3356,
                                                                                      # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/music/jingxuanPAGEqiuA3XbgxDXGhPewPl/mkyuyue/index.json': 3357,
                                                                                    # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/music/jingxuanPAGEqiuA3XbgxDXGhPewPlpy181024/module/jcyyh/index.json': 3358,
                                                                                    # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/music/jingxuanPAGEqiuA3XbgxDXGhPewPlpy181024/module/mgzg/index.json': 3359,
                                                                                     # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/music/jingxuanPAGEqiuA3XbgxDXGhPewPlpy181024/module/fhgy/index.json': 3360,
                                                                                     # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/music/jingxuanPAGEqiuA3XbgxDXGhPewPlpy181024/module/ych/index.json': 3361,
                                                                                     # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/music/jingxuanPAGEqiuA3XbgxDXGhPewPlpy181024/module/yygkk/index.json': 3362,
                                                                                     # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/music/jingxuanPAGEqiuA3XbgxDXGhPewPlpy181024/module/tbjm/index.json': 3363,
                                                                                     # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/medium/main/module/zgjlnew/index.json': 3364,  # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/medium/main/module/ljzb/index.json': 3365,  # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/medium/main/module/hjzb/index.json': 3366,  # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/medium/main/module/jbzt/index.json': 3367,  # APP端-中央媒体移动端-央视影音-军事
        'http://cbox.cntv.cn/json2015/medium/main/module/kjzb/index.json': 3368,  # APP端-中央媒体移动端-央视影音-财经
        'http://cbox.cntv.cn/json2015/medium/main/module/jvztgd/index.json': 3369,  # APP端-中央媒体移动端-央视影音-军事

    }

    def parse(self, response):
        rs = json.loads(response.text)
       # 第一种json情况
        templateUrl = jsonpath.jsonpath(rs, '$..templateUrl')
        listUrl = jsonpath.jsonpath(rs, '$..listUrl')
        vids = jsonpath.jsonpath(rs, '$..vid')
        # 第二种json情况（见小央视频）只是获取视频id不一样 ，详情页json是一样的
        guid = jsonpath.jsonpath(rs, '$..guid')

        # 判断list不为空，去除listurl中的空字符串
        urls = None
        if listUrl:
            listUrl = [x for x in listUrl if x != '']
            urls = listUrl
        if templateUrl:
            templateUrl = [x for x in templateUrl if x != '']
            urls+=templateUrl
        if urls:
            for url in urls:
                video_ids=parse_item_list(url)
                # 判断列表url中获取到的视频id不为空
                if video_ids:
                    vids += video_ids

        if guid:
            guid = [x for x in guid if x != '']
            vids += guid
        # 如果获取到vids 说明存在视频新闻，进入视频解析parse
        if vids:
            vids = [x for x in vids if x != '']
            for vid in vids:
                # detail_url = "https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid="+vid+"&tsp=1563438538&uid=1563438538&vc=A3A3C0FE90BC5AC343A7402E34C790E9&vn=3&wlan=w"
                detail_url = 'https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid='+vid
                yield Request(
                    url=detail_url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'],
                          'start_url_time': response.meta.get('start_url_time'),
                          'schedule_time': response.meta.get('schedule_time')}
                )

    def parse_item(self, response):
        try:
            rj = json.loads(response.text)
            title = jsonpath.jsonpath(rj, '$..title')[0]
            origin_name = jsonpath.jsonpath(rj, '$..play_channel')[0]
            pubtime = jsonpath.jsonpath(rj, '$..f_pgmtime')[0]

            video = rj.get("video")
            chapters2 = video.get("chapters2")[0]
            video_url = chapters2.get("url")
        except:
            return self.produce_debugitem(response, "json error")

        videos = {'1': {'src': video_url}}
        content = '<div>#{{1}}#</div>'

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media={},
            videos=videos
        )

def parse_item_list(url):
    try:
        res = requests.get(url)
        rj = res.json()
        vids = jsonpath.jsonpath(rj, '$..vid')
        return vids
    except:
        return
