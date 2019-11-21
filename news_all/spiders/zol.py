from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from news_all.tools.time_translater import Pubtime


class Zol(NewsRCSpider):
    name = 'zol'

    # 中关村在线==》 补充全站采集
    mystart_urls = {
        'http://www.zol.com.cn/': 1,   #  中关村在线
        'http://news.zol.com.cn/': 2,   #  中关村在线
        'http://news.zol.com.cn/list.html': 3,   #  中关村在线
        'http://news.zol.com.cn/trend/': 4,   #  中关村在线
        'http://bigdata.zol.com.cn/': 5,   #  中关村在线
        'http://bigdata.zol.com.cn/list.html': 6,   #  中关村在线
        'http://bigdata.zol.com.cn/more/2_1860.shtml': 7,   #  中关村在线
        'http://auto.zol.com.cn/': 8,   #  中关村在线
        'http://auto.zol.com.cn/xny.shtml': 9,   #  中关村在线
        'http://ebike.zol.com.cn/': 10,   #  中关村在线
        'http://ebike.zol.com.cn/list.html': 11,   #  中关村在线
        'http://ebike.zol.com.cn/more/2_1921.shtml': 12,   #  中关村在线
        'http://ebike.zol.com.cn/more/2_1923.shtml': 13,   #  中关村在线
        'http://smartwear.zol.com.cn/': 14,   #  中关村在线
        'http://geek.zol.com.cn/detail_13236/': 15,   #  中关村在线
        'http://geek.zol.com.cn/detail_13229/': 16,   #  中关村在线
        'http://bbs.zol.com.cn/cdbbs/': 17,   #  中关村在线
        'http://geek.zol.com.cn/': 18,   #  中关村在线
        'http://zhibo.zol.com.cn/': 19,   #  中关村在线
        'http://news.zol.com.cn/pk/': 20,   #  中关村在线
        'http://news.zol.com.cn/renwu.html': 21,   #  中关村在线
        'http://tupian.zol.com.cn/tushuo/': 22,   #  中关村在线
        'http://tupian.zol.com.cn/tushuo/wanshuma/': 23,   #  中关村在线
        'http://tupian.zol.com.cn/tushuo/duredian/': 24,   #  中关村在线
        'http://tupian.zol.com.cn/tushuo/qukeji/': 25,   #  中关村在线
        'http://tupian.zol.com.cn/tushuo/kanshuju/': 26,   #  中关村在线
        'http://news.zol.com.cn/more/2_1999.shtml': 27,   #  中关村在线
        'http://news.zol.com.cn/more/3_3961.shtml': 28,   #  中关村在线
        'http://news.zol.com.cn/more/3_3962.shtml': 29,   #  中关村在线
        'http://news.zol.com.cn/more/3_3963.shtml': 30,   #  中关村在线
        'http://news.zol.com.cn/more/3_3964.shtml': 31,   #  中关村在线
        'http://news.zol.com.cn/more/3_3965.shtml': 32,   #  中关村在线
        'http://news.zol.com.cn/more/3_3966.shtml': 33,   #  中关村在线
        'http://news.zol.com.cn/more/3_4004.shtml': 34,   #  中关村在线
        'http://news.zol.com.cn/more/3_4005.shtml': 35,   #  中关村在线
        'http://labs.zol.com.cn/': 36,   #  中关村在线
        'http://labs.zol.com.cn/jingxuan.html': 37,   #  中关村在线
        'http://labs.zol.com.cn/fenlei.html': 38,   #  中关村在线
        'http://labs.zol.com.cn/xinpin.html': 39,   #  中关村在线
        'http://labs.zol.com.cn/duibi.html': 40,   #  中关村在线
        'http://price.zol.com.cn/': 41,   #  中关村在线
        'http://price.zol.com.cn/manu.html': 42,   #  中关村在线
        'http://tupian.zol.com.cn/': 43,   #  中关村在线
        'http://tupian.zol.com.cn/jingxuan/': 44,   #  中关村在线
        'http://tupian.zol.com.cn/1/': 45,   #  中关村在线
        'http://tupian.zol.com.cn/2/': 46,   #  中关村在线
        'http://tupian.zol.com.cn/4/': 47,   #  中关村在线
        'http://zol.iqiyi.com.cn/': 48,   #  中关村在线
        'http://top.zol.com.cn/': 49,   #  中关村在线
        'http://dealer.zol.com.cn/beijing/': 50,   #  中关村在线
        'http://ask.zol.com.cn/': 51,   #  中关村在线
        'http://ask.zol.com.cn/video/': 52,   #  中关村在线
        'http://bbs.zol.com.cn/quanzi/': 53,   #  中关村在线
        'http://bbs.zol.com.cn/quanzi/d14.html': 54,   #  中关村在线
        'http://bbs.zol.com.cn/sjbbs/': 55,   #  中关村在线
        'http://bbs.zol.com.cn/dcbbs/': 56,   #  中关村在线
        'http://soft.zol.com.cn/jingyan/': 57,   #  中关村在线
        'http://soft.zol.com.cn/jingyan/new.html': 58,   #  中关村在线
        'http://soft.zol.com.cn/more/2_1261.shtml': 59,   #  中关村在线
        'http://sj.zol.com.cn/game/': 60,   #  中关村在线
        'http://mobile.zol.com.cn/': 61,   #  中关村在线
        'http://nb.zol.com.cn/': 62,   #  中关村在线
        'http://nb.zol.com.cn/list.html': 63,   #  中关村在线
        'http://nb.zol.com.cn/more/3_1983.shtml': 64,   #  中关村在线
        'http://nb.zol.com.cn/more/3_1984.shtml': 65,   #  中关村在线
        'http://nb.zol.com.cn/more/2_1081.shtml': 66,   #  中关村在线
        'http://nb.zol.com.cn/more/2_1080.shtml': 67,   #  中关村在线
        'http://nb.zol.com.cn/yxb/': 68,   #  中关村在线
        'http://nb.zol.com.cn/biz.html': 69,   #  中关村在线
        'http://nb.zol.com.cn/detail_13728/': 70,   #  中关村在线
        'http://nb.zol.com.cn/detail_13729/': 71,   #  中关村在线
        'http://pc.zol.com.cn/': 72,   #  中关村在线
        'http://robot.zol.com.cn/': 73,   #  中关村在线
        'http://aio.zol.com.cn/': 74,   #  中关村在线
        'http://diy.zol.com.cn/': 75,   #  中关村在线
        'http://dcdv.zol.com.cn/': 76,   #  中关村在线
        'http://dcdv.zol.com.cn/more/2_782.shtml': 77,   #  中关村在线
        'http://dcdv.zol.com.cn/more/2_785.shtml': 78,   #  中关村在线
        'http://dcdv.zol.com.cn/more/2_784.shtml': 79,   #  中关村在线
        'http://dcdv.zol.com.cn/more/2_2006.shtml': 80,   #  中关村在线
        'http://dcdv.zol.com.cn/dslr.html': 81,   #  中关村在线
        'http://dcdv.zol.com.cn/more/3_1342.shtml': 82,   #  中关村在线
        'http://dcdv.zol.com.cn/more/3_1354.shtml': 83,   #  中关村在线
        'http://dv.zol.com.cn/': 84,   #  中关村在线
        'http://sound.zol.com.cn/': 85,   #  中关村在线
        'http://headphone.zol.com.cn/': 86,   #  中关村在线
        'http://hifi.zol.com.cn/': 87,   #  中关村在线
        'http://lanya.zol.com.cn/': 88,   #  中关村在线
        'http://ht.zol.com.cn/': 89,   #  中关村在线
        'http://projector.zol.com.cn/': 90,   #  中关村在线
        'http://projector.zol.com.cn/list.html': 91,   #  中关村在线
        'http://projector.zol.com.cn/more/3_1708.shtml': 92,   #  中关村在线
        'http://projector.zol.com.cn/more/2_960.shtml': 93,   #  中关村在线
        'http://search.zol.com.cn/s/video.php?kword=%CD%B6%D3%B0&orderby=cdate': 94,   #  中关村在线
        'http://projector.zol.com.cn/more/2_962.shtml': 95,   #  中关村在线
        'http://jd.zol.com.cn/': 96,   #  中关村在线
        'http://jd.zol.com.cn/more/2_1028.shtml': 97,   #  中关村在线
        'http://jd.zol.com.cn/more/2_1029.shtml': 98,   #  中关村在线
        'http://jd.zol.com.cn/detail_11973/': 99,   #  中关村在线
        'http://jd.zol.com.cn/slide_1.html': 100,   #  中关村在线
        'http://sh.zol.com.cn/': 101,   #  中关村在线
        'http://sh.zol.com.cn/kitchen.html': 102,   #  中关村在线
        'http://sh.zol.com.cn/more/2_1754.shtml': 103,   #  中关村在线
        'http://sh.zol.com.cn/health.html': 104,   #  中关村在线
        'http://sh.zol.com.cn/iot.html': 105,   #  中关村在线
        'http://biz.zol.com.cn/': 106,   #  中关村在线
        'http://biz.zol.com.cn/list.html': 107,   #  中关村在线
        'http://biz.zol.com.cn/more/2_1882.shtml': 108,   #  中关村在线
        'http://dt.zol.com.cn/list.html': 109,   #  中关村在线
        'http://dt.zol.com.cn/': 110,   #  中关村在线
        'http://biz.zol.com.cn/more/2_1883.shtml': 111,   #  中关村在线
        'http://oa.zol.com.cn/': 112,   #  中关村在线
        'http://oa.zol.com.cn/printer.html': 113,   #  中关村在线
        'http://oa.zol.com.cn/aio.html': 114,   #  中关村在线
        'http://oa.zol.com.cn/mfp.html': 115,   #  中关村在线
        'http://oa.zol.com.cn/scanner.html': 116,   #  中关村在线
        'http://oa.zol.com.cn/haocai.shtml': 117,   #  中关村在线
        'http://oa.zol.com.cn/topic/3647381.html': 118,   #  中关村在线
        'http://oa.zol.com.cn/more/3_1762.shtml': 119,   #  中关村在线
        'http://oa.zol.com.cn/more/3_1767.shtml': 120,   #  中关村在线
        'http://oa.zol.com.cn/more/3_1766.shtml': 121,   #  中关村在线
        'http://oa.zol.com.cn/more/3_1763.shtml': 122,   #  中关村在线
        'http://oa.zol.com.cn/more/3_3247.shtml': 123,   #  中关村在线
        'http://oa.zol.com.cn/more/2_994.shtml': 124,   #  中关村在线
        'http://auto.zol.com.cn/more/2_1703.shtml': 125,   #  中关村在线
        'http://gps.zol.com.cn/': 126,   #  中关村在线
        'http://gps.zol.com.cn/list.html': 127,   #  中关村在线
        'http://gps.zol.com.cn/more/2_1006.shtml': 128,   #  中关村在线

    }

    rules = (
        # http://news.zol.com.cn/732/7321917.html
        # http://www.zol.com/goods/7321836.html?t=1573552764
        Rule(LinkExtractor(allow=r'.zol.com.cn/\d+/\d+\.html',),
             callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=r'.zol.com.cn/.*?\.html',),
             process_request=otherurl_meta,
             follow=False),
    )


    def parse_item(self, response):
        # http://news.zol.com.cn/732/7321917.html
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='article-header clearfix']/h1/text()").extract_first()
            pubtime = Pubtime(xp("//span[@id='pubtime_baidu']/text()").extract_first())
            content_div = xp("//div[@class='article-cont clearfix']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)  # str  list
            origin_name = xp("//span[@id='source_baidu']/text()").extract_first()  # None  不要用[0]
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







