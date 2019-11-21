# -*- coding: utf-8 -*-

from datetime import datetime
import re
import requests
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.spider_models import NewsRCSpider


class PeopleVideoSpider(NewsRCSpider):
    """人民视频"""
    name = 'peoplevideo'

    mystart_urls = {
        'http://v.people.cn/GB/61600/': 3823,  # 资讯时政
        'http://v.people.cn/GB/14645/25060/': 3826,  # 国际
        'http://v.people.cn/GB/67816/': 3828,  # 军事
        'http://v.people.cn/GB/79889/': 3829,  # 娱乐
        'http://v.people.cn/GB/39805/': 3831,  # 社会
        'http://v.people.cn/GB/14644/': 3832,  # 访谈

        'http://v.people.cn/GB/67527/': 3834,  # 台湾
        'http://v.people.com.cn/GB/413792/index.html': 3848,  # 热点短视频
        # 'http://v.people.cn/GB/177969/425311/index.html':9,  # 纪录片    不要
        'http://tv.people.com.cn/GB/60604/187593/': 3850,  # 地方频道上海
        'http://tv.people.com.cn/GB/60604/187594/index.html': 3851,  # 广东
        'http://tv.people.com.cn/GB/60604/187595/': 3853,  # 苏南
        'http://tv.people.com.cn/GB/60604/188825/index.html': 3854,  # 甘肃
        'http://tv.people.com.cn/GB/60604/192501/index.html': 3855,  # 广西
        'http://tv.people.com.cn/GB/60604/200153/index.html': 3856,  # 湖北
        'http://tv.people.com.cn/GB/60604/201221/index.html': 3857,  # 山东
        'http://tv.people.com.cn/GB/60604/201599/index.html': 3858,  # 河南
        'http://tv.people.com.cn/GB/60604/201943/index.html': 3859,  # 新疆
        'http://tv.people.com.cn/GB/60604/203472/index.html': 3860,  # 江西
        'http://tv.people.com.cn/GB/60604/207515/index.html': 3862,  # 陕西
        'http://tv.people.com.cn/GB/60604/208841/index.html': 3864,  # 安徽
        'http://tv.people.com.cn/GB/60604/209267/index.html': 3865,  # 浙江
        'http://tv.people.com.cn/GB/60604/211802/index.html': 3866,  # 贵州
        'http://tv.people.com.cn/GB/60604/212783/index.html': 3867,  # 湖南
        'http://tv.people.com.cn/GB/60604/214901/index.html': 3868,  # 云南
        'http://tv.people.com.cn/GB/60604/216321/index.html': 3870,  # 海南
        'http://tv.people.com.cn/GB/60604/221400/index.html': 3871,  # 黑龙江
        'http://tv.people.com.cn/GB/60604/355487/index.html': 3872,  # 福建
        'http://tv.people.com.cn/GB/60604/356167/index.html': 3873,  # 天津
        'http://v.people.com.cn/GB/418789/index.html': 3849,  # 国家日历
        'http://vblog.people.com.cn/index/newcolumn/sid/164': 3836,  # 人民拍客70年
        'http://vblog.people.com.cn/index/newcolumn/sid/165': 3838,  # 资讯  todo
        'http://vblog.people.com.cn/index/newcolumn/sid/166': 3841,  # 政务
        'http://vblog.people.com.cn/index/newcolumn/sid/167': 3843,  # 军事
        'http://vblog.people.com.cn/index/newcolumn/sid/168': 3844,  # Vlog
        'http://vblog.people.com.cn/index/newcolumn/sid/171': 3846,  # 生活
        'http://vblog.people.com.cn/index/newcolumn/sid/169': 3847,  # 西藏
    }
    # http://v.people.cn/n1/2019/0827/c61600-31319435.html
    # http://v.people.com.cn/n1/2019/0828/c413792-31322425.html
    rules = (
        Rule(LinkExtractor(allow=r'v.people.cn.*?/%s\d{2}/c\d+-\d+.html' % datetime.today().strftime('%Y/%m'), ),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'v.people.com.cn.*?/%s\d{2}/c\d+-\d+.html' % datetime.today().strftime('%Y/%m'), ),
             callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        try:
            url_div = response.xpath('//*[@id="pvpShowDiv"]/script[2]/text()').extract_first()
            title = response.xpath('//h2/text()')[0].extract()
            pubtime = response.xpath('/html/head/meta[@name="publishdate"]/@content')[0].extract()
            param = re.findall(".*id:\"(.*)\",skip.*", url_div)[0]
        except:
            return self.produce_debugitem(response, "xpath error")
        if param:
            base_url = "http://tvplayer.people.com.cn/getXML.php?path=" + param
            video_url = parse_item_list(base_url)
            if video_url:
                videos = {'1': {'src': video_url}}
                content = '<div>#{{1}}#</div>'
                return self.produce_item(
                    response=response,
                    title=title,
                    pubtime=pubtime,
                    origin_name="人民视频",
                    content=content,
                    media={},
                    videos=videos
                )


def parse_item_list(url):
    try:
        response = requests.get(url)
        video_url = re.findall(".*\('(.*)', '.*", response.text)[0]
        return video_url
    except:
        return
