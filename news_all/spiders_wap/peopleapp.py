# -*- coding: utf-8 -*-

import json
from copy import deepcopy
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings
from news_all.spiders_wap.peopleapp_tuijian import PeopleAppTjSpider
from news_all.spiders_wap.peopleapp_tuijian import make_img_content


class PeopleappSpider(PeopleAppTjSpider):
    name = 'people_app'

    custom_settings = deepcopy(PeopleAppTjSpider.custom_settings)
    custom_settings.update(
        {
            "SCHEDULER_DUPEFILTER_KEY": '%s:dupefilter' % PeopleAppTjSpider.name,
        }
    )
    start_formdata_map = None
    start_method = 'GET'
    mystart_urls = {
        'https://app.peopleapp.com/WapApi/610/HomeApi/getContentList?category_id=1&refresh_time=0&show_num=10&page=1&'
        'securitykey=ee9bad0d112f882403f5b9f4dc2266a0&interface_code=610': 237,  # 闻热点
        'https://app.peopleapp.com/WapApi/610/HomeApi/getContentList?category_id=2&refresh_time=0&show_num=10&page=1&'
        'securitykey=4f21c0fc02912b9a7903c65e62455ce7&interface_code=610': 276,  # 锐评度

        'https://app.peopleapp.com/WapApi/610/HomeApi/getContentList?category_id=5&refresh_time=0&show_num=10&page=1&'
        'securitykey=89fce10ff73c12bcad189dc40faae1be&interface_code=610': 279,  # 社会

        'https://app.peopleapp.com/WapApi/610/HomeApi/getContentList?category_id=6&refresh_time=0&show_num=10&page=1&'
        'securitykey=b6545f0bf9f611f208b2b1d95dad24de&interface_code=610': 286,  # 财经

        'https://app.peopleapp.com/WapApi/610/HomeApi/getContentList?category_id=12&refresh_time=0&show_num=10&page=1&'
        'securitykey=fd7beda3517dc35e3722b5e7c54ebf8b&interface_code=610': 287,  # 军事

        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=6&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=7b989e043621277f09dca4f31cc2f448&show_num=20&update_time=0&userId=0&version=6.2.1": 1000105,
        # 人民日报客户端-财经
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=104&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=401768a8221b3c430f210fac0a56ee44&show_num=20&update_time=0&userId=0&version=6.2.1": 1000132,
        # 人民日报客户端-地方-安徽
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=102&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=1521551003&securitykey=673e9745af05ddfac642a059c25f3dc0&show_num=20&update_time=0&userId=0&version=6.2.1": 1000120,
        # 人民日报客户端-地方-北京
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=106&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=1b8aa622a6bc0696924bf9e5d0520796&show_num=20&update_time=0&userId=0&version=6.2.1": 1000133,
        # 人民日报客户端-地方-福建
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=38&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=7c9319e1cbc60831a4135f15e6afd428&show_num=20&update_time=0&userId=0&version=6.2.1": 1000147,
        # 人民日报客户端-地方-甘肃
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=103&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=c6eda761905b1b88fda1e4ebef1710c9&show_num=20&update_time=0&userId=0&version=6.2.1": 1000138,
        # 人民日报客户端-地方-广东
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=23&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=09562f4f9eb2aa781dc02970d7234fcb&show_num=20&update_time=0&userId=0&version=6.2.1": 1000139,
        # 人民日报客户端-地方-广西
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=113&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=5fe1b5cf5b61968298de7d35ad5777bf&show_num=20&update_time=0&userId=0&version=6.2.1": 1000143,
        # 人民日报客户端-地方-贵州
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=108&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=a9e4d8ca340095153dcbf65e271496a7&show_num=20&update_time=0&userId=0&version=6.2.1": 1000140,
        # 人民日报客户端-地方-海南
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=105&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=1521550936&securitykey=e2911ce14a8fdabb5789b2d9a1d72e5f&show_num=20&update_time=0&userId=0&version=6.2.1": 1000122,
        # 人民日报客户端-地方-河北
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=112&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=1521550930&securitykey=40b99b0148b46187ba13cad8f30cd190&show_num=20&update_time=0&userId=0&version=6.2.1": 1000126,
        # 人民日报客户端-地方-河南
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=107&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=576dd1b7379590701fcb68b9ac7f37c5&show_num=20&update_time=0&userId=0&version=6.2.1": 1000128,
        # 人民日报客户端-地方-黑龙江
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=101&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=cdeac66de4214b5d2ad534b5dd72ce86&show_num=20&update_time=0&userId=0&version=6.2.1": 1000136,
        # 人民日报客户端-地方-湖北
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=110&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=6984325cb8acefcaa87b4ea1dbc3d13e&show_num=20&update_time=0&userId=0&version=6.2.1": 1000137,
        # 人民日报客户端-地方-湖南
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=109&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=d7ab10b053866b32bb18ace9cca818b6&show_num=20&update_time=0&userId=0&version=6.2.1": 1000127,
        # 人民日报客户端-地方-吉林
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=18&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=eb0147b5793e4966e384899b21cae167&show_num=20&update_time=0&userId=0&version=6.2.1": 1000130,
        # 人民日报客户端-地方-江苏
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=19&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=2b7b37afa8172161fb360d5755eb261e&show_num=20&update_time=0&userId=0&version=6.2.1": 1000134,
        # 人民日报客户端-地方-江西
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=20&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=1521550982&securitykey=4a54c7d21696f44f724297715ed2d81d&show_num=20&update_time=0&userId=0&version=6.2.1": 1000124,
        # 人民日报客户端-地方-辽宁
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=21&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=1521550970&securitykey=8add8ed783bf3a131ca0d3c9fca2ea9a&show_num=20&update_time=0&userId=0&version=6.2.1": 1000125,
        # 人民日报客户端-地方-内蒙古
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=22&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=7535e7e318975d396d7a6aeddfe6e82d&show_num=20&update_time=0&userId=0&version=6.2.1": 1000149,
        # 人民日报客户端-地方-宁夏
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=39&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=13771196491905cdb3c3f87d7da78cbe&show_num=20&update_time=0&userId=0&version=6.2.1": 1000148,
        # 人民日报客户端-地方-青海
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=25&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=33f6ff822c3bbb6d8c068bec6325be2f&show_num=20&update_time=0&userId=0&version=6.2.1": 1000135,
        # 人民日报客户端-地方-山东
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=27&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=1521550985&securitykey=b7eb02799f84308ce432356b11396cfa&show_num=20&update_time=0&userId=0&version=6.2.1": 1000123,
        # 人民日报客户端-地方-山西
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=28&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=dbfcd3eab9fde98c3f949742818a9a09&show_num=20&update_time=0&userId=0&version=6.2.1": 1000146,
        # 人民日报客户端-地方-陕西
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=26&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=04b1b12817a23b842a89c78897f67d28&show_num=20&update_time=0&userId=0&version=6.2.1": 1000129,
        # 人民日报客户端-地方-上海
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=24&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=38c7206b59e5de1c37d17e0b79891be0&show_num=20&update_time=0&userId=0&version=6.2.1": 1000142,
        # 人民日报客户端-地方-四川
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=225&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=1521550987&securitykey=a2656fb94273fb4fee7d5058f7789fd5&show_num=20&update_time=0&userId=0&version=6.2.1": 1000121,
        # 人民日报客户端-地方-天津
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=33&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=fecef1cb4128e787519892519357af35&show_num=20&update_time=0&userId=0&version=6.2.1": 1000145,
        # 人民日报客户端-地方-西藏
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=32&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=30d232dc1e958812ca3c6b2f1fb239c4&show_num=20&update_time=0&userId=0&version=6.2.1": 1000150,
        # 人民日报客户端-地方-新疆
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=34&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=ea24872efb611293e44ce01c31c3c135&show_num=20&update_time=0&userId=0&version=6.2.1": 1000144,
        # 人民日报客户端-地方-云南
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=35&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=aa977f918d8e21e6f0d43ae9158bf4b3&show_num=20&update_time=0&userId=0&version=6.2.1": 1000131,
        # 人民日报客户端-地方-浙江
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=111&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=e0b1abb21712a7729adc979722f7d2e1&show_num=20&update_time=0&userId=0&version=6.2.1": 1000141,
        # 人民日报客户端-地方-重庆
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=15&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=2ae77ce37fea720e6ac4f3ceaf0e8ffc&show_num=20&update_time=0&userId=0&version=6.2.1": 1000111,
        # 人民日报客户端-房产
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=11&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=1635b88d1d81f6c259fb4f02863e564f&show_num=20&update_time=0&userId=0&version=6.2.1": 1000107,
        # 人民日报客户端-健康
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=10&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=9c0cc438d64cc618f75ceb78eee7f09b&show_num=20&update_time=0&userId=0&version=6.2.1": 1000106,
        # 人民日报客户端-教育
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=12&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=bf9b83477c7c1e2bdbe40bdff123d18a&show_num=20&update_time=0&userId=0&version=6.2.1": 1000108,
        # 人民日报客户端-军事
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=13&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=fc3b7d8a0648804a7c93e85b60c5d412&show_num=20&update_time=0&userId=0&version=6.2.1": 1000110,
        # 人民日报客户端-科技
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=229&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=1521550994&securitykey=df61446d239fb0472498b9e5e5e813a3&show_num=20&update_time=0&userId=0&version=6.2.1": 1000103,
        # 人民日报客户端-旅游
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=2&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=1096862&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=0&refresh_time=1521617339&securitykey=6f3764d2c49a885a97a3f31f30c1898c&show_num=20&update_time=0&userId=0&version=6.2.1": 1000101,
        # 人民日报客户端-评论
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=14&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=98db17b59403d22dc41426f3164ce45e&show_num=20&update_time=0&userId=0&version=6.2.1": 1000109,
        # 人民日报客户端-汽车
        "http://app.peopleapp.com/Api/622/GovApi/govList?article_push_id=&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2012.0&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&interface_code=625&latitude=39.919541015625&longitude=116.4710495334201&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_time=0&securitykey=568c9a721a427d95a29ad7fa711a938c&show_num=20&type=0&user_gov_id=&user_id=0&version=6.2.5": 1000153,
        # 人民日报客户端-人民号
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=5&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=1084183&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=0&refresh_time=1521618435&securitykey=81f8ceb4b63a6d4cf203d4b932eb827a&show_num=20&update_time=0&userId=0&version=6.2.1": 1000102,  # 人民日报客户端-社会
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=1&city=&citycode=&device=a1da5005-82b9-337d-b234-e23d5436db7b&device_model=SM801&device_os=Android%205.1.1&device_product=smartisan&device_size=1080*1920&device_type=1&district=&fake_id=&image_height=1920&image_wide=1080&interface_code=619&latitude=0.0&longitude=0.0&page=1&province=&province_code=1517202505000&refresh_tag=1&refresh_time=0&show_num=20&update_time=0&userId=0&version=6.1.9&securitykey=9446061b3358d858a511e9eb51e0b8ea": 1000100,
        # 人民日报客户端-首页
        "http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=9&channel=app%20store&city=%E5%8C%97%E4%BA%AC%E5%B8%82&citycode=010&device=0AF9B2C0-D286-449A-87DF-D547B1B509B3&device_model=iPhone&device_os=iOS%2011.2.6&device_product=%E8%8B%B9%E6%9E%9C&device_size=1125%2A2436&device_type=2&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&fake_id=6789022&id=&image_height=1125&image_wide=2436&interface_code=621&latitude=39.91952880859375&longitude=116.4708805338542&page=1&province=%E5%8C%97%E4%BA%AC%E5%B8%82&refresh_tag=1&refresh_time=0&securitykey=a69d5913a6378cea86882cc470ff4764&show_num=20&update_time=0&userId=0&version=6.2.1": 1000104,
        # 人民日报客户端-文化
    }

    def parse_html(self, response):  # 弃用
        # baseurl = 'https://wap.peopleapp.com/article/{id}/{articleid}'  # js
        try:
            content_div = response.xpath('.//div[@class="article"]')[0]
        except:
            return self.produce_debugitem(response, "xpath error")

        content, media, videos, video_cover = self.content_clean(content_div)
        if '责任编辑' not in content:
            editor = response.xpath('.//*[contains(text(), "责任编辑")]/text()').extract_first('').strip()
            if editor:
                content += '<p>' + editor + '</p>'

        return self.produce_item(
            response=response,
            title=response.request.meta['title'],
            pubtime=response.request.meta['pubtime'],
            origin_name=response.request.meta['origin_name'],
            content=content,
            media=media,
            videos=videos,
        )


class PeopleappAtlasSpider(NewsRSpider):
    """人民日报客户端-镜头"""
    name = 'peopleapp_atlas'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        'https://app.peopleapp.com/WapApi/610/HomeApi/getContentList?category_id=7&refresh_time=0&show_num=10&page=1&'
        'securitykey=58ae40139657734a2ed255491479813e&interface_code=610': 99,  # 288,  # 镜头
    }

    # LimitatedDaysHoursMinutes = (3, 0, 0)

    def parse(self, response):
        rj = json.loads(response.text)
        result = rj.get('result')  # result.get("have_more") == True
        if result.get("errorMsg") != "ok":
            return self.produce_debugitem(response, 'json error')

        for i in rj.get('data') + rj.get('hots'):
            news_url = 'https://wap.peopleapp.com/atlas/{}'.format(i.get("id"))

            pubtime = i.get("news_time")
            title = i.get("article_title") or i.get("title")
            origin_name = i.get('copyfrom')
            img_cons = i.get('image')
            if not img_cons:
                continue
            content, media = make_img_content(img_cons)

            yield self.produce_item(
                response=response,
                title=title,
                pubtime=pubtime,
                origin_name=origin_name,
                content=content,
                media=media,
                srcLink=news_url
            )
