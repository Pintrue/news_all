from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from news_all.tools.time_translater import Pubtime


class D1xz(NewsRCSpider):
    name = 'd1xz'

    # 第一星座网 ==》 补充全站采集
    mystart_urls = {
        ' https://www.d1xz.net/': 1,   #  第一星座网
        'https://www.d1xz.net/astro/': 2,   #  第一星座网
        'https://www.d1xz.net/astro/kaiyun/': 3,   #  第一星座网
        'https://www.d1xz.net/astro/aiqing/': 4,   #  第一星座网
        'https://www.d1xz.net/astro/gexing/': 5,   #  第一星座网
        'https://www.d1xz.net/astro/zhishi/': 6,   #  第一星座网
        'https://www.d1xz.net/astro/Qinggan/': 7,   #  第一星座网
        'https://www.d1xz.net/astro/xinggan/': 8,   #  第一星座网
        'https://www.d1xz.net/astro/shishang/': 9,   #  第一星座网
        'https://www.d1xz.net/yunshi/': 10,   #  第一星座网
        'https://www.d1xz.net/yunshi/today/Aries/': 11,   #  第一星座网
        'https://www.d1xz.net/yunshi/tomorrow/Aries/': 12,   #  第一星座网
        'https://www.d1xz.net/yunshi/week/Aries/': 13,   #  第一星座网
        'https://www.d1xz.net/yunshi/nextweek/Aries/': 14,   #  第一星座网
        'https://www.d1xz.net/yunshi/month/Aries/': 15,   #  第一星座网
        'https://www.d1xz.net/yunshi/today/Taurus/': 16,   #  第一星座网
        'https://www.d1xz.net/yunshi/tomorrow/Taurus/': 17,   #  第一星座网
        'https://www.d1xz.net/yunshi/week/Taurus/': 18,   #  第一星座网
        'https://www.d1xz.net/yunshi/nextweek/Taurus/': 19,   #  第一星座网
        'https://www.d1xz.net/yunshi/month/Taurus/': 20,   #  第一星座网
        'https://www.d1xz.net/yunshi/today/Gemini/': 21,   #  第一星座网
        'https://www.d1xz.net/yunshi/tomorrow/Gemini/': 22,   #  第一星座网
        'https://www.d1xz.net/yunshi/week/Gemini/': 23,   #  第一星座网
        'https://www.d1xz.net/yunshi/nextweek/Gemini/': 24,   #  第一星座网
        'https://www.d1xz.net/yunshi/month/Gemini/': 25,   #  第一星座网
        'https://www.d1xz.net/yunshi/today/Cancer/': 26,   #  第一星座网
        'https://www.d1xz.net/yunshi/tomorrow/Cancer/': 27,   #  第一星座网
        'https://www.d1xz.net/yunshi/week/Cancer/': 28,   #  第一星座网
        'https://www.d1xz.net/yunshi/nextweek/Cancer/': 29,   #  第一星座网
        'https://www.d1xz.net/yunshi/month/Cancer/': 30,   #  第一星座网
        'https://www.d1xz.net/yunshi/today/Leo/': 31,   #  第一星座网
        'https://www.d1xz.net/yunshi/tomorrow/Leo/': 32,   #  第一星座网
        'https://www.d1xz.net/yunshi/week/Leo/': 33,   #  第一星座网
        'https://www.d1xz.net/yunshi/nextweek/Leo/': 34,   #  第一星座网
        'https://www.d1xz.net/yunshi/month/Leo/': 35,   #  第一星座网
        'https://www.d1xz.net/yunshi/today/Virgo/': 36,   #  第一星座网
        'https://www.d1xz.net/yunshi/tomorrow/Virgo/': 37,   #  第一星座网
        'https://www.d1xz.net/yunshi/week/Virgo/': 38,   #  第一星座网
        'https://www.d1xz.net/yunshi/nextweek/Virgo/': 39,   #  第一星座网
        'https://www.d1xz.net/yunshi/month/Virgo/': 40,   #  第一星座网
        'https://www.d1xz.net/yunshi/today/Libra/': 41,   #  第一星座网
        'https://www.d1xz.net/yunshi/tomorrow/Libra/': 42,   #  第一星座网
        'https://www.d1xz.net/yunshi/week/Libra/': 43,   #  第一星座网
        'https://www.d1xz.net/yunshi/nextweek/Libra/': 44,   #  第一星座网
        'https://www.d1xz.net/yunshi/month/Libra/': 45,   #  第一星座网
        'https://www.d1xz.net/yunshi/today/Scorpio/': 46,   #  第一星座网
        'https://www.d1xz.net/yunshi/tomorrow/Scorpio/': 47,   #  第一星座网
        'https://www.d1xz.net/yunshi/week/Scorpio/': 48,   #  第一星座网
        'https://www.d1xz.net/yunshi/nextweek/Scorpio/': 49,   #  第一星座网
        'https://www.d1xz.net/yunshi/month/Scorpio/': 50,   #  第一星座网
        'https://www.d1xz.net/yunshi/today/Sagittarius/': 51,   #  第一星座网
        'https://www.d1xz.net/yunshi/tomorrow/Sagittarius/': 52,   #  第一星座网
        'https://www.d1xz.net/yunshi/week/Sagittarius/': 53,   #  第一星座网
        'https://www.d1xz.net/yunshi/nextweek/Sagittarius/': 54,   #  第一星座网
        'https://www.d1xz.net/yunshi/month/Sagittarius/': 55,   #  第一星座网
        'https://www.d1xz.net/yunshi/today/Capricorn/': 56,   #  第一星座网
        'https://www.d1xz.net/yunshi/tomorrow/Capricorn/': 57,   #  第一星座网
        'https://www.d1xz.net/yunshi/week/Capricorn/': 58,   #  第一星座网
        'https://www.d1xz.net/yunshi/nextweek/Capricorn/': 59,   #  第一星座网
        'https://www.d1xz.net/yunshi/month/Capricorn/': 60,   #  第一星座网
        'https://www.d1xz.net/yunshi/today/Aquarius/': 61,   #  第一星座网
        'https://www.d1xz.net/yunshi/tomorrow/Aquarius/': 62,   #  第一星座网
        'https://www.d1xz.net/yunshi/week/Aquarius/': 63,   #  第一星座网
        'https://www.d1xz.net/yunshi/nextweek/Aquarius/': 64,   #  第一星座网
        'https://www.d1xz.net/yunshi/month/Aquarius/': 65,   #  第一星座网
        'https://www.d1xz.net/yunshi/today/Pisces/': 66,   #  第一星座网
        'https://www.d1xz.net/yunshi/tomorrow/Pisces/': 67,   #  第一星座网
        'https://www.d1xz.net/yunshi/week/Pisces/': 68,   #  第一星座网
        'https://www.d1xz.net/yunshi/nextweek/Pisces/': 69,   #  第一星座网
        'https://www.d1xz.net/yunshi/month/Pisces/': 70,   #  第一星座网
        'https://www.d1xz.net/test/': 71,   #  第一星座网
        'https://www.d1xz.net/test/aiqing/': 72,   #  第一星座网
        'https://www.d1xz.net/test/gexing/': 73,   #  第一星座网
        'https://www.d1xz.net/test/quwei/': 74,   #  第一星座网
        'https://www.d1xz.net/test/caifu/': 75,   #  第一星座网
        'https://www.d1xz.net/test/zhishang/': 76,   #  第一星座网
        'https://www.d1xz.net/test/zhiye/': 77,   #  第一星座网
        'https://www.d1xz.net/test/shejiao/': 78,   #  第一星座网
        'https://www.d1xz.net/test/zonghe/': 79,   #  第一星座网
        'https://www.d1xz.net/jm/': 80,   #  第一星座网
        'https://www.d1xz.net/jm/xifang/': 81,   #  第一星座网
        'https://www.d1xz.net/jm/renwu/': 82,   #  第一星座网
        'https://www.d1xz.net/jm/shenghuo/': 83,   #  第一星座网
        'https://www.d1xz.net/jm/dongwu/': 84,   #  第一星座网
        'https://www.d1xz.net/jm/zhiwu/': 85,   #  第一星座网
        'https://www.d1xz.net/jm/wupin/': 86,   #  第一星座网
        'https://www.d1xz.net/jm/shenti/': 87,   #  第一星座网
        'https://www.d1xz.net/jm/guishen/': 88,   #  第一星座网
        'https://www.d1xz.net/jm/jianzhu/': 89,   #  第一星座网
        'https://www.d1xz.net/jm/ziran/': 90,   #  第一星座网
        'https://www.d1xz.net/jm/qingai/': 91,   #  第一星座网
        'https://www.d1xz.net/jm/yunfu/': 92,   #  第一星座网
        'https://www.d1xz.net/jm/qita/': 93,   #  第一星座网
        'https://www.d1xz.net/jm/gushi/': 94,   #  第一星座网
        'https://www.d1xz.net/jm/jiemengdaquan/': 95,   #  第一星座网
        'https://www.d1xz.net/jm/jiexi/': 96,   #  第一星座网
        'https://www.d1xz.net/sm/': 97,   #  第一星座网
        'https://www.d1xz.net/sm/bazi.aspx': 98,   #  第一星座网
        'https://www.d1xz.net/sm/xingming-test.aspx': 99,   #  第一星座网
        'https://www.d1xz.net/sx/': 100,   #  第一星座网
        'https://www.d1xz.net/sx/zonghe/2019nianshengxiaoyuncheng/': 101,   #  第一星座网
        'https://www.d1xz.net/sx/zonghe/': 102,   #  第一星座网
        'https://www.d1xz.net/sx/jieshuo/': 103,   #  第一星座网
        'https://www.d1xz.net/sx/xingge/': 104,   #  第一星座网
        'https://www.d1xz.net/sx/aiqing/': 105,   #  第一星座网
        'https://www.d1xz.net/sx/shu/index_1.aspx': 106,   #  第一星座网
        'https://www.d1xz.net/sx/niu/index_1.aspx': 107,   #  第一星座网
        'https://www.d1xz.net/sx/hu/index_1.aspx': 108,   #  第一星座网
        'https://www.d1xz.net/sx/tu/index_1.aspx': 109,   #  第一星座网
        'https://www.d1xz.net/sx/long/index_1.aspx': 110,   #  第一星座网
        'https://www.d1xz.net/sx/she/index_1.aspx': 111,   #  第一星座网
        'https://www.d1xz.net/sx/ma/index_1.aspx': 112,   #  第一星座网
        'https://www.d1xz.net/sx/yang/index_1.aspx': 113,   #  第一星座网
        'https://www.d1xz.net/sx/hou/index_1.aspx': 114,   #  第一星座网
        'https://www.d1xz.net/sx/ji/index_1.aspx': 115,   #  第一星座网
        'https://www.d1xz.net/sx/gou/index_1.aspx': 116,   #  第一星座网
        'https://www.d1xz.net/sx/zhu/index_1.aspx': 117,   #  第一星座网
        'https://www.d1xz.net/sx/shu/': 118,   #  第一星座网
        'https://www.d1xz.net/sx/niu/': 119,   #  第一星座网
        'https://www.d1xz.net/sx/hu/': 120,   #  第一星座网
        'https://www.d1xz.net/sx/tu/': 121,   #  第一星座网
        'https://www.d1xz.net/sx/long/': 122,   #  第一星座网
        'https://www.d1xz.net/sx/she/': 123,   #  第一星座网
        'https://www.d1xz.net/sx/ma/': 124,   #  第一星座网
        'https://www.d1xz.net/sx/yang/': 125,   #  第一星座网
        'https://www.d1xz.net/sx/hou/': 126,   #  第一星座网
        'https://www.d1xz.net/sx/ji/': 127,   #  第一星座网
        'https://www.d1xz.net/sx/gou/': 128,   #  第一星座网
        'https://www.d1xz.net/sx/zhu/': 129,   #  第一星座网
        'https://www.d1xz.net/fsml/': 130,   #  第一星座网
        'https://www.d1xz.net/fsml/fszc/': 131,   #  第一星座网
        'https://www.d1xz.net/fsml/aqfs/': 132,   #  第一星座网
        'https://www.d1xz.net/fsml/syfs/': 133,   #  第一星座网
        'https://www.d1xz.net/fsml/kyhs/': 134,   #  第一星座网
        'https://www.d1xz.net/fsml/jiajufengshui/': 135,   #  第一星座网
        'https://www.d1xz.net/zt/bangongfengshui/': 136,   #  第一星座网
        'https://www.d1xz.net/mingli/': 137,   #  第一星座网
        'https://www.d1xz.net/fsml/xsdq/zhixiang/': 138,   #  第一星座网
        'https://www.d1xz.net/fsml/xsdq/mianxiang/': 139,   #  第一星座网
        'https://www.d1xz.net/fsml/bgml/': 140,   #  第一星座网
        'https://www.d1xz.net/fsml/xmcz/': 141,   #  第一星座网
        'https://www.d1xz.net/fsml/xsdq/shouxiangzhuanti/': 142,   #  第一星座网
        'https://www.d1xz.net/fsml/xsdq/': 143,   #  第一星座网
        'https://www.d1xz.net/sm/bazisuanming/': 144,   #  第一星座网
        'https://www.d1xz.net/rili/': 145,   #  第一星座网
        'https://www.d1xz.net/rili/rilibiao/': 146,   #  第一星座网
        'https://www.d1xz.net/rili/jieri/': 147,   #  第一星座网
        'https://www.d1xz.net/rili/jieqi/': 148,   #  第一星座网
        'https://www.d1xz.net/rili/jiri/': 149,   #  第一星座网
        'https://www.d1xz.net/wenhua/': 150,   #  第一星座网
        'https://www.d1xz.net/wenhua/yinshi/': 151,   #  第一星座网
        'https://www.d1xz.net/wenhua/chengshi/': 152,   #  第一星座网
        'https://www.d1xz.net/wenhua/zongjiao/': 153,   #  第一星座网
        'https://www.d1xz.net/wenhua/minzu/': 154,   #  第一星座网
        'https://www.d1xz.net/wenhua/gushi/': 155,   #  第一星座网
        'https://www.d1xz.net/wenhua/xiju/': 156,   #  第一星座网

    }

    rules = (
        # https://www.d1xz.net/astro/kaiyun/art306160.aspx
        Rule(LinkExtractor(allow=r'd1xz.net/\w+/\w+/art\d+\.aspx',),
             callback='parse_item',
             follow=False),

        Rule(LinkExtractor(allow=r'd1xz.net/.*?\.aspx', deny=(r'/jm', '/pic', r'/index')),
             process_request=otherurl_meta,
             follow=False),
    )


    def parse_item(self, response):
        # https://www.d1xz.net/astro/kaiyun/art306160.aspx
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//h1[@class='art_detail_title']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//div[@class='source']/p/span[1]/text()").extract_first())
            content_div = xp("//div[@class='common_det_con']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False,
                                                                     kill_xpaths=["//div[@class='common_det_con']/p[last()]"])  # str  list
            origin_name = "第一星座网"  # None  不要用[0]
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



