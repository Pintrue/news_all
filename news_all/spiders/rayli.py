from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta
from datetime import datetime
from news_all.tools.time_translater import Pubtime
import re


class Rayli(NewsRCSpider):
    name = 'rayli'

    # 瑞丽网 ==》 补充全站采集
    mystart_urls = {
        'http://www.rayli.com.cn/': 7358,   #  瑞丽网
        'http://fashion.rayli.com.cn/': 7359,   #  瑞丽网
        'http://fashion.rayli.com.cn/mixmatch/': 7360,   #  瑞丽网
        'http://fashion.rayli.com.cn/star/': 7361,   #  瑞丽网
        'http://fashion.rayli.com.cn/products/': 7362,   #  瑞丽网
        'http://fashion.rayli.com.cn/lookbook/': 7363,   #  瑞丽网
        'http://fashion.rayli.com.cn/feature/': 7364,   #  瑞丽网
        'http://fashion.rayli.com.cn/brands/': 7365,   #  瑞丽网
        'http://fashion.rayli.com.cn/feature/coverstar/': 7366,   #  瑞丽网
        'http://beauty.rayli.com.cn/': 7367,   #  瑞丽网
        'http://beauty.rayli.com.cn/skincare/': 7368,   #  瑞丽网
        'http://beauty.rayli.com.cn/makeup/': 7369,   #  瑞丽网
        'http://beauty.rayli.com.cn/bodyandperfume/': 7370,   #  瑞丽网
        'http://beauty.rayli.com.cn/products/': 7371,   #  瑞丽网
        'http://beauty.rayli.com.cn/exclusive/': 7372,   #  瑞丽网
        'http://beauty.rayli.com.cn/feature/': 7373,   #  瑞丽网
        'http://beauty.rayli.com.cn/articles/index.shtml': 7374,   #  瑞丽网
        'http://hair.rayli.com.cn/': 7375,   #  瑞丽网
        'http://hair.rayli.com.cn/starhair/': 7376,   #  瑞丽网
        'http://hair.rayli.com.cn/hairstyle/': 7377,   #  瑞丽网
        'http://hair.rayli.com.cn/hairproducts/': 7378,   #  瑞丽网
        'http://hair.rayli.com.cn/news/': 7379,   #  瑞丽网
        'http://lightluxury.rayli.com.cn/': 7380,   #  瑞丽网
        'http://lightluxury.rayli.com.cn/highfashion/': 7381,   #  瑞丽网
        'http://lightluxury.rayli.com.cn/shoesandbags/': 7382,   #  瑞丽网
        'http://lightluxury.rayli.com.cn/luxurylife/': 7383,   #  瑞丽网
        'http://lightluxury.rayli.com.cn/articles/': 7384,   #  瑞丽网
        'http://celeb.rayli.com.cn/': 7385,   #  瑞丽网
        'http://fashion.rayli.com.cn/star/starstyle/': 7386,   #  瑞丽网
        'http://beauty.rayli.com.cn/makeup/star/': 7387,   #  瑞丽网
        'http://life.rayli.com.cn/fun/': 7388,   #  瑞丽网
        'http://beauty.rayli.com.cn/drama/': 7389,   #  瑞丽网
        'http://inleon.rayli.com.cn/': 7390,   #  瑞丽网
        'http://inleon.rayli.com.cn/fashion/': 7391,   #  瑞丽网
        'http://inleon.rayli.com.cn/snap/': 7392,   #  瑞丽网
        'http://inleon.rayli.com.cn/celebrities/': 7393,   #  瑞丽网
        'http://inleon.rayli.com.cn/car/': 7394,   #  瑞丽网
        'http://inleon.rayli.com.cn/watch/': 7395,   #  瑞丽网
        'http://inleon.rayli.com.cn/lifestyle/': 7396,   #  瑞丽网
        'http://inleon.rayli.com.cn/video/': 7397,   #  瑞丽网
        'http://life.rayli.com.cn/': 7398,   #  瑞丽网
        'http://life.rayli.com.cn/health/': 7399,   #  瑞丽网
        'http://life.rayli.com.cn/food/': 7400,   #  瑞丽网
        'http://life.rayli.com.cn/travel/': 7401,   #  瑞丽网
        'http://life.rayli.com.cn/player/': 7402,   #  瑞丽网
        # 'http://life.rayli.com.cn/fun/': 7403,   #  瑞丽网 网站重复
        'http://life.rayli.com.cn/parents/': 7404,   #  瑞丽网
        'http://video.rayli.com.cn/': 7405,   #  瑞丽网
        'http://video.rayli.com.cn/live/': 7406,   #  瑞丽网
        'http://video.rayli.com.cn/celebrity/': 7407,   #  瑞丽网


    }

    rules = (
        # http://beauty.rayli.com.cn/makeup/star/2019-11-12/664656.shtml
        # http://inleon.rayli.com.cn/video/1970-01-01/622715.shtml
        Rule(LinkExtractor(
            allow=r'.rayli.com.cn/.*?/%s-\d{2}/\d+\.shtml' % datetime.today().strftime('%Y-%m'), deny='/video'),
             callback='parse_item',
             follow=False),
        Rule(LinkExtractor(
            allow=r'.rayli.com.cn/video/.*?'),
            callback='parse_item_2',
            follow=False),

        Rule(LinkExtractor(allow=r'.rayli.com.cn/.*?\.shtml', deny=(r'/201[0-8]', r'/2019-0[1-9]', r'/2019-1[0]',
                                                                    r'/index'),),
             process_request=otherurl_meta,
             follow=False),
    )

    def parse_item(self, response):
        # http://beauty.rayli.com.cn/makeup/star/2019-11-12/664656.shtml
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//h1[@class='title mar-t-20']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//p[@class='source']/span[1]/text()").extract_first())
            try:
                content_div = xp("//div[@id='js_content']")[0]
                content, media, videos, video_cover = self.content_clean(content_div, need_video=False)  # str  list
            except:
                content_div = xp("//div[@class='summary']")[0]
                content, media, videos, video_cover = self.content_clean(content_div, need_video=False,
                                                                         kill_xpaths=["//h1[@class='title mar-t-20']",
                                                                                      "//p[@class='source']"])  # str  list

            origin_name = xp("//p[@class='source']/span[2]/text()").extract_first()# None  不要用[0]
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

    def parse_item_2(self, response):
        """video"""
        # http://inleon.rayli.com.cn/video/1970-01-01/622715.shtml
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//h3[@class='title mar-t-20']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//p[@class='source']/span[1]/text()").extract_first())
            video_div = xp("//div[@class='video_d']/script/text()").get()
            # http://v.rayli.com.cn/2018-05-07/20180507193252.mp4
            video_url = re.findall(r'http://.*?\.mp4', video_div)[0]
            videos = {'1': {'src': video_url}}
            content = '<div>#{{1}}#</div>'
            origin_name = xp("//p[@class='source']/span[2]/text()").extract_first()  # None  不要用[0]
        except Exception as e:
            return self.produce_debugitem(response, "xpath error")

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            videos=videos,

        )



