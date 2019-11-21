#!/usr/bin/env python
# -*- coding:utf-8 _*-
# Time: 2019/07/24
# Author: zcy

from urllib.request import urljoin
import jsonpath
from news_all.spider_models import *
from scrapy.conf import settings
import json
from scrapy import Request
from copy import deepcopy


class CriWapSipder(NewsRSpider):
    """国际在线 app"""
    name = 'cri_app'
    dd = deepcopy(settings.getdict('APP_DOWN'))
    dd['news_all.middlewares.ProxyRdMiddleware'] = 100  # 备用 使用隧道代理
    custom_settings = {'DOWNLOADER_MIDDLEWARES': dd, }
    sleep_time = 300
    mystart_urls = {
        'http://101.37.31.60:8080/portal/dubboaction.act': [418, 420, 427, 430, 435, 442, 443, 445, 447, 454, 464, 480,
                                                            506, 519, 522, 523, 525, 526, 527, 528, 529, 530, 615]}
    
    start_body_map = {  # 基类封装body中index 替换为range(10)
        418: ('要闻',
              [
                  '{"c_menu_id":"101","index":"%s", "c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"1720E58F58F5E3A067D28B9154BA5CB1","uuid":"1562327071111"}' % i
                  for i in range(10)]),
        420: ('锐评',
              [
                  '{"c_menu_id":"97b248b23255472dabea2bbf138e10a4","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"DCC49F6333BA0EBBB5A7DAB1D59FABD5","uuid":"1562327581514"}' % i
                  for i in range(10)]),
        427: ('国际',
              [
                  '{"c_menu_id":"102","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"ABEB339603CD7BD6B239EBEF31068EC9","uuid":"1562651795723"}' % i
                  for i in range(10)]),
        430: ('国内',
              [
                  '{"c_menu_id":"103","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"9ECC683F07DBFC496CB20D6ABF5432C2","uuid":"1562650610142"}' % i
                  for i in range(10)]),
        435: ('北京',
              [
                  '{"c_menu_id":"ebc88eec42c04d8e8c30fa71882e7ee9","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"AA7F0E01AF2FC8AA117FCB9C9CEE7D2A","uuid":"1562652208415"}' % i
                  for i in range(10)]),
        442: ('城市',
              [
                  '{"c_menu_id":"110","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"3FE1CE1E0005262CAD5BA84F87BE2FF2","uuid":"1562652648450"}' % i
                  for i in range(10)]),
        443: ('老外在中国',
              [
                  '{"c_menu_id":"200","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"EF5B7F6F5B0F4C533BFCDB0B89F8243B","uuid":"1562651433639"}' % i
                  for i in range(10)]),
        445: ('娱乐',
              [
                  '{"c_menu_id":"106","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"7B2A28124E07BC1597FA58D590FAFF0A","uuid":"1562651834312"}' % i
                  for i in range(10)]),
        447: ('视频',
              [
                  '{"c_menu_id":"2e84d4a9686a4e368b10a2099764acbf","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"77E4FDC9A674CD9D941BEFAC08A3896A","uuid":"1562652182865"}' % i
                  for i in range(10)]),
        454: ('原创',
              [
                  '{"c_menu_id":"aa92d8a0b63c40ebaef25e90d6d78232","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"72AA568DD824D0F82F253719D86DE123","uuid":"1562651304921"}' % i
                  for i in range(10)]),
        464: ('体育',
              [
                  '{"c_menu_id": "107","index":"%s","c_app_ver": "4.0.0","c_channel": "chinanews","c_inst_code": "10063","c_language_id": "zh","c_os": "1","c_user_id": "","interfaceId": "newslist_02","system_language_id": "zh","sign": "B6270D98433FD38C784B1ABBDD36A16D","uuid": "1563785505369"}' % i
                  for i in range(10)]),
        480: ('汽车',
              [
                  '{"c_menu_id":"109","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"C99BE0C398343F183EB30FDF4634ACD5","uuid":"1562651691103"}' % i
                  for i in range(10)]),
        506: ('金融',
              [
                  '{"c_menu_id":"2851cb57f36d4522b688a751b25ef23a","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"4D378BBC7E18FA1A185B93A462B8BA93","uuid":"1562651391278"}' % i
                  for i in range(10)]),
        519: ('环球财智',
              [
                  '{"c_menu_id":"108","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"423ACE113F81EBF4E047DD1F5DEA9643","uuid":"1562652716841"}' % i
                  for i in range(10)]),
        522: ('老外街访评',
              [
                  '{"c_menu_id":"67be2371b3854dcbac29f4568d51add5","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"D00A8BF242CBF784E3A76A8F13B9166A","uuid":"1562652289808"}' % i
                  for i in range(10)]),
        523: ('评论',
              [
                  '{"c_menu_id":"104","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"E12F37CA7D764B10C64CD3D515A1A754","uuid":"1562652109164"}' % i
                  for i in range(10)]),
        525: ('生态中国',
              [
                  '{"c_menu_id":"d646a2a7156f44c0a460056e669603dd","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"F671B1A64AC4F6C4101409EBED357FA7","uuid":"1562651734990"}' % i
                  for i in range(10)]),
        526: ('非遗',
              [
                  '{"c_menu_id":"45a255bb8895483bb574fdda9d37bc83","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"41CD965FBF7348F8578371F0B36BD41E","uuid":"1562651361166"}' % i
                  for i in range(10)]),
        527: ('环球创业',
              [
                  '{"c_menu_id":"0ddbba01f88347499f57add1c8b273fa","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"7F3CDB90758A99BBFAB5C584D4DCE53C","uuid":"1562650810110"}' % i
                  for i in range(10)]),
        528: ('外媒看中国',
              [
                  '{"c_menu_id":"0a76995c83634753a6ea3f9ad4453435","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"C54D60BBBAC00AE5DDE666EB3CC2F87F","uuid":"1562651496852"}' % i
                  for i in range(10)]),
        529: ('创新',
              [
                  '{"c_menu_id":"c98f827ca1be4a5e9ec58c96c491915a","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"7486411C43C37832B4836962FDEE4F27","uuid":"1562650979073"}' % i
                  for i in range(10)]),
        530: ('企业',
              [
                  '{"c_menu_id":"a6517e3c8574495eaccc727bae526f0e","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"BDB7B0C7115C8B64237A3A16B55B13E1","uuid":"1562650915432"}' % i
                  for i in range(10)]),
        615: ('学习有道',
              [
                  '{"c_menu_id":"deae4c36371f4da6942697d206b6db4d","index":"%s","c_app_ver":"4.0.6","c_channel":"chinanews","c_inst_code":"10128","c_language_id":"zh","c_os":"1","c_user_id":"","interfaceId":"newslist_02","system_language_id":"zh","sign":"0F6FF43AF85449E20F85530CBC5A4EB3","uuid":"1562651653945"}' % i
                  for i in range(10)]),
    }
    
    start_method = 'POST'

    def parse(self, response):
        rs = json.loads(response.body)
        # 返回的 json 有两种格式  rs['newslist_02']是dict 或 list
        if isinstance(rs['newslist_02'], dict):
            for vo in rs['newslist_02'].get('content', {}).get('voList', []):
                for article in vo['returnEntrie']:
                    news_url = article['newsHttp']
                    pubtime = article['newsTime']
                    
                    article_dict = {
                        'title': article['newsTitle'],
                        # 'summary': article['newsContent'],
                        'pubtime': pubtime,
                        'origin_name': article['newsFrom'],
                        'images': article['picUrlList'],
                        'videos': {'1': {"src": article['radioHttp']}} if article['radioHttp'] != '' else '',
                        'url': news_url
                    }
                    # ValueError: Missing scheme in request url: /20190808/bf7ddac9-55bb-e3ff-ac1c-f12e7747f302.html
                    yield Request(
                        url=news_url,
                        callback=self.parse_item,
                        meta={
                            'article_dict': deepcopy(article_dict),
                            'source_id': response.meta['source_id'],
                            'start_url_time': response.meta.get('start_url_time'),
                            'schedule_time': response.meta.get('schedule_time')
                        }
                    )
        else:
            total = jsonpath.jsonpath(rs, '$.newslist_02[*].entries[*]')
            for entry in total:
                news_url = urljoin('http://news.cri.cn', entry['url']) if entry['url'][:4] != 'http' else entry['url']
                # '/20190808/bf7ddac9-55bb-e3ff-ac1c-f12e7747f302.html'
                pubtime = entry['publishTime']
                art = entry['article']
                if art.get('videoResources'):  # dict_list 'url' 'thumbnail'
                    print()
                article_dict = {
                    'title': entry['title'],
                    'pubtime': entry['publishTime'],
                    'origin_name': entry['article']['source'],
                    'videos': {'1': {"src": art['videoResources'][0]['url']}} if art.get('videoResources') else '',
                    'url': news_url
                }
                
                yield Request(
                    url=news_url,
                    callback=self.parse_item,
                    meta={
                        'article_dict': deepcopy(article_dict),
                        'source_id': response.meta['source_id'],
                        'start_url_time': response.meta.get('start_url_time'),
                        'schedule_time': response.meta.get('schedule_time')
                    }
                )
    
    def parse_item(self, response):
        article_dict = response.meta['article_dict']
        
        content = response.xpath('//*[@id="abody"]').extract_first('')
        content_clean, media, video, cover = self.content_clean(content, need_video=True)  # img video原本就包含在content中
        
        if article_dict['videos'] != '' and not video:  # 防止video没被content包含
            content_clean = '<div>#{{1}}#</div>' % content_clean
            video = article_dict['videos']
        
        return self.produce_item(
            response=response,
            title=article_dict['title'],
            pubtime=article_dict['pubtime'],
            origin_name=article_dict['origin_name'],
            content=content_clean,
            media=media,
            videos=video
        )
