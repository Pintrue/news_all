# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, js_meta


class CyolAllSpider(NewsRCSpider):
    """中青在线"""
    name = 'cyol_all'
    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}
    mystart_urls = {
        'http://theory.cyol.com/indexapp.htm?tid=645&title=%E9%9D%92%C2%B7%E5%AD%A6%E4%B9%A0&type=channel': 1584,
        'http://theory.cyol.com/indexapp.htm?tid=603&title=%E9%9D%92%C2%B7%E7%90%86%E8%AE%BA&type=channel': 1585,
        'http://theory.cyol.com/indexapp.htm?tid=605&title=%E9%9D%92%C2%B7%E5%A3%B0%E9%9F%B3&type=channel': 1586,
        'http://theory.cyol.com/indexapp.htm?tid=606&title=%E9%9D%92%C2%B7%E4%BD%93%E9%AA%8C&type=channel': 1587,
        'http://theory.cyol.com/indexapp.htm?tid=607&title=%E9%9D%92%C2%B7%E8%A7%86%E9%87%8E&type=channel': 1588,
        'http://news.cyol.com/indexapp.htm?tid=548&title=%E6%97%B6%E6%94%BF&type=channel': 1589,
        'http://news.cyol.com/indexapp.htm?tid=554&title=%E6%B5%B7%E8%BF%90%E4%BB%93%E5%86%85%E5%8F%82': 1590,
        'http://news.cyol.com/indexapp.htm?tid=770&title=%E6%97%B6%E6%94%BF+': 1591,
        'http://gqt.cyol.com/indexapp.htm?tid=688&title=%E8%81%94%E6%92%AD&type=channel': 1592,
        'http://news.cyol.com/indexapp.htm?tid=767&title=%E5%AD%A6%E4%B9%A0&type=channel': 1593,
        'http://news.cyol.com/indexapp.htm?tid=768&title=%E5%AD%A6%E4%B9%A0%E8%BF%9B%E8%A1%8C%E6%97%B6': 1594,
        'http://news.cyol.com/indexapp.htm?tid=555&title=%E5%AD%A6%E4%B9%A0%E9%9D%92%E5%B9%B4': 1595,
        'http://news.cyol.com/indexapp.htm?tid=769&title=%E5%AD%A6%E4%B9%A0+': 1596,
        'http://news.cyol.com/indexapp.htm?tid=771&title=%E5%86%B0%E7%82%B9&type=channel': 1597,
        'http://news.cyol.com/indexapp.htm?tid=777&title=%E8%AF%84%E8%AE%BA&type=channel': 1598,
        'http://news.cyol.com/indexapp.htm?tid=779&title=%E5%BF%AB%E8%AF%84': 1599,
        'http://news.cyol.com/indexapp.htm?tid=782&title=%E4%B8%AD%E9%9D%92%E8%9E%8D%E8%AF%84': 1600,
        'http://news.cyol.com/indexapp.htm?tid=556&title=%E8%AF%84%E8%AE%BA+': 1601,
        'http://news.cyol.com/indexapp.htm?tid=885&title=%E5%BE%AE%E4%BF%A1%E7%B2%BE%E9%80%89&type=channel': 1602,
        'http://news.cyol.com/indexapp.htm?tid=644&title=%E4%B8%AD%E9%9D%92%E6%8A%A5%E5%AE%98%E5%BE%AE': 1603,
        'http://news.cyol.com/indexapp.htm?tid=502&title=%E5%9D%A4%E5%93%A5007': 1604,
        'http://news.cyol.com/indexapp.htm?tid=480&title=%E9%9D%92%E5%B9%B4%E8%A7%82%E5%AF%9F%E5%AE%B6': 1605,
        'http://news.cyol.com/indexapp.htm?tid=895&title=%E9%9D%92%E5%B9%B4%E7%9C%BC&type=channel': 1606,
        'http://news.cyol.com/indexapp.htm?tid=896&title=%E7%9C%8B%E4%B8%96%E7%95%8C': 1607,
        'http://news.cyol.com/indexapp.htm?tid=897&title=%E7%9C%8B%E4%B8%AD%E5%9B%BD': 1608,
        'http://news.cyol.com/indexapp.htm?tid=898&title=%E7%9C%8B%E6%A0%A1%E5%9B%AD': 1609,
        'http://news.cyol.com/indexapp.htm?tid=886&title=%E4%BC%A0%E6%89%BF%E7%9A%84%E5%8A%9B%E9%87%8F&type=channel': 1610,
        'http://news.cyol.com/indexapp.htm?tid=785&title=%E6%95%99%E8%82%B2&type=channel': 1611,
        'http://news.cyol.com/indexapp.htm?tid=786&title=%E6%88%90%E9%95%BF': 1612,
        'http://news.cyol.com/indexapp.htm?tid=652&title=%E7%95%99%E5%AD%A6': 1613,
        'http://news.cyol.com/indexapp.htm?tid=788&title=%E6%95%99%E8%82%B2%E5%9C%86%E6%A1%8C': 1614,
        'http://news.cyol.com/indexapp.htm?tid=789&title=%E9%9D%92%E9%B2%81%E7%8F%AD': 1615,
        'http://news.cyol.com/indexapp.htm?tid=791&title=%E5%B0%B1%E4%B8%9A': 1616,
        'http://news.cyol.com/indexapp.htm?tid=793&title=%E9%AB%98%E8%80%83': 1617,
        'http://news.cyol.com/indexapp.htm?tid=795&title=%E8%82%B2%E5%84%BF': 1618,
        'http://news.cyol.com/indexapp.htm?tid=588&title=%E6%95%99%E8%82%B2+': 1619,
        'http://news.cyol.com/indexapp.htm?tid=797&title=%E6%A0%A1%E5%9B%AD&type=channel': 1620,
        'http://news.cyol.com/indexapp.htm?tid=861&title=%E6%A0%A1%E5%9B%AD%E7%83%AD%E7%82%B9': 1621,
        'http://news.cyol.com/indexapp.htm?tid=862&title=%E6%B4%BB%E5%8A%A8%E5%AE%B6': 1622,
        'http://news.cyol.com/indexapp.htm?tid=863&title=%E5%BF%83%E7%81%B5%E9%A9%BF%E7%AB%99': 1623,
        'http://news.cyol.com/indexapp.htm?tid=865&title=%E9%95%9C%E5%A4%B4%E8%AF%B4%E8%AF%9D': 1624,
        'http://news.cyol.com/indexapp.htm?tid=492&title=%E6%A0%A1%E5%9B%AD+': 1625,
        'http://news.cyol.com/indexapp.htm?tid=803&title=%E5%9B%BD%E9%99%85&type=channel': 1626,
        'http://news.cyol.com/indexapp.htm?tid=866&title=24%E6%97%B6%E5%8C%BA': 1627,
        'http://news.cyol.com/indexapp.htm?tid=651&title=%E9%9D%92%E5%B9%B4%E5%8F%82%E8%80%83': 1628,
        'http://news.cyol.com/indexapp.htm?tid=524&title=%E5%9B%BD%E9%99%85+': 1629,
        'http://news.cyol.com/indexapp.htm?tid=804&title=%E8%B4%A2%E7%BB%8F&type=channel': 1630,
        'http://news.cyol.com/indexapp.htm?tid=805&title=%E7%BB%8F%E6%B5%8E%E8%B0%83%E6%9F%A5': 1631,
        'http://news.cyol.com/indexapp.htm?tid=807&title=%E4%BA%92%E8%81%94%E7%BD%91': 1632,
        'http://news.cyol.com/indexapp.htm?tid=808&title=%E6%B6%88%E8%B4%B9+': 1633,
        'http://news.cyol.com/indexapp.htm?tid=811&title=%E6%B3%95%E6%B2%BB&type=channel': 1634,
        'http://news.cyol.com/indexapp.htm?tid=650&title=%E6%B3%95%E6%B2%BB+': 1635,
        'http://news.cyol.com/indexapp.htm?tid=812&title=%E7%A4%BE%E4%BC%9A&type=channel': 1636,
        'http://news.cyol.com/indexapp.htm?tid=642&title=%E7%AC%AC%E4%B8%80%E6%97%B6%E9%97%B4': 1637,
        'http://news.cyol.com/indexapp.htm?tid=567&title=%E6%9A%96%E9%97%BB': 1638,
        'http://news.cyol.com/indexapp.htm?tid=82&title=%E8%88%86%E6%83%85': 1639,
        'http://news.cyol.com/indexapp.htm?tid=813&title=%E7%A4%BE%E4%BC%9A+': 1640,
        'http://news.cyol.com/indexapp.htm?tid=814&title=%E4%BD%93%E8%82%B2&type=channel': 1641,
        'http://news.cyol.com/indexapp.htm?tid=870&title=%E8%B5%9B%E5%8F%B0': 1642,
        'http://news.cyol.com/indexapp.htm?tid=815&title=%E8%B6%B3%E7%90%83': 1643,
        'http://news.cyol.com/indexapp.htm?tid=817&title=%E7%AF%AE%E7%90%83': 1644,
        'http://news.cyol.com/indexapp.htm?tid=871&title=%E5%86%AC%E5%A5%A5': 1645,
        'http://news.cyol.com/indexapp.htm?tid=816&title=%E5%81%A5%E8%BA%AB': 1646,
        'http://news.cyol.com/indexapp.htm?tid=572&title=%E4%BD%93%E8%82%B2+': 1647,
        'http://news.cyol.com/indexapp.htm?tid=818&title=%E6%96%87%E5%8C%96&type=channel': 1648,
        'http://news.cyol.com/indexapp.htm?tid=819&title=%E6%82%A6%E8%AF%BB': 1649,
        'http://news.cyol.com/indexapp.htm?tid=820&title=%E5%BD%B1%E8%A7%86': 1650,
        'http://news.cyol.com/indexapp.htm?tid=821&title=%E5%9B%BD%E5%AD%A6': 1651,
        'http://news.cyol.com/indexapp.htm?tid=822&title=%E6%96%87%E5%8C%96%E8%A7%82%E5%AF%9F': 1652,
        'http://news.cyol.com/indexapp.htm?tid=525&title=%E6%96%87%E5%8C%96+': 1653,
        'http://news.cyol.com/indexapp.htm?tid=826&title=%E5%86%9B%E4%BA%8B&type=channel': 1654,
        'http://news.cyol.com/indexapp.htm?tid=828&title=%E5%86%9B%E8%A7%86': 1655,
        'http://news.cyol.com/indexapp.htm?tid=530&title=%E5%86%9B%E4%BA%8B+': 1656,
        'http://news.cyol.com/indexapp.htm?tid=834&title=%E7%A7%91%E6%8A%80&type=channel': 1657,
        'http://news.cyol.com/indexapp.htm?tid=835&title=%E7%A7%91%E6%8A%80%E5%89%8D%E6%B2%BF': 1658,
        'http://news.cyol.com/indexapp.htm?tid=509&title=%E6%9D%A5%E7%82%B9%E7%A7%91%E5%AD%A6': 1659,
        'http://news.cyol.com/indexapp.htm?tid=837&title=%E6%B1%BD%E8%BD%A6&type=channel': 1660,
        'http://news.cyol.com/indexapp.htm?tid=838&title=%E6%B1%BD%E8%BD%A6%E4%B8%AD%E5%9B%BD%E6%A2%A6': 1661,
        'http://news.cyol.com/indexapp.htm?tid=839&title=%E6%9C%AA%E6%9D%A5%E5%90%AF%E7%A4%BA%E5%BD%95': 1662,
        'http://news.cyol.com/indexapp.htm?tid=872&title=%E7%8E%AF%E7%90%83%E8%A7%82': 1663,
        'http://news.cyol.com/indexapp.htm?tid=840&title=%E9%9D%92%E5%B9%B4%E8%AF%B4': 113,  # 1664,
        'http://news.cyol.com/indexapp.htm?tid=841&title=%E5%8C%A0%E4%BA%BA%E8%A1%8C': 1665,
        'http://news.cyol.com/indexapp.htm?tid=532&title=%E6%B1%BD%E8%BD%A6+': 1666,
        'http://news.cyol.com/indexapp.htm?tid=842&title=%E5%88%9B%E4%B8%9A&type=channel': 1667,
        'http://news.cyol.com/indexapp.htm?tid=843&title=%E5%88%9B%E5%AE%A2': 1668,
        'http://news.cyol.com/indexapp.htm?tid=844&title=%E5%88%9B%E8%AF%BE': 1669,
        'http://news.cyol.com/indexapp.htm?tid=103&title=KAB': 1670,
        'http://news.cyol.com/indexapp.htm?tid=90&title=%E5%88%9B%E4%B8%9A+': 1671,
        'http://news.cyol.com/indexapp.htm?tid=550&title=%E7%94%9F%E6%B4%BB&type=channel': 1672,
        'http://news.cyol.com/indexapp.htm?tid=571&title=%E6%97%85%E6%B8%B8': 1673,
        'http://news.cyol.com/indexapp.htm?tid=873&title=%E7%A0%94%E5%AD%A6': 1674,
        'http://news.cyol.com/indexapp.htm?tid=655&title=%E5%81%A5%E5%BA%B7': 1675,
        'http://news.cyol.com/indexapp.htm?tid=657&title=%E5%BF%83%E7%90%86': 1676,
        'http://news.cyol.com/indexapp.htm?tid=846&title=%E7%BE%8E%E9%A3%9F': 1677,
        'http://news.cyol.com/indexapp.htm?tid=656&title=%E6%83%85%E6%84%9F': 1678,
        'http://news.cyol.com/indexapp.htm?tid=847&title=%E7%94%9F%E6%B4%BB+': 1679,
        'http://news.cyol.com/indexapp.htm?tid=848&title=%E8%A7%86%E8%A7%89&type=channel': 1680,
        'http://news.cyol.com/indexapp.htm?tid=746&title=%E5%BE%AE%E5%85%89': 115,  # 1681,
        'http://news.cyol.com/indexapp.htm?tid=576&title=%E8%A7%86%E8%A7%89+': 116,  # 1682,
        'http://news.cyol.com/indexapp.htm?tid=849&title=%E4%B8%AD%E9%9D%92%E5%8F%B7&type=channel': 118,  # 1683,
        'http://news.cyol.com/indexapp.htm?tid=850&title=%E9%9D%92%E5%B9%B4%E6%97%B6%E8%AE%AF': 120,  # 1684,
        'http://news.cyol.com/indexapp.htm?tid=646&title=%E5%86%B0%E7%82%B9%E6%8E%A8%E8%8D%90': 122,  # 1685,
        'http://news.cyol.com/indexapp.htm?tid=648&title=%E6%B7%B1%E5%BA%A6%E8%B0%83%E6%9F%A5': 123,  # 1686,
        'http://news.cyol.com/indexapp.htm?tid=653&title=%E8%81%8C%E5%9C%BA': 125,  # 1687,
        'http://auto.cyol.com/index.htm': 1688,
        'http://auto.cyol.com/node_46342.htm': 1689,
    }

    # http://news.cyol.com/node_65534.htm?para1=News&para2=201904&para3=22&urlId=210533
    # http://news.cyol.com/node_65534.htm?para1=News&para2=201904&para3=22&urlId=210522

    rules = (
        Rule(LinkExtractor(allow=(r'cyol.com/node_\d+.htm.*?urlId=\d+'), ),
             callback='parse_item', follow=False, process_request=js_meta
             ),
    )

    # http://news.cyol.com/node_65534.htm?para1=News&para2=201904&para3=22&urlId=210533
    def parse_item(self, response):
        xp = response.xpath
        try:
            news_div = xp('.//div[@class="main-left"]/div[@class="zw"]')[0]
            source_div = news_div.xpath('./div[@class="newsInfo"]')[0]
            content_div = news_div.xpath('./div[@class="content"]')[0]
            if xp('//div[@id="player-con"]/*') or self.video_filter(content_div):
                return self.produce_debugitem(response, 'video filter')
                """
                <video class="vjs-tech" src="https://vod.cyol.com/vod/data/video/201909/22/
                6fb42dda-4736-457e-bc2d-2d3dfa73f40c/transcode_765307e9-d095-f54a-e844-
                c23bbb0a.mp4/av-g.m3u8" data-setup="{}" id="vjs_video_3_html5_api" tabindex="-1">
                """
            # http://news.cyol.com/node_65534.htm?para1=News&para2=201909&para3=22&urlId=272419
            # Request URL: http://g.alicdn.com/de/prismplayer-flash/2.8.0/PrismPlayer.swf
            # 视频 <div class="prism-player" id="player-con">
            # http://vod.cyol.com/vod/data/video/201909/22/6fb42dda-4736-457e-bc2d-2d3dfa73f40c/transcode_765307e9-d095-f54a-e844-c23bbb0a.mp4/av-g.m3u8
            time_re = source_div.re(r'\d{1,2}-\d{1,2}\s\d{1,2}\:\d{1,2}')
            pubtime = time_re[0]
            title = ''.join(i.strip() for i in news_div.xpath('./h1/text()').extract())
            origin_name = source_div.xpath('./span[@class="source"]/text()').extract_first('')
            content, media, videos, video_cover = self.content_clean(content_div)
        except:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media
        )

"""

def makeurl(news_url):
    '''新闻详情页解析'''
    # http://news.cyol.com/node_65534.htm?para1=News&para2=201909&para3=22&urlId=272419
    from news_all.tools.html_clean import get_query_map
    initUrl = "http://shareapp.cyol.com/cmsfile"
    query_map = get_query_map(news_url)
    # ["para1=News", "para2=201909", "para3=22", "urlId=272419"]
    for _, v in query_map['query'].items():
        initUrl += '/'+v
    initUrl += '.js'
    #  'http://shareapp.cyol.com/cmsfile/News/201909/22/272419.js'
    return initUrl

频道
{
    "data": [
        {
            "tid": "-1",
            "cnname": "推荐",
            "pid": "0",
            "childs": []
        },
        {
            "tid": "767",
            "cnname": "学习",
            "pid": "676",
            "childs": [
                {
                    "tid": "768",
                    "cnname": "学习进行时",
                    "pid": "767",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/d4ad7a1bb5e14ff919049d63d6eb87d0.png"
                },
                {
                    "tid": "555",
                    "cnname": "学习青年",
                    "pid": "767",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/09ac25df42ca3c558d7fe0300f10fe48.jpg"
                },
                {
                    "tid": "769",
                    "cnname": "学习+",
                    "pid": "767",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/46e5041db62f3d71724949edef79247d.png"
                }
            ]
        },
        {
            "tid": "548",
            "cnname": "时政",
            "pid": "676",
            "childs": [
                {
                    "tid": "643",
                    "cnname": "要闻",
                    "pid": "548",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/e61b6f0eaa7b2123df3652c8b45ccc32.png"
                },
                {
                    "tid": "554",
                    "cnname": "海运仓内参",
                    "pid": "548",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/1073c7d42fcebd5a7601d74954a9974b.jpg"
                },
                {
                    "tid": "649",
                    "cnname": "民族",
                    "pid": "548",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/59da70c6febe91df83ca95b69fbe8d9c.png"
                },
                {
                    "tid": "770",
                    "cnname": "时政+",
                    "pid": "548",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/15cc74bbaf23d0f7bb65b03c258f0e49.png"
                }
            ]
        },
        {
            "tid": "771",
            "cnname": "冰点",
            "pid": "676",
            "childs": [
                {
                    "tid": "772",
                    "cnname": "事件观",
                    "pid": "771",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/70c8d47445c89cad5020437a16c50730.png"
                },
                {
                    "tid": "773",
                    "cnname": "冰点特稿",
                    "pid": "771",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/4b1c6e6ebd4be7cc5064b404229316c3.png"
                },
                {
                    "tid": "774",
                    "cnname": "冰点人物",
                    "pid": "771",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/746f85aef0a41107d7c270c729750001.png"
                },
                {
                    "tid": "775",
                    "cnname": "冰点观察",
                    "pid": "771",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/3d60c1d255c0df94720146f5800ee9f2.png"
                },
                {
                    "tid": "477",
                    "cnname": "冰点+",
                    "pid": "771",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/0bb763d137286c2a589969c66c86712f.png"
                }
            ]
        },
        {
            "tid": "777",
            "cnname": "评论",
            "pid": "676",
            "childs": [
                {
                    "tid": "778",
                    "cnname": "社论",
                    "pid": "777",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/367d3037ab2e7f04ec03cc64b3ed5b7e.png"
                },
                {
                    "tid": "779",
                    "cnname": "快评",
                    "pid": "777",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/5c7f3b1eca0280a3ba4cc1319c3313fd.png"
                },
                {
                    "tid": "780",
                    "cnname": "冰点时评",
                    "pid": "777",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/36317ee6dca5546082290989f1bfc323.png"
                },
                {
                    "tid": "781",
                    "cnname": "自由谈",
                    "pid": "777",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/dca704b0fd1f3ec5fda5b5f4e482143f.png"
                },
                {
                    "tid": "782",
                    "cnname": "中青融评",
                    "pid": "777",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/93f7e066f3c2566b3635c79515b345e6.png"
                },
                {
                    "tid": "783",
                    "cnname": "吐槽青年曹林",
                    "pid": "777",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/2e9cf030d53dcdaf9311ad9917f58ad3.png"
                },
                {
                    "tid": "556",
                    "cnname": "评论+",
                    "pid": "777",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/884dd7244cd4f4684b537df1899124a8.jpg"
                }
            ]
        },
        {
            "tid": "885",
            "cnname": "微信精选",
            "pid": "676",
            "childs": [
                {
                    "tid": "644",
                    "cnname": "中青报官微",
                    "pid": "885",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/ea56ac6fc0ac5d2ae1caebb2f68278ac.jpg"
                },
                {
                    "tid": "502",
                    "cnname": "坤哥007",
                    "pid": "885",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/f3f31f27a498962b5d10100a3ad258af.png"
                },
                {
                    "tid": "480",
                    "cnname": "青年观察家",
                    "pid": "885",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/c10dac91ed81b5ff288f82f72c24ddcd.png"
                },
                {
                    "tid": "856",
                    "cnname": "青团子",
                    "pid": "885",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/1f6749251a770eeb108732784a5eee50.png"
                },
                {
                    "tid": "675",
                    "cnname": "青年范儿",
                    "pid": "885",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/b9238bab1364debee52159ef3225b23c.png"
                },
                {
                    "tid": "857",
                    "cnname": "豫青年",
                    "pid": "885",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/7e320a352cf5aeddabccdeedcf2a3926.png"
                }
            ]
        },
        {
            "tid": "895",
            "cnname": "青年眼",
            "pid": "676",
            "childs": [
                {
                    "tid": "896",
                    "cnname": "看世界",
                    "pid": "895",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/7b634f804be9006b35a9639c03abb3fa.png"
                },
                {
                    "tid": "897",
                    "cnname": "看中国",
                    "pid": "895",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/959f2b7eb8c4edd2755499bce45e502e.png"
                },
                {
                    "tid": "898",
                    "cnname": "看校园",
                    "pid": "895",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/a819a8ec89e8451204ad41fa6888a7eb.png"
                },
                {
                    "tid": "907",
                    "cnname": "看审计",
                    "pid": "895",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/9c611b60e4a316a8abe15e3eece6842a.png"
                },
                {
                    "tid": "913",
                    "cnname": "看传承",
                    "pid": "895",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/28f7263fe2e422e67c23c0912f87bd41.png"
                },
                {
                    "tid": "899",
                    "cnname": "青梅视频",
                    "pid": "895",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/2293aec06aad15afcabf1bbae6c544bc.png"
                }
            ]
        },
        {
            "tid": "886",
            "cnname": "传承的力量",
            "pid": "676",
            "childs": [
                {
                    "tid": "887",
                    "cnname": "元旦",
                    "pid": "886",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/965617b144da136bc9e1bdc878628368.png"
                },
                {
                    "tid": "888",
                    "cnname": "春节",
                    "pid": "886",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/c431956efcbb105e2c54462547f219be.png"
                },
                {
                    "tid": "889",
                    "cnname": "清明节",
                    "pid": "886",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/5b53af40de88f6037ae42817b72f5020.png"
                },
                {
                    "tid": "890",
                    "cnname": "五四青年节",
                    "pid": "886",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/ba257cc49f025a341734be49dcf0cafe.png"
                },
                {
                    "tid": "891",
                    "cnname": "端午节",
                    "pid": "886",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/b56f0d6d60f6fa12632a84a5a77f210d.png"
                },
                {
                    "tid": "892",
                    "cnname": "教师节",
                    "pid": "886",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/d7a6f97bd7fcab3733b26d335098153f.png"
                },
                {
                    "tid": "893",
                    "cnname": "中秋节",
                    "pid": "886",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/ffcf17adb3420d5244d5354dda3c4567.png"
                },
                {
                    "tid": "894",
                    "cnname": "国庆节",
                    "pid": "886",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/2db75fa2af1404babce81088df170e9f.png"
                },
                {
                    "tid": "911",
                    "cnname": "前沿",
                    "pid": "886",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/9f09ae59134f3f18de1d0dfb93d8b914.png"
                },
                {
                    "tid": "910",
                    "cnname": "汪星撞地球",
                    "pid": "886",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/692a7632f39483c0534c26022509ac9b.png"
                },
                {
                    "tid": "902",
                    "cnname": "校园足球歌曲",
                    "pid": "886",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/2db1f47f4d9017203562246999b09779.png"
                },
                {
                    "tid": "901",
                    "cnname": "原创校园中国古典诗歌",
                    "pid": "886",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/f2ffdc8310ac625dffc42e06322f10e9.png"
                },
                {
                    "tid": "900",
                    "cnname": "优秀传统文化公开课",
                    "pid": "886",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/8d1dd2b9fb87fb5cdc60b103e0d2bbfc.png"
                }
            ]
        },
        {
            "tid": "785",
            "cnname": "教育",
            "pid": "676",
            "childs": [
                {
                    "tid": "786",
                    "cnname": "成长",
                    "pid": "785",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/8aa6dafc763ec9694c4dc2b3df849335.png"
                },
                {
                    "tid": "652",
                    "cnname": "留学",
                    "pid": "785",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/748e39d923c1101dd59226e95a465a71.png"
                },
                {
                    "tid": "788",
                    "cnname": "教育圆桌",
                    "pid": "785",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/e174c175769ceabd0b9cacdfb3f98c66.png"
                },
                {
                    "tid": "789",
                    "cnname": "青鲁班",
                    "pid": "785",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/778ba635c6c3714a8ab5ae2430ae151f.png"
                },
                {
                    "tid": "791",
                    "cnname": "就业",
                    "pid": "785",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/6637252d81fde7da475048a6c972a2f4.png"
                },
                {
                    "tid": "792",
                    "cnname": "家长汇",
                    "pid": "785",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/38ccd78398a819731d74dcc8227947cc.png"
                },
                {
                    "tid": "793",
                    "cnname": "高考",
                    "pid": "785",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/a804b9ef6bc9857f1e70db5051033992.png"
                },
                {
                    "tid": "794",
                    "cnname": "长大大",
                    "pid": "785",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/3459f3873a3e992e44fb06d5c28ac269.png"
                },
                {
                    "tid": "795",
                    "cnname": "育儿",
                    "pid": "785",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/0090ec693927b9bfc82df85a84653445.png"
                },
                {
                    "tid": "588",
                    "cnname": "教育+",
                    "pid": "785",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/e0ca864f73e8722ee7f1db77bc613967.png"
                }
            ]
        },
        {
            "tid": "797",
            "cnname": "校园",
            "pid": "676",
            "childs": [
                {
                    "tid": "861",
                    "cnname": "校园热点",
                    "pid": "797",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/bce9db1f13944b02b071519a5eec2382.png"
                },
                {
                    "tid": "862",
                    "cnname": "活动家",
                    "pid": "797",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/f6e7b192a6e0f5eda58bc5cf960dceac.png"
                },
                {
                    "tid": "863",
                    "cnname": "心灵驿站",
                    "pid": "797",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/a0c95abcbeb8a731f4b42175c897caa8.png"
                },
                {
                    "tid": "864",
                    "cnname": "校媒FM",
                    "pid": "797",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/5f8c3655ce1cfe8670dfc2a559b523d0.png"
                },
                {
                    "tid": "865",
                    "cnname": "镜头说话",
                    "pid": "797",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/e96e6d1dc8a206e4531a6b23c7f0f5a5.png"
                },
                {
                    "tid": "492",
                    "cnname": "校园+",
                    "pid": "797",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/7478e71b2b063b325f8098c305c800fd.png"
                }
            ]
        },
        {
            "tid": "551",
            "cnname": "视频",
            "pid": "676",
            "childs": [
                {
                    "tid": "583",
                    "cnname": "资讯",
                    "pid": "551",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/53a25e2ee5197cda4a797daee98c0cdd.png"
                },
                {
                    "tid": "853",
                    "cnname": "我看见",
                    "pid": "551",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/d1ebc70d2dfd70c9e515a624618bacd1.png"
                },
                {
                    "tid": "599",
                    "cnname": "共青团新闻联播",
                    "pid": "551",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/33f1aeb3eccf7c35bbcd7c852aaa6395.png"
                },
                {
                    "tid": "600",
                    "cnname": "高校新闻联播",
                    "pid": "551",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/2914d3960996a58b5091c5a26b2d527f.png"
                },
                {
                    "tid": "578",
                    "cnname": "暖闻周刊",
                    "pid": "551",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/0eaebbc2087f112192dbe370273e6972.png"
                },
                {
                    "tid": "581",
                    "cnname": "中国好青年",
                    "pid": "551",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/848269c2226d578670199e4140da8f84.png"
                },
                {
                    "tid": "760",
                    "cnname": "中国吸引力",
                    "pid": "551",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/75a85307afed4eeb51591b28d02f17ac.jpg"
                },
                {
                    "tid": "664",
                    "cnname": "带着国旗去旅行",
                    "pid": "551",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/811b78a517da69201171ba2d26179c02.jpg"
                },
                {
                    "tid": "582",
                    "cnname": "精彩点播",
                    "pid": "551",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/4d1c172bec0e9321186dd968c8ccebc9.png"
                },
                {
                    "tid": "903",
                    "cnname": "中国青年说",
                    "pid": "551",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/1c57c7b121dacee31679c85469d1ef5e.png"
                }
            ]
        },
        {
            "tid": "803",
            "cnname": "国际",
            "pid": "676",
            "childs": [
                {
                    "tid": "866",
                    "cnname": "24时区",
                    "pid": "803",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/3ef6010f749cf358f2dc9be4c9277453.png"
                },
                {
                    "tid": "867",
                    "cnname": "国际观察",
                    "pid": "803",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/bec4fc16a0bb83f848c5ded6c86533f2.png"
                },
                {
                    "tid": "651",
                    "cnname": "青年参考",
                    "pid": "803",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/308ded8bf6ad347e367211c7d9456bb9.png"
                },
                {
                    "tid": "524",
                    "cnname": "国际+",
                    "pid": "803",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/35bb540fc9ac4dfa942480080c5c575b.png"
                }
            ]
        },
        {
            "tid": "804",
            "cnname": "财经",
            "pid": "676",
            "childs": [
                {
                    "tid": "805",
                    "cnname": "经济调查",
                    "pid": "804",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/8d7122ce6b9e9b1d4bef6aad979aa4f7.png"
                },
                {
                    "tid": "806",
                    "cnname": "青年经济说",
                    "pid": "804",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/564b1f53c429b008b6a589f73e7d1a64.png"
                },
                {
                    "tid": "559",
                    "cnname": "财经+",
                    "pid": "804",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/55975595d37d34ff464bf7f70460c07c.png"
                }
            ]
        },
        {
            "tid": "811",
            "cnname": "法治",
            "pid": "676",
            "childs": [
                {
                    "tid": "650",
                    "cnname": "法治+",
                    "pid": "811",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/0da78bebfe8760e68f10b8c0e7377a83.png"
                }
            ]
        },
        {
            "tid": "812",
            "cnname": "社会",
            "pid": "676",
            "childs": [
                {
                    "tid": "642",
                    "cnname": "第一时间",
                    "pid": "812",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/4eb109f73b8b7f49667d824d8ef09a91.png"
                },
                {
                    "tid": "567",
                    "cnname": "暖闻",
                    "pid": "812",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/d054db654f295a7cd489b1de08c492b9.png"
                },
                {
                    "tid": "511",
                    "cnname": "青年之声",
                    "pid": "812",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/d7b3e2fc4ddd993c0548c03f17b3a24c.png"
                },
                {
                    "tid": "479",
                    "cnname": "青年调查",
                    "pid": "812",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/4549cae6719ab6aad1f77b2c0c2bf69e.png"
                },
                {
                    "tid": "82",
                    "cnname": "舆情",
                    "pid": "812",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/4d8f71106cfd8e955d2303f8fef827b3.png"
                },
                {
                    "tid": "813",
                    "cnname": "社会+",
                    "pid": "812",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/ffb4c08eaec54cfe758dd2576f877397.png"
                }
            ]
        },
        {
            "tid": "814",
            "cnname": "体育",
            "pid": "676",
            "childs": [
                {
                    "tid": "870",
                    "cnname": "赛台",
                    "pid": "814",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/491e121c3a590a617e6a0c94f4fa619b.png"
                },
                {
                    "tid": "815",
                    "cnname": "足球",
                    "pid": "814",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/dc803eae26431e3fe802eaa7e8c5d8e7.png"
                },
                {
                    "tid": "817",
                    "cnname": "篮球",
                    "pid": "814",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/70aa740eef1b7ea6390297806d61b68d.png"
                },
                {
                    "tid": "871",
                    "cnname": "冬奥",
                    "pid": "814",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/2531c5995d69978f1fab404b8a07c451.png"
                },
                {
                    "tid": "816",
                    "cnname": "健身",
                    "pid": "814",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/f2d249cd55cf03612350b8f4cc4620f7.png"
                },
                {
                    "tid": "572",
                    "cnname": "体育+",
                    "pid": "814",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/aeae2849beab7ec95099ed1be0232a93.png"
                }
            ]
        },
        {
            "tid": "818",
            "cnname": "文化",
            "pid": "676",
            "childs": [
                {
                    "tid": "819",
                    "cnname": "悦读",
                    "pid": "818",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/e78c84ab6e42e1ead057b073af44c2ca.png"
                },
                {
                    "tid": "820",
                    "cnname": "影视",
                    "pid": "818",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/010aa348e2d19e8b3b0f6234ff510b1d.png"
                },
                {
                    "tid": "821",
                    "cnname": "国学",
                    "pid": "818",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/1397b84f8c769ca3790ce0b41779ee49.png"
                },
                {
                    "tid": "822",
                    "cnname": "文化观察",
                    "pid": "818",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/adf1fc133e6580e9508eda9b6758f67b.png"
                },
                {
                    "tid": "905",
                    "cnname": "舞台",
                    "pid": "818",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/a9237c2e813c2581fbe4a417ec140a6b.png"
                },
                {
                    "tid": "906",
                    "cnname": "展览",
                    "pid": "818",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/f55d11fb4fa4c94c2eb6bc5bb4b5311e.png"
                },
                {
                    "tid": "525",
                    "cnname": "文化+",
                    "pid": "818",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/e3fac4be9ae0fcbc3b780b0b3602ff10.png"
                }
            ]
        },
        {
            "tid": "826",
            "cnname": "军事",
            "pid": "676",
            "childs": [
                {
                    "tid": "827",
                    "cnname": "军情",
                    "pid": "826",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/ebb49e989e6bc094ff5b1a0d5d00af74.png"
                },
                {
                    "tid": "828",
                    "cnname": "军视",
                    "pid": "826",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/27ef43e00367b49a081092d5f3b19ad6.png"
                },
                {
                    "tid": "530",
                    "cnname": "军事+",
                    "pid": "826",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/5e26e95bb19fc27ed32e53e2a7e7f396.png"
                }
            ]
        },
        {
            "tid": "834",
            "cnname": "科技",
            "pid": "676",
            "childs": [
                {
                    "tid": "835",
                    "cnname": "科技前沿",
                    "pid": "834",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/243979bd77c1c9c2f6116fe3c4b953e4.png"
                },
                {
                    "tid": "509",
                    "cnname": "来点科学",
                    "pid": "834",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/0ed0531f7d536159b4cf829f291f8dc3.png"
                },
                {
                    "tid": "836",
                    "cnname": "科技+",
                    "pid": "834",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/2412cc3596394460a93e8354322bd419.png"
                }
            ]
        },
        {
            "tid": "837",
            "cnname": "汽车",
            "pid": "676",
            "childs": [
                {
                    "tid": "838",
                    "cnname": "汽车中国梦",
                    "pid": "837",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/b9d5e22afb2caf47881bf196f5e91b64.png"
                },
                {
                    "tid": "839",
                    "cnname": "未来启示录",
                    "pid": "837",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/3cc14b5182c03c2ed28b944206463355.png"
                },
                {
                    "tid": "872",
                    "cnname": "环球观",
                    "pid": "837",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/c784369aed7e9d6212628a68b830caf7.png"
                },
                {
                    "tid": "840",
                    "cnname": "青年说",
                    "pid": "837",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/d7351cc94d8da15e8fa63e6ae7649b3b.png"
                },
                {
                    "tid": "841",
                    "cnname": "匠人行",
                    "pid": "837",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/339ae5baae0f316f9ebe8df7472ab44d.png"
                },
                {
                    "tid": "532",
                    "cnname": "汽车+",
                    "pid": "837",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/84af672e177a242748f0d6a3bead5f22.png"
                }
            ]
        },
        {
            "tid": "842",
            "cnname": "创业",
            "pid": "676",
            "childs": [
                {
                    "tid": "843",
                    "cnname": "创客",
                    "pid": "842",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/a30b862cda5d0b963e4fc1e4ee893b66.png"
                },
                {
                    "tid": "844",
                    "cnname": "创课",
                    "pid": "842",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/7e5f8e33a6e7e5cd9face4324d5c6bfa.png"
                },
                {
                    "tid": "103",
                    "cnname": "KAB",
                    "pid": "842",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/5a219c8c39060b786a7596d3bb83e0dd.png"
                },
                {
                    "tid": "90",
                    "cnname": "创业+",
                    "pid": "842",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/6349580625875edb0ece1e8259ba0f3f.png"
                }
            ]
        },
        {
            "tid": "550",
            "cnname": "生活",
            "pid": "676",
            "childs": [
                {
                    "tid": "571",
                    "cnname": "旅游",
                    "pid": "550",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/724aeec0b257b61dabdc184568762509.png"
                },
                {
                    "tid": "873",
                    "cnname": "研学",
                    "pid": "550",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/4eb2793a2d86aa9dffc329b38d82c59c.png"
                },
                {
                    "tid": "655",
                    "cnname": "健康",
                    "pid": "550",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/ae256067c3a2a82698c6da23b3646192.png"
                },
                {
                    "tid": "657",
                    "cnname": "心理",
                    "pid": "550",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/01fd15e649788a91a2f334d5d439ee9e.png"
                },
                {
                    "tid": "846",
                    "cnname": "美食",
                    "pid": "550",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/58e024d6f35aca9d360340212422fdb2.png"
                },
                {
                    "tid": "656",
                    "cnname": "情感",
                    "pid": "550",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/2bad3fa1aa3a7fb7e0ef11d0f99d8cc3.png"
                },
                {
                    "tid": "847",
                    "cnname": "生活+",
                    "pid": "550",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/89cdbc4a81bcd645908922d7c6954b39.png"
                }
            ]
        },
        {
            "tid": "848",
            "cnname": "视觉",
            "pid": "676",
            "childs": [
                {
                    "tid": "746",
                    "cnname": "微光",
                    "pid": "848",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/af34cfbe780aaca53cb36fa2e30e6bfe.jpg"
                },
                {
                    "tid": "576",
                    "cnname": "视觉+",
                    "pid": "848",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/733faf7036a8ba38f27d90d7dc630e63.jpg"
                }
            ]
        },
        {
            "tid": "849",
            "cnname": "中青号",
            "pid": "676",
            "childs": [
                {
                    "tid": "850",
                    "cnname": "青年时讯",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/b41da9e0962118e2d8f820a002f23b78.png"
                },
                {
                    "tid": "674",
                    "cnname": "中国青年作家报",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/7d06061ac8d54961ccc0bc8902332d48.png"
                },
                {
                    "tid": "646",
                    "cnname": "冰点推荐",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/fde80b52896a206f4edc87a50cd21f09.png"
                },
                {
                    "tid": "648",
                    "cnname": "深度调查",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/c2653e548eb21ebaeaff08624d7376a1.png"
                },
                {
                    "tid": "759",
                    "cnname": "青椒",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/85477a74f8282ac5143495a0f00b08ed.png"
                },
                {
                    "tid": "654",
                    "cnname": "我找",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/457980a1dbf3fb43b084bae83c661aaf.png"
                },
                {
                    "tid": "653",
                    "cnname": "职场",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/25267c45b588373c7734c8c428d715b9.png"
                },
                {
                    "tid": "761",
                    "cnname": "陕西工业职业技术学院",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/83f983ffab41566ca49cba637513d902.png"
                },
                {
                    "tid": "758",
                    "cnname": "无锡职业技术学院",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/25baa6c5ef8f759d0a1065644104949d.png"
                },
                {
                    "tid": "757",
                    "cnname": "兰州资源环境职业技术学院",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/77915cfe1c78b22d600437b89ee9a134.png"
                },
                {
                    "tid": "756",
                    "cnname": "湖南铁道职业技术学院",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/31a8dbb378071886ea17094f88c264b5.png"
                },
                {
                    "tid": "755",
                    "cnname": "陕西铁路工程职业技术学院",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/b35e66e2ecc0bee3a61ea2670a33252c.png"
                },
                {
                    "tid": "754",
                    "cnname": "南京工业职业技术学院",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/a8183fc6791b81a9ddf7795b8a4f4201.jpg"
                },
                {
                    "tid": "753",
                    "cnname": "西安航空职业技术学院",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/548cdfcbde059258d9dccfab796c69d1.png"
                },
                {
                    "tid": "752",
                    "cnname": "重庆工程职业技术学院",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/977c4050371b3b5108738fab2fc310c5.png"
                },
                {
                    "tid": "751",
                    "cnname": "天津职业大学",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/cc688455d5ed4eabbbad4b8963cbc20f.png"
                },
                {
                    "tid": "750",
                    "cnname": "四川交通职业技术学院",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/e3edb195222670d9e8f9e619f5925aff.png"
                },
                {
                    "tid": "749",
                    "cnname": "深圳职业技术学院",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/c99e1360c7f3fa440cf2e5977ddbb06f.png"
                },
                {
                    "tid": "748",
                    "cnname": "日照职业技术学院",
                    "pid": "849",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/b3e7781eaf5dc6a7e2f2c93e733bf7db.png"
                }
            ]
        },
        {
            "tid": "668",
            "cnname": "榜样阅读",
            "pid": "676",
            "childs": [
                {
                    "tid": "673",
                    "cnname": "榜样故事",
                    "pid": "668",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/b9d4f364e174e4472770253b102369f4.png"
                },
                {
                    "tid": "669",
                    "cnname": "邀你共读",
                    "pid": "668",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/e0de6ae11234ec33305babb8fbc354ec.png"
                },
                {
                    "tid": "670",
                    "cnname": "个性解读",
                    "pid": "668",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/ede6260e23dbdd39ad4683334b40dee5.png"
                },
                {
                    "tid": "671",
                    "cnname": "独家对话",
                    "pid": "668",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/aa15c1d32b5a4db61baa78499517fc14.png"
                },
                {
                    "tid": "672",
                    "cnname": "幕后花絮",
                    "pid": "668",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/d3e3bf4bda504828d338aff600ee63bb.png"
                }
            ]
        },
        {
            "tid": "624",
            "cnname": "青秀H5",
            "pid": "676",
            "childs": [
                {
                    "tid": "625",
                    "cnname": "时政解读",
                    "pid": "624",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/a68ccad6fbd472511ad15235f4ce15ce.png"
                },
                {
                    "tid": "626",
                    "cnname": "中青报道",
                    "pid": "624",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/bbfc736f23739a229d642ca6fc4c23e7.png"
                },
                {
                    "tid": "627",
                    "cnname": "校园精品",
                    "pid": "624",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/201c7314cc5dbfa1f803cd776a10a58c.png"
                },
                {
                    "tid": "628",
                    "cnname": "定制产品",
                    "pid": "624",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/86bc3b598130da742cd725d9de002af4.png"
                },
                {
                    "tid": "629",
                    "cnname": "小游戏",
                    "pid": "624",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/92a719ce76e7c9466d5d727da91f1b8c.png"
                }
            ]
        },
        {
            "tid": "859",
            "cnname": "专题",
            "pid": "676",
            "childs": [
                {
                    "tid": "566",
                    "cnname": "时事",
                    "pid": "859",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/e7053d03b6ad2e556114d816963c7aa0.png"
                }
            ]
        },
        {
            "tid": "658",
            "cnname": "活动",
            "pid": "676",
            "childs": [
                {
                    "tid": "659",
                    "cnname": "青创",
                    "pid": "658",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/38cb4b1ebf54a29857170656a7eaf677.png"
                },
                {
                    "tid": "660",
                    "cnname": "校园活动",
                    "pid": "658",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/d669f69c0c47369ef8ad38be0d1f0d8e.png"
                },
                {
                    "tid": "661",
                    "cnname": "中青活动家",
                    "pid": "658",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/fb507081ab176d90c614933ca680b7ea.png"
                }
            ]
        },
        {
            "tid": "602",
            "cnname": "思想者",
            "pid": "676",
            "childs": [
                {
                    "tid": "645",
                    "cnname": "青·学习",
                    "pid": "602",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/b1ed36a9dd33bead1c956670657be4f7.png"
                },
                {
                    "tid": "603",
                    "cnname": "青·理论",
                    "pid": "602",
                    "typeimg": "https://shareapp.cyol.com/"
                },
                {
                    "tid": "605",
                    "cnname": "青·声音",
                    "pid": "602",
                    "typeimg": "https://shareapp.cyol.com/"
                },
                {
                    "tid": "606",
                    "cnname": "青·体验",
                    "pid": "602",
                    "typeimg": "https://shareapp.cyol.com/"
                },
                {
                    "tid": "607",
                    "cnname": "青·视野",
                    "pid": "602",
                    "typeimg": "https://shareapp.cyol.com/"
                },
                {
                    "tid": "604",
                    "cnname": "青·研究",
                    "pid": "602",
                    "typeimg": "https://shareapp.cyol.com/"
                }
            ]
        },
        {
            "tid": "875",
            "cnname": "两会",
            "pid": "676",
            "childs": [
                {
                    "tid": "883",
                    "cnname": "进行时",
                    "pid": "875",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/b8c7028a2abb35abc921a6e5ddd4131b.png"
                },
                {
                    "tid": "876",
                    "cnname": "中青视线",
                    "pid": "875",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/556cdd67b7c4022fb1ed660ececf348a.png"
                },
                {
                    "tid": "884",
                    "cnname": "青小豹评两会",
                    "pid": "875",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/5bebeb96812380f85065fd299168f06e.png"
                },
                {
                    "tid": "877",
                    "cnname": "青年大学习",
                    "pid": "875",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/8a322a84d5212ef6221d226d11cf124f.png"
                },
                {
                    "tid": "878",
                    "cnname": "两会青年说",
                    "pid": "875",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/dea4f81d1ce9755df84b684f9c203962.png"
                },
                {
                    "tid": "879",
                    "cnname": "我看见·两会",
                    "pid": "875",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/2e380216967ef395cbbfb68961bf9efc.png"
                },
                {
                    "tid": "880",
                    "cnname": "奔跑吧追梦人",
                    "pid": "875",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/f9c5d2e762797deaf21453d4b4e74c02.png"
                },
                {
                    "tid": "881",
                    "cnname": "部长之声",
                    "pid": "875",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/7ab6b83ad4ae0dcbce63bf9143d911af.png"
                },
                {
                    "tid": "882",
                    "cnname": "代表委员之声",
                    "pid": "875",
                    "typeimg": "https://shareapp.cyol.com/cmsfile/thumb/d263e2a3aecc1090089b4bc0c2e16e0c.png"
                }
            ]
        },
        {
            "tid": "0",
            "cnname": "订阅",
            "pid": "0",
            "childs": []
        }
    ],
    "msg": "ok",
    "code": "200"
}
"""
