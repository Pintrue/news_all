from copy import deepcopy
from scrapy import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news_all.tools.time_translater import Pubtime
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime


class PeopleSpider(NewsRCSpider):
    name = 'mrjjnews'
    mystart_urls = {
        'http://www.nbd.com.cn/': 7466,  # 每日经济新闻
        'http://economy.nbd.com.cn/': 7467,  # 每日经济新闻
        'http://economy.nbd.com.cn/columns/313': 7468,  # 每日经济新闻
        'http://economy.nbd.com.cn/columns/475': 7469,  # 每日经济新闻
        'http://finance.nbd.com.cn/': 7470,  # 每日经济新闻
        'http://finance.nbd.com.cn/columns/329': 7471,  # 每日经济新闻
        'http://finance.nbd.com.cn/columns/415': 7472,  # 每日经济新闻
        'http://finance.nbd.com.cn/columns/327': 7473,  # 每日经济新闻
        'http://finance.nbd.com.cn/columns/326': 7474,  # 每日经济新闻
        'http://industry.nbd.com.cn/': 7475,  # 每日经济新闻
        'http://industry.nbd.com.cn/columns/346': 7476,  # 每日经济新闻
        'http://industry.nbd.com.cn/columns/585': 7477,  # 每日经济新闻
        'http://industry.nbd.com.cn/columns/418': 7478,  # 每日经济新闻
        'http://industry.nbd.com.cn/columns/586': 7479,  # 每日经济新闻
        'http://industry.nbd.com.cn/columns/587': 7480,  # 每日经济新闻
        'http://www.nbd.com.cn/video': 7481,  # 每日经济新闻
        'http://www.nbd.com.cn/video?column_id=1038': 7482,  # 每日经济新闻
        'http://www.nbd.com.cn/video?column_id=1043': 7483,  # 每日经济新闻
        'http://www.nbd.com.cn/video?column_id=1040': 7484,  # 每日经济新闻
        'http://www.nbd.com.cn/video?column_id=1041': 7485,  # 每日经济新闻
        'http://www.nbd.com.cn/video?column_id=1044': 7486,  # 每日经济新闻
        'http://www.nbd.com.cn/video?column_id=1042': 7487,  # 每日经济新闻
        'http://www.nbd.com.cn/video?column_id=1039': 7488,  # 每日经济新闻
        'http://stocks.nbd.com.cn/': 7489,  # 每日经济新闻
        'http://stocks.nbd.com.cn/columns/318': 7490,  # 每日经济新闻
        'http://stocks.nbd.com.cn/columns/275': 7491,  # 每日经济新闻
        'http://stocks.nbd.com.cn/columns/28': 7492,  # 每日经济新闻
        'http://stocks.nbd.com.cn/columns/476': 7493,  # 每日经济新闻
        'http://stocks.nbd.com.cn/columns/405': 7494,  # 每日经济新闻
        'http://stocks.nbd.com.cn/columns/800': 7495,  # 每日经济新闻
        'http://www.nbd.com.cn/kechuang': 7496,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/1024': 7497,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/1025': 7498,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/1026': 7499,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/1027': 7500,  # 每日经济新闻
        'http://money.nbd.com.cn/': 7501,  # 每日经济新闻
        'http://money.nbd.com.cn/columns/440': 7502,  # 每日经济新闻
        'http://money.nbd.com.cn/columns/441': 7503,  # 每日经济新闻
        'http://money.nbd.com.cn/columns/439': 7504,  # 每日经济新闻
        'http://money.nbd.com.cn/columns/589': 7505,  # 每日经济新闻
        'http://money.nbd.com.cn/columns/801': 7506,  # 每日经济新闻
        'http://auto.nbd.com.cn/': 7507,  # 每日经济新闻
        'http://auto.nbd.com.cn/columns/140': 7508,  # 每日经济新闻
        'http://auto.nbd.com.cn/columns/261': 7509,  # 每日经济新闻
        'http://auto.nbd.com.cn/columns/132': 7510,  # 每日经济新闻
        'http://auto.nbd.com.cn/columns/511': 7511,  # 每日经济新闻
        'http://auto.nbd.com.cn/columns/337': 7512,  # 每日经济新闻
        'http://www.nbd.com.cn/fangchan': 7513,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/fangchan/300': 7514,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/fangchan/301': 7515,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/fangchan/302': 7516,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/fangchan/304': 7517,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/fangchan/305': 7518,  # 每日经济新闻
        'http://movie.nbd.com.cn/': 7519,  # 每日经济新闻
        'http://movie.nbd.com.cn/columns/492': 7520,  # 每日经济新闻
        'http://movie.nbd.com.cn/columns/493': 7521,  # 每日经济新闻
        'http://movie.nbd.com.cn/columns/494': 7522,  # 每日经济新闻
        'http://movie.nbd.com.cn/columns/495': 7523,  # 每日经济新闻
        'http://tmt.nbd.com.cn/': 7524,  # 每日经济新闻
        'http://tmt.nbd.com.cn/columns/478': 7525,  # 每日经济新闻
        'http://tmt.nbd.com.cn/columns/838': 7526,  # 每日经济新闻
        'http://tmt.nbd.com.cn/columns/448': 7527,  # 每日经济新闻
        'http://tmt.nbd.com.cn/columns/451': 7528,  # 每日经济新闻
        'http://tmt.nbd.com.cn/columns/839': 7529,  # 每日经济新闻
        'http://tmt.nbd.com.cn/columns/841': 7530,  # 每日经济新闻
        'http://tmt.nbd.com.cn/columns/981': 7531,  # 每日经济新闻
        'http://tmt.nbd.com.cn/columns/842': 7532,  # 每日经济新闻
        'http://tmt.nbd.com.cn/columns/843': 7533,  # 每日经济新闻
        'http://cd.nbd.com.cn/': 7534,  # 每日经济新闻
        'http://cd.nbd.com.cn/columns/578': 7535,  # 每日经济新闻
        'http://cd.nbd.com.cn/columns/579': 7536,  # 每日经济新闻
        'http://cd.nbd.com.cn/columns/580': 7537,  # 每日经济新闻
        'http://fx.nbd.com.cn/': 7538,  # 每日经济新闻
        'http://fx.nbd.com.cn/columns/832': 7539,  # 每日经济新闻
        'http://fx.nbd.com.cn/columns/833': 7540,  # 每日经济新闻
        'http://fx.nbd.com.cn/columns/835': 7541,  # 每日经济新闻
        'http://fx.nbd.com.cn/columns/836': 7542,  # 每日经济新闻
        'http://fx.nbd.com.cn/columns/837': 7543,  # 每日经济新闻
        'http://www.nbd.com.cn/corp/waiguangzhui/index.html': 7544,  # 每日经济新闻
        'http://www.nbd.com.cn/corp/waiguangzhui/zixun.html': 7545,  # 每日经济新闻
        'http://www.nbd.com.cn/xinsanban': 7546,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/3': 7547,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/1072': 7548,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/697': 7549,  # 每日经济新闻
        'http://world.nbd.com.cn/': 7550,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/8': 7551,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/402': 7552,  # 每日经济新闻
        'http://www.nbd.com.cn/columns/416': 7553,  # 每日经济新闻

    }
    #http://www.nbd.com.cn/articles/2019-11-18/1386925.html

    rules = (
        Rule(LinkExtractor(allow=r'nbd.com.cn/articles/%s-\d{2}/\d+\.html' % datetime.today().strftime('%Y-%m'),
                           ),
             callback='parse_item',follow=False),
        Rule(LinkExtractor(allow=(r'nbd.com.cn/.*\.html',)
                           ),
             process_request=otherurl_meta, follow=False),
    )


    def parse_item(self, response):
        # http://www.nbd.com.cn/articles/2019-11-18/1386925.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='g-article-top']/h1").extract_first("")
            pubtime = Pubtime(xp("//span[@class='time']/text()").extract_first(""))
            content_div = xp("//div[@class='g-articl-text']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//span[@class='source']/text()").extract_first("")
        except:
            return self.parse_item_2(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_2(self, response):

     #http://www.cb.com.cn/index/show/gx/cv/cv135195161336
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp("//div[@class='m-articleBox']/h1").extract_first("")
            pubtime = Pubtime(xp("//div[@class='m-creatTime']/span[2]/text()").extract_first(""))
            content_div = xp("//div[@class='m-articleContent']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, kill_xpaths=[],)
            origin_name = xp("//span[@class='u-clomun']/text()").extract_first("")

        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,
            content=content,
            media=media,
            videos=videos,

        )
