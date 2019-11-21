from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from news_all.tools.time_translater import Pubtime


class Oeeee(NewsRCSpider):
    name = 'oeeee'

    # 奥一网 ==》 补充全站采集
    mystart_urls = {
        'http://www.oeeee.com/': 6442,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/china': 6443,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/opinion': 6444,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/depth': 6445,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/economy': 6446,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/ent': 6447,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/sports': 6448,  # 奥一网
        'http://ndauto.oeeee.com/': 6449,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/gz': 6450,  # 奥一网
        'https://sz.oeeee.com/': 6451,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/dg': 6452,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/fs': 6453,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/zh': 6454,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/zs': 6455,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/jm': 6456,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/hz': 6457,  # 奥一网
        'http://baoliao.oeeee.com/': 6458,  # 奥一网
        'http://baoliao.oeeee.com/baoliao/newList': 6459,  # 奥一网
        'http://baoliao.oeeee.com/baoliao/hotList': 6460,  # 奥一网
        'http://baoliao.oeeee.com/baoliao/follow': 6461,  # 奥一网
        'http://baoliao.oeeee.com/baoliao/bang': 6462,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/szjf': 6463,  # 奥一网
        'http://finance.oeeee.com/': 6464,  # 奥一网
        'http://finance.oeeee.com/api/channel.php?s=/index/index/channel/moneyrule': 6465,  # 奥一网
        'http://finance.oeeee.com/api/channel.php?s=/index/index/channel/moneystreet': 6466,  # 奥一网
        'http://finance.oeeee.com/api/channel.php?s=/index/index/channel/caishen': 6467,  # 奥一网
        'http://finance.oeeee.com/api/channel.php?s=/index/index/channel/ducai': 6468,  # 奥一网
        'http://finance.oeeee.com/api/channel.php?s=/index/index/channel/icaiwan': 6469,  # 奥一网
        'http://finance.oeeee.com/api/channel.php?s=/index/index/channel/visibility': 6470,  # 奥一网
        'http://szhome.oeeee.com/': 6471,  # 奥一网
        'http://szhome.oeeee.com/api/house.php?s=house/channels/channel/zixun': 6472,  # 奥一网
        'http://szhome.oeeee.com/api/house.php?s=house/channels/channel/buyings': 6473,  # 奥一网
        'http://szhome.oeeee.com/api/house.php?s=house/channels/channel/rolling': 6474,  # 奥一网
        'http://edu.oeeee.com/': 6475,  # 奥一网
        'https://edu.oeeee.com/api/channel.php?s=/index/index/channel/jyzx': 6476,  # 奥一网
        'https://edu.oeeee.com/api/channel.php?s=/index/index/channel/msdjt': 6477,  # 奥一网
        'http://health.oeeee.com/api/channel.php?s=/index/index/channel/jkkx': 6478,  # 奥一网
        'http://health.oeeee.com/api/channel.php?s=/index/index/channel/ys': 6479,  # 奥一网
        'http://health.oeeee.com/api/channel.php?s=/index/index/channel/my': 6480,  # 奥一网
        'http://health.oeeee.com/api/channel.php?s=/index/index/channel/zx': 6481,  # 奥一网
        'http://life.oeeee.com/': 6482,  # 奥一网
        'http://life.oeeee.com/food/': 6483,  # 奥一网
        'http://life.oeeee.com/shopping/': 6484,  # 奥一网
        'http://life.oeeee.com/yellowpage/': 6485,  # 奥一网
        'http://life.oeeee.com/licai/': 6486,  # 奥一网
        'http://life.oeeee.com/liferoll/': 6487,  # 奥一网
        'https://epaper.oeeee.com/epaper/A/html/2019-11/01/node_16577.htm': 6488,  # 奥一网
        'https://epaper.oeeee.com/epaper/G/html/2019-11/01/node_16466.htm': 6489,  # 奥一网
        'https://epaper.oeeee.com/epaper/H/html/2019-11/01/node_16551.htm': 6490,  # 奥一网
        'https://epaper.oeeee.com/epaper/I/html/2019-11/01/node_16462.htm': 6491,  # 奥一网
        'https://epaper.oeeee.com/epaper/K/html/2019-11/01/node_16468.htm': 6492,  # 奥一网
        'https://epaper.oeeee.com/epaper/J/html/2019-11/01/node_16490.htm': 6493,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/ndVediolist': 6494,  # 奥一网
        'http://live.oeeee.com/': 6495,  # 奥一网
        'http://zt3.oeeee.com/2019ssgg/zcgg.html': 6496,  # 奥一网
        'http://zt3.oeeee.com/2019ssgg/rdwt.html': 6497,  # 奥一网
        'http://zt3.oeeee.com/2019ssgg/tssg.html': 6498,  # 奥一网
        'http://zt3.oeeee.com/2019ssgg/sp.html': 6499,  # 奥一网
        'http://www.oeeee.com/api/channel.php?s=/index/index/channel/index': 6500,  # 奥一网
        'https://www.oeeee.com/api/index.php?s=/Wxjhealth/index': 6501,  # 奥一网
      #  'https://www.oeeee.com/api/index.php?s=/Wxjhealth/index': 6502,  # 奥一网  #域名重复
      #  'https://www.oeeee.com/api/index.php?s=/Wxjhealth/index': 6503,  # 奥一网  #域名重复
      #  'https://www.oeeee.com/api/index.php?s=/Wxjhealth/index': 6504,  # 奥一网  #域名重复
      #  'https://www.oeeee.com/api/index.php?s=/Wxjhealth/index': 6505,  # 奥一网  #域名重复
      #  'https://www.oeeee.com/api/index.php?s=/Wxjhealth/index': 6506,  # 奥一网  #域名重复
        'http://www.oeeee.com/api/index.php?s=/Fastread/sz': 6507,  # 奥一网
        'http://sztong.oeeee.com/lht/': 6508,  # 奥一网

    }

    rules = (

        # https://m.mp.oeeee.com/a/BAAFRD000020191029221228.html
        # http://www.oeeee.com/html/201910/29/833368.html
        # http://baoliao.oeeee.com/index/show/id/181174.html
        Rule(LinkExtractor(allow=r'.oeeee.com/a/\w{10}%s\d{2}\d+\.html' % datetime.today().strftime('%Y%m'),),
             callback='parse_item',
             follow=False),

        Rule(LinkExtractor(allow=r'.oeeee.com/html/%s/\d{2}/\d+\.html' % datetime.today().strftime('%Y%m'), ),
             callback='parse_item_3',
             follow=False),
        Rule(LinkExtractor(allow=r'.oeeee.com/index/show/id/\d+\.html'),
             callback='parse_item_4',
             follow=False),

        Rule(LinkExtractor(allow=r'oeeee.com/.*?\.html', deny=(r'/201[0-8]', r'/20190[1-9]', r'/20191[0]'),),
             process_request=otherurl_meta,
             follow=False),
    )


    def parse_item(self, response):
        # https://m.mp.oeeee.com/a/BAAFRD000020191029221228.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//h2[@class='rich_media_title']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//span[@class='introduce']/text()").extract_first())
            content_div = xp("//div[@id='docContent']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=True,
                                                                     kill_xpaths=[r"//div[@id='zanshang']",
                                                                                  r"//div[@class='title']",
                                                                                  r"//div[@class='sourcelist sourcelist1 border-around clearfix']",
                                                                                  r"//div[@id='buyCopyright']"])  # str  list
            origin_name = xp("//span[@class='name avatar_click']/text()").extract_first()# None  不要用[0]
        except Exception as e:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_2(self, response):
        # 有视频
        # https://m.mp.oeeee.com/a/BAAFRD000020191029221228.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//h2[@class='rich_media_title']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//span[@class='introduce']/text()").extract_first())
            content_div = xp("//div[@id='DocSummary']")[0]
            content, media, _, _ = self.content_clean(content_div)  # str  list
            video_url = xp("//video/source[@type='video/mp4']/@src").get()
            videos = {'1': {'src': video_url}}
            origin_name = xp("//span[@class='name avatar_click']/text()").extract_first()  # None  不要用[0]
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_3(self, response):
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='title']/h1/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//span[@class='time']/text()").extract_first())
            content_div = xp("//div[@class='content']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False,)  # str  list
            origin_name = xp("//span[@class='source']/text()").extract_first()  # None  不要用[0]
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_4(self, response):
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//h1[@class='title mr']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//span[@class='time']/text()").extract_first())
            content_div = xp("//div[@class='content']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False,)  # str  list
            origin_name = "奥一报料"  # None  不要用[0]
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,

        )




