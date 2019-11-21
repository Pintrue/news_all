from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from news_all.spider_models import NewsRCSpider, otherurl_meta, js_meta
from datetime import datetime
from news_all.tools.time_translater import Pubtime
import re
from copy import deepcopy

class Auto(NewsRCSpider):
    name = 'autohome'

    custom_settings = {'DOWNLOADER_MIDDLEWARES':
                           {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'news_all.middlewares.UserAgentMiddleware': 20,
                            'news_all.middlewares.PhantomJSMiddleware': 540,
                            }}
    start_meta = {'jstype': True}

    # 汽车之家网 ==》 补充全站采集
    mystart_urls = {
        'https://www.autohome.com.cn/beijing/': 7408,   #  汽车之家
        'https://www.autohome.com.cn/all/#pvareaid=3311229': 7409,   #  汽车之家
        'https://www.autohome.com.cn/topics/#pvareaid=2023455': 7410,   #  汽车之家
        'https://www.autohome.com.cn/topics/1': 7411,   #  汽车之家
        'https://www.autohome.com.cn/topics/': 7412,   #  汽车之家
        'https://www.autohome.com.cn/topics/2': 7413,   #  汽车之家
        'https://www.autohome.com.cn/topics/3': 7414,   #  汽车之家
        'https://www.autohome.com.cn/topics/5': 7415,   #  汽车之家
        'https://www.autohome.com.cn/topics/6': 7416,   #  汽车之家
        'https://www.autohome.com.cn/bestauto/#pvareaid=3311236': 7417,   #  汽车之家
        'https://chejiahao.autohome.com.cn/#pvareaid=3311237': 7418,   #  汽车之家
        'https://chejiahao.autohome.com.cn/Good#pvareaid=2808145': 7419,   #  汽车之家
        'https://chejiahao.autohome.com.cn/category/1#pvareaid=2808145': 7420,   #  汽车之家
        'https://chejiahao.autohome.com.cn/category/2#pvareaid=2808145': 7421,   #  汽车之家
        'https://chejiahao.autohome.com.cn/category/3#pvareaid=2808145': 7422,   #  汽车之家
        'https://chejiahao.autohome.com.cn/category/4#pvareaid=2808145': 7423,   #  汽车之家
        'https://chejiahao.autohome.com.cn/category/5#pvareaid=2808145': 7424,   #  汽车之家
        'https://chejiahao.autohome.com.cn/category/6#pvareaid=2808145': 7425,   #  汽车之家
        'https://chejiahao.autohome.com.cn/category/7#pvareaid=2808145': 7426,   #  汽车之家
        'https://chejiahao.autohome.com.cn/category/8#pvareaid=2808145': 7427,   #  汽车之家
        'https://chejiahao.autohome.com.cn/category/9#pvareaid=2808145': 7428,   #  汽车之家
        'https://chejiahao.autohome.com.cn/category/10#pvareaid=2808145': 7429,   #  汽车之家
        'https://chejiahao.autohome.com.cn/category/11#pvareaid=2808145': 7430,   #  汽车之家
        'https://v.autohome.com.cn/#pvareaid=3311238': 7431,   #  汽车之家
        'https://v.autohome.com.cn/#': 7432,   #  汽车之家
        'https://v.autohome.com.cn/u/19996353/#pvareaid=3454181': 7433,   #  汽车之家
        'https://v.autohome.com.cn/u/19987472/#pvareaid=3454181': 7434,   #  汽车之家
        'https://v.autohome.com.cn/u/35729101/#pvareaid=3454181': 7435,   #  汽车之家
        'https://v.autohome.com.cn/u/66592556/#pvareaid=3454181': 7436,   #  汽车之家
        'https://v.autohome.com.cn/u/27493450/#pvareaid=3454181': 7437,   #  汽车之家
        'https://v.autohome.com.cn/u/41890819/#pvareaid=3454181': 7438,   #  汽车之家
        'https://v.autohome.com.cn/u/53106259/#pvareaid=3454181': 7439,   #  汽车之家
        'https://v.autohome.com.cn/u/40398749/#pvareaid=3454181': 7440,   #  汽车之家
        'https://v.autohome.com.cn/u/20380947/#pvareaid=3454181': 7441,   #  汽车之家
        'https://v.autohome.com.cn/u/94904626/#pvareaid=3454181': 7442,   #  汽车之家
        'https://www.autohome.com.cn/hangye/#pvareaid=6825588': 7443,   #  汽车之家
        'https://www.autohome.com.cn/hangye/': 7444,   #  汽车之家
        'https://www.autohome.com.cn/hangye/news/': 7445,   #  汽车之家
        'https://www.autohome.com.cn/hangye/guandian/': 7446,   #  汽车之家
        'https://club.autohome.com.cn/#pvareaid=3311253': 7447,   #  汽车之家
        'https://club.autohome.com.cn/newfe/videocommunity#pvareaid=6830656': 7448,   #  汽车之家
        'https://club.autohome.com.cn/jingxuan/#pvareaid=3311254': 7449,   #  汽车之家
        'https://club.autohome.com.cn/Young/Index#pvareaid=3454621': 7450,   #  汽车之家
        'https://wenda.autohome.com.cn/#pvareaid=3468129': 7451,   #  汽车之家
        'https://www.autohome.com.cn/ev/#pvareaid=3454680': 7452,   #  汽车之家
        'https://ev.autohome.com.cn/#pvareaid=3311257': 7453,   #  汽车之家
        'https://www.autohome.com.cn/all/#pvareaid=3311481': 7454,   #  汽车之家
        'https://www.autohome.com.cn/all/': 7455,   #  汽车之家
        'https://www.autohome.com.cn/news/': 7456,   #  汽车之家
        'https://www.autohome.com.cn/advice/': 7457,   #  汽车之家
        'https://www.autohome.com.cn/drive/': 7458,   #  汽车之家
        'https://www.autohome.com.cn/use/': 7459,   #  汽车之家
        'https://www.autohome.com.cn/culture/': 7460,   #  汽车之家
        'https://www.autohome.com.cn/travels/': 7461,   #  汽车之家
        'https://www.autohome.com.cn/tech/': 7462,   #  汽车之家
        'https://www.autohome.com.cn/tuning/': 7463,   #  汽车之家
        'https://www.autohome.com.cn/ev/': 7464,   #  汽车之家
        'https://www.autohome.com.cn/hangye/list/': 7465,   #  汽车之家


    }

    rules = (

        # https://chejiahao.autohome.com.cn/info/4895107
        # https://www.autohome.com.cn/news/201911/951442.html?pvareaid=3311316
        # https://www.autohome.com.cn/topic/1338/#pvareaid=2023456
        # https://buy.autohome.com.cn/37984/0/102094/441874315.html#pvareaid=3311449
        Rule(LinkExtractor(allow=r'.autohome.com.cn/info/\d+'),
             callback='parse_item',
             follow=False,
             process_request=js_meta),

        Rule(LinkExtractor(allow=r'.autohome.com.cn/.*/%s/\d+\.html' % datetime.today().strftime('%Y%m'),),
             callback='parse_item_2',
             follow=False,
             process_request=js_meta),

        Rule(LinkExtractor(allow=r'.autohome.com.cn/topic/\d+/.*'),
             callback='parse_item_6',
             follow=False,
             process_request=js_meta),

        Rule(LinkExtractor(allow=r'.autohome.com.cn/.*?'),
             process_request=otherurl_meta,
             follow=False),
    )

    def parse_item(self, response):
        # https://chejiahao.autohome.com.cn/info/4895107
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//span[@class='text-overflow ']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = xp("//div[@class='articleTag']/span[3]/text()").extract_first()
            content_div = xp("//div[@class='introduce_content']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)  # str  list
            origin_name = xp("//div[@class='articleTag']/span[1]/text()").extract_first()# None  不要用[0]
        except Exception as e:
            return self.parse_item_3(response)

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
        # https://www.autohome.com.cn/news/201911/951442.html?pvareaid=3311316
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@id='articlewrap']/h1/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = xp("//span[@class='time']/text()").extract_first()
            content_div = xp("//div[@id='articleContent']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False,
                                                                     kill_xpaths=("//div[@class='article-extend article-extend-old']"))  # str  list
            origin_name = xp("//span[@class='source']/a/text()").extract_first()# None  不要用[0]
        except Exception as e:
            try:
                title_url = xp("//div[@class='top-title']/a/@href").get()
                return response.follow(title_url, callback=self.parse_item_2)
            except Exception as e:
                return self.parse_item_5(response)

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
        """换页图"""
        # https://chejiahao.autohome.com.cn/info/5082670
        xp = response.xpath
        try:
            title_list = xp("//div[@class='introduce']/p[@class='text']/text()").get()
            title = re.findall(r"【(.*)】", title_list)[0]
            pubtime = Pubtime(xp("//div[@class='articleTag']/span[3]/text()").extract_first())
            content_div = xp("//div[@class='introduce']/p[@class='text']")[0]
            content, _, _, _ = self.content_clean(content_div, need_video=False)# str  list
            imgs = xp("//div[@class='stage-box']/ul//img/@src").extract()
            origin_name = xp("//div[@class='articleTag']/span[1]/text()").extract_first()# None  不要用[0]
            media = self.make_img_content(imgs)

        except Exception as e:
            return self.parse_item_4(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
        )

    def make_img_content(self, img_url_list):
            # http://qnwww2.autoimg.cn/chejiahaodfs/g3/M05/4A/A3/autohomecar__ChsEm13SNK2AZuihAAa63DwexLQ294.jpg?
            media = {'images': {}}
            for i, j in enumerate(img_url_list):
                img_url = 'http:' + re.findall(r'//.*\.jpg', j)[0]
                media['images'][str(i + 1)] = {"src": img_url}
            return media

    def parse_item_4(self, response):
        """有视频"""
        # https://chejiahao.autohome.com.cn/info/5082878
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//span[@class='text-overflow ']/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = Pubtime(xp("//div[@class='articleTag']/span[3]/text()").extract_first())
            video_url = xp("//video/@src").get()
            videos = {'1': {'src': video_url}}
            content = '<div>#{{1}}#</div>'  # str  list
            origin_name = xp("//div[@class='articleTag']/span[1]/text()").extract_first()# None  不要用[0]
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

    def parse_item_5(self, response):
        # https://m.autohome.com.cn/news/201911/951768.html#pvareaid=6825865
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//header[@class='header']/h1/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = xp("//div[@class='user']/div[@class='date']/text()").extract_first()
            content_div = xp("//div[@id='content']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)  # str  list
            origin_name = "汽车之家"  # None  不要用[0]
        except Exception as e:
            return self.parse_item_7(response)

        return self.produce_item(
            response=response,
            title=title,
            pubtime=pubtime,
            origin_name=origin_name,  # ""  None xpath
            content=content,
            media=media,
            videos=videos,

        )

    def parse_item_6(self, response):
        # https://www.autohome.com.cn/topic/1338/#pvareaid=2023456
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@id='articlewrap']/h1/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = xp("//div[@class='article-info']/span[1]/text()").extract_first()
            pubtime = re.sub(r'\s+', '', pubtime)
            content_div = xp("//div[@id='articleContent']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)  # str  list
            origin_name = xp("//div[@class='article-info']/span[2]/a/text()").get()  # None  不要用[0]
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

    def parse_item_7(self, response):
        # https://www.autohome.com.cn/dealer/201911/442000840.html#pvareaid=3311336
        xp = response.xpath
        try:
            title = self.get_page_title(response).split('_')[0] or xp(
                "//div[@class='area article']/h1/text()").extract_first()  # self.get_page_title(response).split('_')[0]
            pubtime = xp("//div[@class='article-info']/span[1]/text()").extract_first()
            content_div = xp("//div[@class='dealertext']")[0]
            content, media, videos, video_cover = self.content_clean(content_div, need_video=False)  # str  list
            origin_name = xp("//div[@class='article-info']/span[2]/text()").get()  # None  不要用[0]
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







