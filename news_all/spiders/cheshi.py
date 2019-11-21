from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from news_all.tools.time_translater import Pubtime


class Cheshi(NewsRCSpider):
    name = 'cheshi'

    # 网上车市==》 补充全站采集
    mystart_urls = {
        'http://www.cheshi.com/': 1,  # 网上车市
        'http://news.cheshi.com/': 2,  # 网上车市
        'http://news.cheshi.com/djbd/': 3,  # 网上车市
        'http://news.cheshi.com/video/': 4,  # 网上车市
        'http://news.cheshi.com/diaoyan/': 5,  # 网上车市
        'http://news.cheshi.com/hyyj/': 6,  # 网上车市
        'http://news.cheshi.com/pingce/': 7,  # 网上车市
        'http://news.cheshi.com/luxury.shtml': 8,  # 网上车市
        'http://news.cheshi.com/suv.shtml': 9,  # 网上车市
        'http://news.cheshi.com/fashion/': 10,  # 网上车市
        'http://news.cheshi.com/yule/morelist_1.shtml': 11,  # 网上车市
        'http://news.cheshi.com/xcjd/morelist_1.shtml': 12,  # 网上车市
        'http://ask.cheshi.com/': 13,  # 网上车市
        'http://bbs.cheshi.com/': 14,  # 网上车市
        'http://bbs.cheshi.com/1/': 15,  # 网上车市
        'http://bbs.cheshi.com/club/post-3914-1.html': 16,  # 网上车市
        'http://bbs.cheshi.com/club/post-1465-1.html': 17,  # 网上车市
        'http://bbs.cheshi.com/club/post-1508-1.html': 18,  # 网上车市
        'http://bbs.cheshi.com/club/post-1463-1.html': 19,  # 网上车市
        'http://www.haoche18.com/': 20,  # 网上车市
        'http://news.cheshi.com/pika.shtml': 21,  # 网上车市
        'https://cheshihao.cheshi.com/': 22,  # 网上车市
        'https://cheshihao.cheshi.com/2.html': 23,  # 网上车市
        'https://cheshihao.cheshi.com/3.html': 24,  # 网上车市
        'https://cheshihao.cheshi.com/4.html': 25,  # 网上车市
        'https://cheshihao.cheshi.com/5.html': 26,  # 网上车市
        'https://cheshihao.cheshi.com/6.html': 27,  # 网上车市
        'https://cheshihao.cheshi.com/7.html': 28,  # 网上车市
        'https://cheshihao.cheshi.com/8.html': 29,  # 网上车市
        'http://auto.cztv.com/cate_44/': 30,  # 网上车市
        'http://news.cheshi.com/daogou/morelist_1.shtml': 31,  # 网上车市

    }

    rules = (
        # http://news.cheshi.com/dujia/20191113/3232564.shtml
        Rule(LinkExtractor(allow=r'.cheshi.com/\w+/%s\d{2}/\d+\.shtml' % datetime.today().strftime('%Y%m'),),
             callback='parse_item',
             follow=False),

        Rule(LinkExtractor(allow=r'.cheshi.com/.*?\.shtml', deny=(r'/201[0-8]', r'/20190[1-9]', r'/20191[0]',
                                                                  r'/morelist'),),
             process_request=otherurl_meta,
             follow=False),
    )


    def parse_item(self, response):
        # http://news.cheshi.com/dujia/20191113/3232564.shtml
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='border-box']/h2/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//span[@class='fr']/text()").extract_first())
            content_div = xp("//div[@class='border-box']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False,
                                                                     kill_xpaths=["//div[@class='article_info']",
                                                                                  "//div[@class='border-box']/h2",
                                                                                  "//div[@class='border-box']/h2"])  # str  list
            origin_name = xp("string(//div[@class='article_l fl']/span[3])").get()# None  不要用[0]
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



